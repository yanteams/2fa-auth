import os
import subprocess
import sys

def setup_prisma():
    """Thiết lập Prisma và kiểm tra kết nối"""
    try:
        print("🔧 Thiết lập Prisma...")
        
        # Kiểm tra file .env
        if not os.path.exists('.env'):
            print("❌ File .env không tồn tại. Vui lòng chạy: python setup_env.py")
            return False
        
        # Tạo Prisma client
        print("📦 Tạo Prisma client...")
        result = subprocess.run([sys.executable, "-m", "prisma", "generate"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Prisma client đã được tạo thành công")
        else:
            print(f"❌ Lỗi khi tạo Prisma client: {result.stderr}")
            return False
        
        # Kiểm tra kết nối database
        print("🔍 Kiểm tra kết nối database...")
        result = subprocess.run([sys.executable, "-m", "prisma", "db", "pull"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Kết nối database thành công")
        else:
            print(f"⚠️ Cảnh báo kết nối database: {result.stderr}")
            print("💡 Vui lòng chạy: python create_database.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi thiết lập Prisma: {e}")
        return False

if __name__ == "__main__":
    setup_prisma() 