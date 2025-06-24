import os
import shutil

def setup_env():
    """Tạo file .env từ env_example.txt nếu chưa tồn tại"""
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            shutil.copy('env_example.txt', '.env')
            print("✅ Đã tạo file .env từ env_example.txt")
        else:
            print("❌ Không tìm thấy file env_example.txt")
            return False
    else:
        print("ℹ️ File .env đã tồn tại")
    
    return True

if __name__ == "__main__":
    setup_env() 