# 🔐 2FA Authenticator

Ứng dụng xác thực 2FA hiện đại được xây dựng với PyQt5, Prisma và PostgreSQL. Hỗ trợ cả môi trường phát triển (LOCAL) và triển khai (PRODUCTION).

## ✨ Tính năng

- 🔐 **TOTP Authentication**: Hỗ trợ Google Authenticator, Authy
- 📱 **Modern UI**: Giao diện PyQt5 đẹp mắt và responsive
- 🔍 **Search & Filter**: Tìm kiếm tài khoản nhanh chóng
- 📋 **Copy to Clipboard**: Sao chép mã 2FA một cách dễ dàng
- ⚡ **Real-time Updates**: Cập nhật mã 2FA theo thời gian thực
- 🗄️ **Database Storage**: Lưu trữ an toàn với Prisma + PostgreSQL
- 🌍 **Multi-environment**: Hỗ trợ LOCAL và PRODUCTION
- 🎯 **Context Menu**: Menu chuột phải cho các thao tác
- 🔧 **Edit Accounts**: Chỉnh sửa thông tin tài khoản
- 📦 **System Tray**: Minimize vào system tray
- 🔑 **Secret Key Management**: Quản lý và chỉnh sửa secret key
- ⚙️ **Smart Config**: Tự động sử dụng config mặc định khi không có .env

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd 2FAAuth-App
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Thiết lập môi trường

#### Tự động (Khuyến nghị)
```bash
# Ứng dụng sẽ tự động sử dụng config mặc định (PRODUCTION)
python setup_prisma.py
```

#### Môi trường LOCAL (Phát triển)
```bash
# Tạo file .env
python setup_env.py

# Chỉnh sửa file .env
DEPLOY=LOCAL
DATABASE_URL="file:./dev.db"

# Thiết lập Prisma
python setup_prisma.py
```

#### Môi trường PRODUCTION (Triển khai)
```bash
# Tạo file .env
python setup_env.py

# Chỉnh sửa file .env
DEPLOY=PRODUCTION
DATABASE_URL="postgresql://username:password@host:port/database"

# Thiết lập Prisma
python setup_prisma.py
```

### 4. Kiểm tra trạng thái
```bash
python check_app.py
```

### 5. Chạy ứng dụng
```bash
python main.py
```

## 🌍 Hệ thống Môi trường

### Tự động (Không có .env)
- Sử dụng cấu hình mặc định từ `config.py`
- Mode: PRODUCTION
- Database: PostgreSQL remote
- Phù hợp cho triển khai nhanh

### LOCAL Mode
- Sử dụng Prisma client đã generate
- Database SQLite local
- Phù hợp cho phát triển và testing

### PRODUCTION Mode
- Kết nối trực tiếp đến DATABASE_URL
- Database PostgreSQL remote
- Phù hợp cho triển khai production

## 📁 Cấu trúc Project

```
2FAAuth App/
├── models/              # Data models
│   └── twofa_model.py   # Database operations
├── controllers/         # Business logic
│   └── twofa_controller.py
├── views/              # UI components
│   └── main_view.py    # Main application window
├── prisma/             # Database schema
│   └── schema.prisma
├── main.py             # Application entry point
├── config.py           # Default configuration
├── setup_env.py        # Environment setup
├── setup_prisma.py     # Prisma setup
├── check_app.py        # Status checker
└── requirements.txt    # Dependencies
```

## 🔧 Cấu hình

### File .env (Tùy chọn)
```env
# Deployment Mode
DEPLOY=LOCAL  # hoặc PRODUCTION

# Database Configuration
DATABASE_URL="file:./dev.db"  # LOCAL
# DATABASE_URL="postgresql://..."  # PRODUCTION

# Application Settings
APP_NAME="2FA Authenticator"
APP_VERSION="1.0.0"

# Security
ENCRYPTION_KEY="your-secret-key"
```

### File config.py (Mặc định)
- Sử dụng khi không có file `.env`
- Cấu hình PRODUCTION mặc định
- Có thể chỉnh sửa trực tiếp

## 🎯 Sử dụng

### Thêm tài khoản 2FA
1. Click "Thêm tài khoản"
2. Nhập tên tài khoản
3. Nhập secret key (từ QR code hoặc manual)
4. Click "Lưu"

### Sao chép mã 2FA
- **Copy Code**: Click chuột phải → "Sao chép mã"
- **Copy Key**: Click chuột phải → "Sao chép secret key"

### Chỉnh sửa tài khoản
1. Click chuột phải vào tài khoản
2. Chọn "Chỉnh sửa"
3. Cập nhật thông tin
4. Click "Lưu"

### Tìm kiếm
- Sử dụng ô tìm kiếm để lọc tài khoản theo tên

### System Tray
- Click nút minimize để ẩn vào system tray
- Click chuột phải vào icon tray để mở menu

## 🛠️ Troubleshooting

### Lỗi kết nối database
```bash
# Kiểm tra trạng thái
python check_app.py

# Thiết lập lại Prisma
python setup_prisma.py
```

### Lỗi Prisma client
```bash
# LOCAL mode: Generate client
prisma generate

# PRODUCTION mode: Kiểm tra DATABASE_URL
```

### Lỗi dependencies
```bash
pip install -r requirements.txt
```

### Không có file .env
```bash
# Ứng dụng sẽ tự động sử dụng config mặc định
# Để tùy chỉnh, tạo file .env:
python setup_env.py
```

## 📦 Dependencies

- **PyQt5**: GUI framework
- **Prisma**: Database ORM
- **pyotp**: TOTP implementation
- **pyperclip**: Clipboard operations
- **python-dotenv**: Environment variables

## 🔒 Bảo mật

- Secret keys được mã hóa trong database
- Không lưu trữ mã 2FA, chỉ tính toán real-time
- Hỗ trợ encryption key tùy chỉnh

## 🤝 Đóng góp

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 🆘 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Chạy `python check_app.py` để kiểm tra
2. Xem logs để tìm lỗi
3. Tạo issue với thông tin chi tiết