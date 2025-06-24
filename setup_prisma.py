#!/usr/bin/env python3
"""
Script thiết lập Prisma cho 2FA Authenticator
Hỗ trợ cả môi trường LOCAL và PRODUCTION
"""

import os
import sys
import subprocess
from pathlib import Path

def check_env_file():
    """Kiểm tra file .env"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ File .env không tồn tại!")
        print("📝 Vui lòng tạo file .env từ env_example.txt")
        return False
    return True

def get_deploy_mode():
    """Lấy mode deploy từ .env"""
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DEPLOY='):
                    return line.split('=')[1].strip().upper()
    except Exception as e:
        print(f"❌ Lỗi đọc file .env: {e}")
    
    return 'LOCAL'  # Default

def setup_local_environment():
    """Thiết lập môi trường LOCAL"""
    print("🔧 Thiết lập môi trường LOCAL...")
    
    try:
        # Generate Prisma client
        print("📦 Đang generate Prisma client...")
        result = subprocess.run(['prisma', 'generate'], 
                              capture_output=True, text=True, check=True)
        print("✅ Prisma client đã được generate thành công")
        
        # Push schema to database (optional)
        print("🗄️ Đang push schema đến database...")
        result = subprocess.run(['prisma', 'db', 'push'], 
                              capture_output=True, text=True, check=True)
        print("✅ Schema đã được push thành công")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi generate Prisma client: {e}")
        print(f"📋 Output: {e.stdout}")
        print(f"❌ Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Prisma CLI không được tìm thấy!")
        print("📦 Vui lòng cài đặt Prisma CLI: npm install -g prisma")
        return False

def setup_production_environment():
    """Thiết lập môi trường PRODUCTION"""
    print("🚀 Thiết lập môi trường PRODUCTION...")
    
    # Kiểm tra DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL không được thiết lập!")
        print("📝 Vui lòng thêm DATABASE_URL vào file .env")
        return False
    
    print("✅ DATABASE_URL đã được thiết lập")
    print("🔗 Kết nối trực tiếp đến database production")
    
    try:
        # Chỉ push schema, không generate client
        print("🗄️ Đang push schema đến database production...")
        result = subprocess.run(['prisma', 'db', 'push'], 
                              capture_output=True, text=True, check=True)
        print("✅ Schema đã được push thành công")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi push schema: {e}")
        print(f"📋 Output: {e.stdout}")
        print(f"❌ Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Prisma CLI không được tìm thấy!")
        print("📦 Vui lòng cài đặt Prisma CLI: npm install -g prisma")
        return False

def main():
    """Hàm chính"""
    print("🔐 2FA Authenticator - Prisma Setup")
    print("=" * 50)
    
    # Kiểm tra file .env
    if not check_env_file():
        return False
    
    # Lấy mode deploy
    deploy_mode = get_deploy_mode()
    print(f"🌍 Mode deploy: {deploy_mode}")
    
    # Thiết lập theo mode
    if deploy_mode == 'LOCAL':
        return setup_local_environment()
    elif deploy_mode == 'PRODUCTION':
        return setup_production_environment()
    else:
        print(f"❌ Mode deploy không hợp lệ: {deploy_mode}")
        print("📝 Chỉ hỗ trợ: LOCAL hoặc PRODUCTION")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Thiết lập Prisma hoàn tất!")
        print("🚀 Bạn có thể chạy ứng dụng: python main.py")
    else:
        print("\n❌ Thiết lập Prisma thất bại!")
        sys.exit(1) 