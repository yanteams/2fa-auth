import os
import sys
from dotenv import load_dotenv

def test_connection():
    """Kiểm tra kết nối database và Prisma"""
    try:
        # Load .env
        load_dotenv()
        
        print("🔍 Kiểm tra cấu hình...")
        
        # Kiểm tra biến môi trường
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            print(f"✅ DATABASE_URL: {database_url[:50]}...")
        else:
            print("❌ DATABASE_URL không được tìm thấy")
            return False
        
        # Kiểm tra Prisma
        print("\n🔧 Kiểm tra Prisma...")
        try:
            from prisma import Prisma
            db = Prisma()
            db.connect()
            print("✅ Kết nối Prisma thành công")
            
            # Kiểm tra bảng
            try:
                accounts = db.twofaaccount.find_many()
                print(f"✅ Bảng twofa_accounts tồn tại, có {len(accounts)} bản ghi")
            except Exception as e:
                print(f"❌ Lỗi khi truy cập bảng: {e}")
                print("💡 Vui lòng chạy: python create_database.py")
                return False
            
            db.disconnect()
            
        except Exception as e:
            print(f"❌ Lỗi kết nối Prisma: {e}")
            print("💡 Vui lòng chạy: python setup_prisma.py")
            return False
        
        print("\n🎉 Tất cả kiểm tra đều thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    test_connection() 