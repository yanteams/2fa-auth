from models.twofa_model import TwoFAModel
from typing import List, Dict, Tuple
import pyperclip

class TwoFAController:
    def __init__(self):
        self.model = TwoFAModel()
    
    def add_new_account(self, name: str, secret_key: str, key_type: str = "TOTP") -> Tuple[bool, str]:
        """Thêm tài khoản mới"""
        if not name.strip():
            return False, "Tên tài khoản không được để trống"
        
        if not secret_key.strip():
            return False, "Khóa bí mật không được để trống"
        
        success = self.model.add_account(name.strip(), secret_key.strip(), key_type)
        if success:
            return True, "Thêm tài khoản thành công"
        else:
            return False, "Khóa bí mật không hợp lệ"
    
    def get_all_accounts(self) -> List[Dict]:
        """Lấy tất cả tài khoản"""
        return self.model.get_accounts()
    
    def search_accounts(self, query: str) -> List[Dict]:
        """Tìm kiếm tài khoản"""
        if not query.strip():
            return self.get_all_accounts()
        return self.model.search_accounts(query)
    
    def get_account_with_code(self, account: Dict) -> Dict:
        """Lấy thông tin tài khoản kèm mã TOTP hiện tại"""
        account_copy = account.copy()
        account_copy["current_code"] = self.model.get_totp_code(account["secret_key"])
        account_copy["remaining_time"] = self.model.get_remaining_time()
        return account_copy
    
    def get_all_accounts_with_codes(self) -> List[Dict]:
        """Lấy tất cả tài khoản kèm mã TOTP"""
        accounts = self.get_all_accounts()
        return [self.get_account_with_code(account) for account in accounts]
    
    def delete_account(self, account_id: int) -> Tuple[bool, str]:
        """Xóa tài khoản"""
        success = self.model.delete_account(account_id)
        if success:
            return True, "Xóa tài khoản thành công"
        else:
            return False, "Không tìm thấy tài khoản để xóa"
    
    def copy_secret_key(self, secret_key: str) -> bool:
        """Copy secret key vào clipboard"""
        try:
            pyperclip.copy(secret_key)
            return True
        except Exception as e:
            print(f"Lỗi khi copy secret key: {e}")
            return False
    
    def copy_totp_code(self, secret_key: str) -> bool:
        """Copy mã TOTP vào clipboard"""
        try:
            code = self.model.get_totp_code(secret_key)
            if code != "ERROR":
                pyperclip.copy(code)
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi copy mã TOTP: {e}")
            return False
    
    def get_remaining_time(self) -> int:
        """Lấy thời gian còn lại"""
        return self.model.get_remaining_time() 