import sys
import os
from prisma import Prisma
from typing import List, Dict, Optional
import pyotp
from datetime import datetime

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

class TwoFAModel:
    def __init__(self):
        self.db = None
        # Sử dụng config từ config.py nếu không có .env
        self.deploy_mode = config.DEPLOY
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database theo môi trường"""
        try:
            if self.deploy_mode == 'LOCAL':
                # LOCAL: Sử dụng Prisma client đã generate
                self.db = Prisma()
                self.db.connect()
                print(f"✅ Kết nối database LOCAL thành công")
            elif self.deploy_mode == 'PRODUCTION':
                # PRODUCTION: Kết nối trực tiếp đến DATABASE_URL
                self.db = Prisma()
                # Sử dụng DATABASE_URL từ config
                database_url = config.get_database_url()
                if not database_url:
                    raise Exception("DATABASE_URL không được thiết lập cho môi trường PRODUCTION")
                self.db.connect()
                print(f"✅ Kết nối database PRODUCTION thành công")
                print(f"🔗 Database: {database_url.split('@')[1] if '@' in database_url else database_url}")
            else:
                raise Exception(f"DEPLOY mode không hợp lệ: {self.deploy_mode}")
                
        except Exception as e:
            print(f"❌ Lỗi kết nối database: {e}")
            raise e
    
    def __del__(self):
        if hasattr(self, 'db') and self.db:
            try:
                self.db.disconnect()
            except:
                pass
    
    def add_account(self, name: str, secret_key: str, key_type: str = "TOTP") -> bool:
        """Thêm tài khoản mới"""
        try:
            # Kiểm tra secret key có hợp lệ không
            totp = pyotp.TOTP(secret_key)
            totp.now()  # Test tạo mã
            
            # Loại bỏ khoảng trắng và ký tự đặc biệt từ secret key
            cleaned_key = secret_key.replace(" ", "").replace("-", "").replace(":", "")
            
            self.db.twofaaccount.create({
                "name": name.strip(),
                "secret_key": cleaned_key,
                "key_type": key_type
            })
            return True
        except Exception as e:
            print(f"Lỗi khi thêm tài khoản: {e}")
            return False
    
    def delete_account(self, account_id: int) -> bool:
        """Xóa tài khoản theo ID"""
        try:
            self.db.twofaaccount.delete(where={"id": account_id})
            return True
        except Exception as e:
            print(f"Lỗi khi xóa tài khoản: {e}")
            return False
    
    def get_accounts(self) -> List[Dict]:
        """Lấy tất cả tài khoản"""
        try:
            accounts = self.db.twofaaccount.find_many(order={"created_at": "desc"})
            return [self._convert_to_dict(account) for account in accounts]
        except Exception as e:
            print(f"Lỗi khi lấy danh sách tài khoản: {e}")
            return []
    
    def search_accounts(self, query: str) -> List[Dict]:
        """Tìm kiếm tài khoản theo tên"""
        try:
            query = query.lower()
            accounts = self.db.twofaaccount.find_many(
                where={"name": {"contains": query, "mode": "insensitive"}},
                order={"created_at": "desc"}
            )
            return [self._convert_to_dict(account) for account in accounts]
        except Exception as e:
            print(f"Lỗi khi tìm kiếm tài khoản: {e}")
            return []
    
    def get_totp_code(self, secret_key: str) -> str:
        """Tạo mã TOTP từ secret key"""
        try:
            totp = pyotp.TOTP(secret_key)
            return totp.now()
        except Exception as e:
            print(f"Lỗi khi tạo mã TOTP: {e}")
            return "ERROR"
    
    def get_remaining_time(self) -> int:
        """Lấy thời gian còn lại cho mã hiện tại (giây)"""
        return 30 - (datetime.now().second % 30)
    
    def _convert_to_dict(self, account) -> Dict:
        """Chuyển đổi Prisma model thành dictionary"""
        return {
            "id": account.id,
            "name": account.name,
            "secret_key": account.secret_key,
            "key_type": account.key_type,
            "created_at": account.created_at.isoformat() if account.created_at else None,
            "updated_at": account.updated_at.isoformat() if account.updated_at else None
        }
    
    def get_account(self, account_id: int) -> Optional[Dict]:
        """Lấy thông tin tài khoản theo ID"""
        try:
            account = self.db.twofaaccount.find_unique(where={"id": account_id})
            if account:
                return self._convert_to_dict(account)
            return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin tài khoản: {e}")
            return None
    
    def update_account(self, account_id: int, data: Dict) -> bool:
        """Cập nhật thông tin tài khoản"""
        try:
            update_data = {}
            if "name" in data:
                update_data["name"] = data["name"].strip()
            if "key_type" in data:
                update_data["key_type"] = data["key_type"]
            if "secret_key" in data and data["secret_key"].strip():
                # Loại bỏ khoảng trắng và ký tự đặc biệt từ secret key
                cleaned_key = data["secret_key"].replace(" ", "").replace("-", "").replace(":", "")
                update_data["secret_key"] = cleaned_key
            
            if update_data:
                self.db.twofaaccount.update(
                    where={"id": account_id},
                    data=update_data
                )
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật tài khoản: {e}")
            return False 