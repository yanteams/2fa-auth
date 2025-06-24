#!/usr/bin/env python3
"""
Script kiểm tra trạng thái ứng dụng 2FA Authenticator
"""

import os
import sys
from pathlib import Path

# Thêm thư mục gốc vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config

def check_env_file():
    """Kiểm tra file .env"""
    print("🔍 Kiểm tra file .env...")
    
    if not os.path.exists('.env'):
        print("⚠️ File .env không tồn tại!")
        print("💡 Sử dụng cấu hình mặc định từ config.py (PRODUCTION mode)")
        
        # Hiển thị thông tin từ config
        deploy_info = config.get_deploy_info()
        print(f"🌍 Mode deploy: {deploy_info['mode']}")
        
        database_url = deploy_info['database_url']
        if database_url:
            # Ẩn thông tin nhạy cảm
            if 'postgresql://' in database_url:
                parts = database_url.split('@')
                if len(parts) > 1:
                    safe_url = f"postgresql://***:***@{parts[1]}"
                else:
                    safe_url = "postgresql://***:***@***"
            else:
                safe_url = database_url
            print(f"🗄️ Database URL: {safe_url}")
        else:
            print("⚠️ DATABASE_URL chưa được thiết lập")
        
        return False
    
    print("✅ File .env tồn tại")
    
    # Đọc và hiển thị cấu hình
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            config_env = {}
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config_env[key] = value
            
            # Hiển thị thông tin quan trọng
            deploy_mode = config_env.get('DEPLOY', 'LOCAL')
            print(f"🌍 Mode deploy: {deploy_mode}")
            
            database_url = config_env.get('DATABASE_URL', '')
            if database_url:
                # Ẩn thông tin nhạy cảm
                if 'postgresql://' in database_url:
                    parts = database_url.split('@')
                    if len(parts) > 1:
                        safe_url = f"postgresql://***:***@{parts[1]}"
                    else:
                        safe_url = "postgresql://***:***@***"
                else:
                    safe_url = database_url
                print(f"🗄️ Database URL: {safe_url}")
            else:
                print("⚠️ DATABASE_URL chưa được thiết lập")
            
            return True
            
    except Exception as e:
        print(f"❌ Lỗi đọc file .env: {e}")
        return False

def check_prisma_schema():
    """Kiểm tra Prisma schema"""
    print("\n🔍 Kiểm tra Prisma schema...")
    
    schema_file = Path('prisma/schema.prisma')
    if not schema_file.exists():
        print("❌ File prisma/schema.prisma không tồn tại!")
        return False
    
    print("✅ Prisma schema tồn tại")
    return True

def check_database_connection():
    """Kiểm tra kết nối database"""
    print("\n🔍 Kiểm tra kết nối database...")
    
    try:
        from models.twofa_model import TwoFAModel
        
        # Tạo instance để test kết nối
        model = TwoFAModel()
        
        # Test query đơn giản
        accounts = model.get_all_accounts()
        print(f"✅ Kết nối database thành công")
        print(f"📊 Số lượng tài khoản: {len(accounts)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return False

def check_dependencies():
    """Kiểm tra dependencies"""
    print("\n🔍 Kiểm tra dependencies...")
    
    required_packages = [
        'PyQt5',
        'prisma',
        'pyotp',
        'pyperclip'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower())
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Chưa cài đặt")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Cài đặt packages thiếu:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_deployment_mode():
    """Kiểm tra mode deploy"""
    print("\n🔍 Kiểm tra mode deploy...")
    
    deploy_info = config.get_deploy_info()
    deploy_mode = deploy_info['mode']
    
    if deploy_mode == 'LOCAL':
        print("🌍 Mode: LOCAL")
        print("💡 Sử dụng Prisma client đã generate")
        
        # Kiểm tra Prisma client
        try:
            from prisma import Prisma
            db = Prisma()
            db.connect()
            db.disconnect()
            print("✅ Prisma client hoạt động bình thường")
        except Exception as e:
            print(f"❌ Lỗi Prisma client: {e}")
            print("💡 Chạy: python setup_prisma.py")
            return False
            
    elif deploy_mode == 'PRODUCTION':
        print("🚀 Mode: PRODUCTION")
        print("💡 Kết nối trực tiếp đến DATABASE_URL")
        
        database_url = deploy_info['database_url']
        if not database_url:
            print("❌ DATABASE_URL không được thiết lập!")
            return False
        
        print("✅ DATABASE_URL đã được thiết lập")
        print(f"🔗 Database: {database_url.split('@')[1] if '@' in database_url else database_url}")
        
    else:
        print(f"❌ Mode deploy không hợp lệ: {deploy_mode}")
        return False
    
    return True

def main():
    """Hàm chính"""
    print("🔐 2FA Authenticator - Status Check")
    print("=" * 50)
    
    checks = [
        check_env_file,
        check_prisma_schema,
        check_dependencies,
        check_deployment_mode,
        check_database_connection
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"❌ Lỗi trong quá trình kiểm tra: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Kết quả: {passed}/{total} kiểm tra thành công")
    
    if passed == total:
        print("🎉 Tất cả kiểm tra đều thành công!")
        print("🚀 Ứng dụng sẵn sàng chạy: python main.py")
    else:
        print("⚠️ Có một số vấn đề cần khắc phục")
        print("💡 Vui lòng làm theo hướng dẫn ở trên")

if __name__ == "__main__":
    main() 