import psycopg2
from psycopg2 import sql
import config

def create_database():
    """Tạo database và bảng twofa_accounts"""
    try:
        # Kết nối đến PostgreSQL server (không chỉ định database cụ thể)
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Tạo database nếu chưa tồn tại
        try:
            cursor.execute(f"CREATE DATABASE {config.DB_NAME}")
            print(f"✅ Đã tạo database '{config.DB_NAME}'")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ℹ️ Database '{config.DB_NAME}' đã tồn tại")
        
        cursor.close()
        conn.close()
        
        # Kết nối đến database cụ thể
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Xóa bảng cũ nếu tồn tại (để tạo lại với cấu trúc mới)
        try:
            cursor.execute("DROP TABLE IF EXISTS twofa_accounts CASCADE;")
            print("🗑️ Đã xóa bảng cũ (nếu có)")
        except Exception as e:
            print(f"ℹ️ Không có bảng cũ để xóa: {e}")
        
        # Tạo bảng twofa_accounts với cấu trúc đúng cho Prisma
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS twofa_accounts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            secret_key VARCHAR(255) NOT NULL,
            key_type VARCHAR(50) DEFAULT 'TOTP',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_sql)
        print("✅ Đã tạo bảng 'twofa_accounts' với cấu trúc mới")
        
        # Tạo index cho tìm kiếm
        try:
            cursor.execute("CREATE INDEX idx_twofa_accounts_name ON twofa_accounts(name);")
            print("✅ Đã tạo index cho cột 'name'")
        except psycopg2.errors.DuplicateTable:
            print("ℹ️ Index đã tồn tại")
        
        # Thêm dữ liệu mẫu (tùy chọn)
        sample_data = [
            ("Gmail", "JBSWY3DPEHPK3PXP", "TOTP"),
            ("GitHub", "JBSWY3DPEHPK3PXP", "TOTP"),
            ("Facebook", "JBSWY3DPEHPK3PXP", "TOTP")
        ]
        
        insert_sql = """
        INSERT INTO twofa_accounts (name, secret_key, key_type) 
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
        """
        
        for name, secret_key, key_type in sample_data:
            cursor.execute(insert_sql, (name, secret_key, key_type))
        
        print("✅ Đã thêm dữ liệu mẫu")
        
        # Kiểm tra bảng đã tạo
        cursor.execute("SELECT COUNT(*) FROM twofa_accounts;")
        count = cursor.fetchone()[0]
        print(f"📊 Số lượng tài khoản trong bảng: {count}")
        
        # Hiển thị cấu trúc bảng
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'twofa_accounts' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print("\n📋 Cấu trúc bảng twofa_accounts:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Khởi tạo database thành công!")
        print("💡 Bây giờ bạn có thể chạy: prisma generate")
        
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo database: {e}")

if __name__ == "__main__":
    create_database() 