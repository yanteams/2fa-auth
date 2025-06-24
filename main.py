import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from views.main_view import TwoFAView

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_environment():
    """Thiết lập môi trường trước khi chạy ứng dụng"""
    # Tạo file .env nếu chưa có
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            import shutil
            shutil.copy('env_example.txt', '.env')
            print("✅ Đã tạo file .env từ env_example.txt")
        else:
            print("❌ Không tìm thấy file env_example.txt")
            return False
    
    # Kiểm tra Prisma client
    if not os.path.exists('prisma/__pycache__') and not os.path.exists('prisma/client.py'):
        print("🔧 Thiết lập Prisma...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "-m", "prisma", "generate"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Prisma client đã được tạo")
            else:
                print(f"⚠️ Cảnh báo: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Không thể tạo Prisma client: {e}")
    
    return True

def main():
    """Hàm chính để khởi chạy ứng dụng"""
    try:
        # Thiết lập môi trường
        if not setup_environment():
            print("❌ Không thể thiết lập môi trường")
            input("Nhấn Enter để thoát...")
            return
        
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