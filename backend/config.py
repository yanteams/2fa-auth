#!/usr/bin/env python3
"""
Cấu hình mặc định cho 2FA Authenticator
Sử dụng khi không có file .env (PRODUCTION mode)
"""

import os
from pathlib import Path

# Deployment Mode
DEPLOY = os.getenv("DEPLOY", "PRODUCTION").upper()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://yancoder_auth:CkzKRWRGAETAwpTt@173.249.199.28:5432/yancoder_auth",
)

# Database Connection Details
DB_HOST = os.getenv("DB_HOST", "173.249.199.28")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "yancoder_auth")
DB_USER = os.getenv("DB_USER", "yancoder_auth")
DB_PASSWORD = os.getenv("DB_PASSWORD", "CkzKRWRGAETAwpTt")

# Application Settings
APP_NAME = os.getenv("APP_NAME", "2FA Authenticator")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Security Settings
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "caiconcac")

# UI Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# TOTP Settings
TOTP_DIGITS = 6
TOTP_PERIOD = 30  # seconds

# File Paths
BASE_DIR = Path(__file__).parent
PRISMA_DIR = BASE_DIR / "prisma"
SCHEMA_FILE = PRISMA_DIR / "schema.prisma"


def get_database_url():
    """Lấy DATABASE_URL theo môi trường"""
    if DEPLOY == "LOCAL":
        return "file:./dev.db"
    else:
        return DATABASE_URL


def is_production():
    """Kiểm tra có phải môi trường production không"""
    return DEPLOY == "PRODUCTION"


def is_local():
    """Kiểm tra có phải môi trường local không"""
    return DEPLOY == "LOCAL"


def get_deploy_info():
    """Lấy thông tin deploy"""
    return {
        "mode": DEPLOY,
        "database_url": get_database_url(),
        "is_production": is_production(),
        "is_local": is_local(),
    }
