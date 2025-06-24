#!/usr/bin/env python3
"""
Script thiết lập môi trường cho 2FA Authenticator
"""

import os
import shutil
from pathlib import Path
import sys

# Thêm thư mục gốc vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config

def setup_environment():
    """Thiết lập file .env từ template"""
    print("🔐 2FA Authenticator - Environment Setup")
    print("=" * 50)
    
    # Kiểm tra file .env đã tồn tại
    if os.path.exists('.env'):
        print("⚠️ File .env đã tồn tại!")
        overwrite = input("Bạn có muốn ghi đè không? (y/N): ").lower()
        if overwrite != 'y':
            print("❌ Hủy thiết lập")
            return False
    
    # Kiểm tra file template
    if not os.path.exists('env_example.txt'):
        print("❌ File env_example.txt không tồn tại!")
        return False
    
    try:
        # Copy template
        shutil.copy('env_example.txt', '.env')
        print("✅ Đã tạo file .env từ template")
        
        # Hiển thị thông tin về config mặc định
        print("\n📝 Lưu ý về cấu hình:")
        print("💡 Nếu không có file .env, ứng dụng sẽ sử dụng:")
        print(f"   - Mode deploy: {config.DEPLOY}")
        print(f"   - Database: {config.get_database_url().split('@')[1] if '@' in config.get_database_url() else config.get_database_url()}")
        
        # Hướng dẫn cấu hình
        print("\n📝 Hướng dẫn cấu hình:")
        print("1. Mở file .env và cập nhật các giá trị:")
        print("   - DEPLOY: LOCAL (phát triển) hoặc PRODUCTION (triển khai)")
        print("   - DATABASE_URL: URL kết nối database")
        print("   - ENCRYPTION_KEY: Khóa mã hóa (tạo ngẫu nhiên)")
        
        print("\n2. Chạy thiết lập Prisma:")
        print("   python setup_prisma.py")
        
        print("\n3. Chạy ứng dụng:")
        print("   python main.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo file .env: {e}")
        return False

def main():
    """Hàm chính"""
    success = setup_environment()
    if success:
        print("\n🎉 Thiết lập môi trường hoàn tất!")
        print("📝 Vui lòng chỉnh sửa file .env theo hướng dẫn")
    else:
        print("\n❌ Thiết lập môi trường thất bại!")

if __name__ == "__main__":
    main() 