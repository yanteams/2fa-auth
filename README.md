# 2FA Authenticator - Ứng dụng quản lý mã xác thực

Ứng dụng Python với PyQt5 và Prisma để quản lý mã 2FA tương tự Google Authenticator với giao diện hiện đại và z-index cao.

## Tính năng

- ✅ Giao diện PyQt5 hiện đại với z-index cao (luôn hiển thị trên cùng)
- ✅ Thêm tài khoản 2FA mới với tên, khóa bí mật và loại khóa
- ✅ Hiển thị danh sách tài khoản với mã TOTP 6 số
- ✅ Đếm ngược thời gian còn lại cho mã hiện tại (cập nhật real-time)
- ✅ Tìm kiếm tài khoản theo tên
- ✅ Copy mã 6 số vào clipboard
- ✅ Copy khóa bí mật vào clipboard
- ✅ Xóa tài khoản
- ✅ Lưu trữ dữ liệu với PostgreSQL và Prisma
- ✅ Thread riêng biệt để cập nhật mã và thời gian
- ✅ Cấu hình database qua file .env

## Cài đặt

1. Cài đặt Python 3.8+ nếu chưa có
2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

3. Thiết lập môi trường:

```bash
# Tạo file .env từ env_example.txt
python setup_env.py

# Tạo database và bảng
python create_database.py

# Thiết lập Prisma
python setup_prisma.py

# Kiểm tra kết nối
python test_connection.py
```

## Chạy ứng dụng

```bash
python main.py
```

## Cấu hình .env

Tạo file `.env` với các thông tin sau:

```env
DATABASE_URL="postgresql://username:password@host:port/database_name"
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## Cách sử dụng

### Thêm tài khoản mới

1. Nhập tên tài khoản (ví dụ: "Gmail", "Facebook", "GitHub")
2. Nhập khóa bí mật (secret key) từ dịch vụ
3. Chọn loại khóa (TOTP hoặc HOTP)
4. Nhấn "➕ Thêm tài khoản"

### Sử dụng mã 2FA

- Mã 6 số sẽ tự động cập nhật mỗi 30 giây
- Nhấn "📋 Copy mã" để copy mã hiện tại vào clipboard
- Nhấn "🔑 Copy khóa" để copy khóa bí mật vào clipboard
- Nhấn "🗑️ Xóa" để xóa tài khoản

### Tìm kiếm

- Nhập tên tài khoản vào ô tìm kiếm để lọc danh sách

## Cấu trúc dự án

```
2FAAuth App/
├── models/
│   └── twofa_model.py      # Model quản lý dữ liệu với Prisma
├── controllers/
│   └── twofa_controller.py # Controller xử lý logic
├── views/
│   └── main_view.py        # Giao diện PyQt5 hiện đại
├── prisma/
│   └── schema.prisma       # Schema database
├── main.py                 # File khởi chạy
├── config.py              # Cấu hình database từ .env
├── create_database.py     # Script tạo database
├── setup_env.py           # Script tạo file .env
├── setup_prisma.py        # Script thiết lập Prisma
├── test_connection.py     # Script kiểm tra kết nối
├── env_example.txt        # Mẫu file .env
├── requirements.txt        # Thư viện cần thiết
└── README.md              # Hướng dẫn sử dụng
```

## Tính năng giao diện

- **Z-index cao**: Cửa sổ luôn hiển thị trên cùng
- **Giao diện hiện đại**: Thiết kế Material Design với màu sắc và hiệu ứng
- **Responsive**: Tự động điều chỉnh kích thước
- **Splitter layout**: Chia màn hình thành 2 panel
- **Real-time updates**: Cập nhật mã và thời gian mỗi giây
- **Thread-safe**: Sử dụng QThread để cập nhật không block UI

## Khắc phục lỗi

### Lỗi Prisma.connect()
```bash
# Chạy lại setup Prisma
python setup_prisma.py
```

### Lỗi bảng không tồn tại
```bash
# Tạo lại database và bảng
python create_database.py
```

### Lỗi kết nối database
```bash
# Kiểm tra kết nối
python test_connection.py
```

### Lỗi Prisma client
```bash
# Tạo lại Prisma client
prisma generate
```

## Lưu ý bảo mật

- Dữ liệu tài khoản được lưu trong PostgreSQL database
- Khóa bí mật được mã hóa và chỉ hiển thị khi cần thiết
- Nên bảo vệ thông tin database trong file .env
- Ứng dụng có z-index cao nên cần cẩn thận khi sử dụng

## Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. Python version (yêu cầu 3.8+)
2. Các thư viện đã được cài đặt đầy đủ
3. File .env đã được tạo và cấu hình đúng
4. Kết nối database PostgreSQL
5. Bảng twofa_accounts đã được tạo
6. Prisma client đã được generate
7. Quyền ghi file trong thư mục chạy ứng dụng

## Yêu cầu hệ thống

- Python 3.8+
- PostgreSQL database
- PyQt5
- Prisma
- pyotp
- pyperclip
- psycopg2-binary 