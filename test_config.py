#!/usr/bin/env python3
"""
Script test hệ thống config mới
Kiểm tra hoạt động với và không có file .env
"""

import os
import sys
import shutil
from pathlib import Path

# Thêm thư mục gốc vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config

def test_config_without_env():
    """Test config khi không có file .env"""
    print("🧪 Test 1: Không có file .env")
    print("-" * 40)
    
    # Backup .env nếu có
    env_backup = None
    if os.path.exists('.env'):
        env_backup = '.env.backup'
        shutil.copy('.env', env_backup)
        os.remove('.env')
        print("📁 Đã backup và xóa file .env")
    
    try:
        # Test config
        deploy_info = config.get_deploy_info()
        print(f"✅ Mode deploy: {deploy_info['mode']}")
        print(f"✅ Database URL: {deploy_info['database_url']}")
        print(f"✅ Is production: {deploy_info['is_production']}")
        print(f"✅ Is local: {deploy_info['is_local']}")
        
        # Test database connection
        from models.twofa_model import TwoFAModel
        model = TwoFAModel()
        accounts = model.get_all_accounts()
        print(f"✅ Database connection: OK ({len(accounts)} accounts)")
        
        print("✅ Test 1 PASSED - Config hoạt động tốt khi không có .env")
        return True
        
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        return False
        
    finally:
        # Restore .env nếu có backup
        if env_backup and os.path.exists(env_backup):
            shutil.copy(env_backup, '.env')
            os.remove(env_backup)
            print("📁 Đã restore file .env")

def test_config_with_env():
    """Test config khi có file .env"""
    print("\n🧪 Test 2: Có file .env")
    print("-" * 40)
    
    # Tạo file .env test
    test_env_content = """DEPLOY=LOCAL
DATABASE_URL="file:./test.db"
APP_NAME="Test App"
APP_VERSION="1.0.0"
ENCRYPTION_KEY="test-key"
"""
    
    with open('.env', 'w') as f:
        f.write(test_env_content)
    
    print("📁 Đã tạo file .env test")
    
    try:
        # Test config
        deploy_info = config.get_deploy_info()
        print(f"✅ Mode deploy: {deploy_info['mode']}")
        print(f"✅ Database URL: {deploy_info['database_url']}")
        print(f"✅ Is production: {deploy_info['is_production']}")
        print(f"✅ Is local: {deploy_info['is_local']}")
        
        print("✅ Test 2 PASSED - Config hoạt động tốt khi có .env")
        return True
        
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        return False
        
    finally:
        # Xóa file .env test
        if os.path.exists('.env'):
            os.remove('.env')
            print("📁 Đã xóa file .env test")

def test_config_priority():
    """Test độ ưu tiên của config"""
    print("\n🧪 Test 3: Độ ưu tiên config")
    print("-" * 40)
    
    # Tạo file .env với LOCAL
    test_env_content = """DEPLOY=LOCAL
DATABASE_URL="file:./test.db"
"""
    
    with open('.env', 'w') as f:
        f.write(test_env_content)
    
    print("📁 Đã tạo file .env với DEPLOY=LOCAL")
    
    try:
        # Test config
        deploy_info = config.get_deploy_info()
        print(f"✅ Mode deploy: {deploy_info['mode']}")
        print(f"✅ Database URL: {deploy_info['database_url']}")
        
        if deploy_info['mode'] == 'LOCAL':
            print("✅ Test 3 PASSED - .env có độ ưu tiên cao hơn config.py")
        else:
            print("❌ Test 3 FAILED - .env không được ưu tiên")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        return False
        
    finally:
        # Xóa file .env test
        if os.path.exists('.env'):
            os.remove('.env')
            print("📁 Đã xóa file .env test")

def main():
    """Hàm chính"""
    print("🔐 2FA Authenticator - Config System Test")
    print("=" * 60)
    
    tests = [
        test_config_without_env,
        test_config_with_env,
        test_config_priority
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Lỗi trong quá trình test: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Kết quả: {passed}/{total} test thành công")
    
    if passed == total:
        print("🎉 Tất cả test đều thành công!")
        print("✅ Hệ thống config hoạt động hoàn hảo")
    else:
        print("⚠️ Có một số test thất bại")
        print("💡 Vui lòng kiểm tra lại cấu hình")

if __name__ == "__main__":
    main() 