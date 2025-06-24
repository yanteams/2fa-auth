import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from views.main_view import TwoFAView

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Hàm chính để khởi chạy ứng dụng"""
    try:
        # Tạo ứng dụng PyQt5
        app = QApplication(sys.argv)
        
        # Thiết lập thông tin ứng dụng
        app.setApplicationName("2FA Authenticator")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("2FA App")
        
        # Thiết lập style toàn cục
        app.setStyle('Fusion')
        
        # Tạo cửa sổ chính
        window = TwoFAView()
        window.show()
        
        # Chạy ứng dụng
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Lỗi khi khởi chạy ứng dụng: {e}")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main() 