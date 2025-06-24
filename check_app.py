import sys
import os
import warnings

# Ẩn DeprecationWarning từ PyQt5
warnings.filterwarnings("ignore", category=DeprecationWarning, module="PyQt5")

def check_app_status():
    """Kiểm tra trạng thái ứng dụng"""
    print("🔍 Kiểm tra trạng thái ứng dụng 2FA Authenticator...")
    print("=" * 50)
    
    # Kiểm tra Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Kiểm tra các thư viện cần thiết
    required_modules = [
        'PyQt5', 'prisma', 'pyotp', 'pyperclip', 'dotenv'
    ]
    
    print("\n📦 Kiểm tra thư viện:")
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - Chưa cài đặt")
    
    # Kiểm tra file cấu hình
    print("\n📁 Kiểm tra file cấu hình:")
    config_files = [
        '.env', 'env_example.txt', 'config.py', 'requirements.txt'
    ]
    
    for file in config_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Không tồn tại")
    
    # Kiểm tra cấu trúc thư mục
    print("\n📂 Kiểm tra cấu trúc thư mục:")
    directories = [
        'models', 'controllers', 'views', 'prisma'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ - Không tồn tại")
    
    # Kiểm tra file chính
    print("\n📄 Kiểm tra file chính:")
    main_files = [
        'main.py', 'models/twofa_model.py', 'controllers/twofa_controller.py', 
        'views/main_view.py', 'prisma/schema.prisma'
    ]
    
    for file in main_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Không tồn tại")
    
    # Kiểm tra database
    print("\n🗄️ Kiểm tra database:")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            print(f"  ✅ DATABASE_URL: {database_url[:50]}...")
        else:
            print("  ❌ DATABASE_URL không được tìm thấy")
            
    except Exception as e:
        print(f"  ❌ Lỗi khi kiểm tra database: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Kiểm tra hoàn tất!")
    
    # Gợi ý tiếp theo
    print("\n💡 Gợi ý tiếp theo:")
    print("1. Nếu có lỗi, chạy: pip install -r requirements.txt")
    print("2. Tạo database: python create_database.py")
    print("3. Thiết lập Prisma: python setup_prisma.py")
    print("4. Chạy ứng dụng: python main.py")

if __name__ == "__main__":
    check_app_status() 