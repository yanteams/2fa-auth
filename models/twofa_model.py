from prisma import Prisma
from typing import List, Dict, Optional
import pyotp
from datetime import datetime
import config

class TwoFAModel:
    def __init__(self):
        self.db = Prisma()
        self.db.connect()
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()
    
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
                "secretKey": cleaned_key,
                "keyType": key_type
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
            accounts = self.db.twofaaccount.find_many(order={"createdAt": "desc"})
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
                order={"createdAt": "desc"}
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
            "secret_key": account.secretKey,
            "key_type": account.keyType,
            "created_at": account.createdAt.isoformat() if account.createdAt else None,
            "updated_at": account.updatedAt.isoformat() if account.updatedAt else None
        } 