import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFrame, QScrollArea,
                             QGridLayout, QCheckBox, QSplitter, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from controllers.twofa_controller import TwoFAController
import time

class UpdateThread(QThread):
    """Thread để cập nhật mã và thời gian"""
    update_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        while self.running:
            self.update_signal.emit()
            time.sleep(1)
    
    def stop(self):
        self.running = False

class ModernButton(QPushButton):
    """Nút hiện đại với hiệu ứng hover"""
    def __init__(self, text, color="#4CAF50", hover_color="#45a049"):
        super().__init__(text)
        self.color = color
        self.hover_color = hover_color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: #3d8b40;
            }}
        """)

class ModernLineEdit(QLineEdit):
    """Input hiện đại"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

class ModernComboBox(QComboBox):
    """ComboBox hiện đại"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
        """)

class TwoFAView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = TwoFAController()
        self.update_thread = UpdateThread()
        self.init_ui()
        self.start_update_thread()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("2FA Authenticator - Quản lý mã xác thực")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Thiết lập style cho cửa sổ chính
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)
        
        # Widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tiêu đề
        self.create_title(main_layout)
        
        # Splitter cho layout chính
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel bên trái - Thêm tài khoản
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panel bên phải - Danh sách tài khoản
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Tỷ lệ splitter
        splitter.setSizes([400, 800])
        
        # Thiết lập z-index cao
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
    
    def create_title(self, layout):
        """Tạo tiêu đề"""
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #4CAF50, stop:1 #45a049);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("🔐 2FA Authenticator")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("Quản lý mã xác thực hai yếu tố")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                text-align: center;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addWidget(title_frame)
    
    def create_left_panel(self):
        """Tạo panel bên trái - Form thêm tài khoản"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tiêu đề panel
        panel_title = QLabel("➕ Thêm tài khoản mới")
        panel_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                padding-bottom: 10px;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        layout.addWidget(panel_title)
        
        # Form thêm tài khoản
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        
        # Tên tài khoản
        form_layout.addWidget(QLabel("Tên tài khoản:"), 0, 0)
        self.name_input = ModernLineEdit("Ví dụ: Gmail, Facebook, GitHub")
        form_layout.addWidget(self.name_input, 0, 1)
        
        # Khóa bí mật
        form_layout.addWidget(QLabel("Khóa bí mật:"), 1, 0)
        self.secret_input = ModernLineEdit("Nhập secret key từ dịch vụ")
        self.secret_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.secret_input, 1, 1)
        
        # Checkbox hiển thị khóa
        self.show_secret_cb = QCheckBox("Hiển thị khóa")
        self.show_secret_cb.toggled.connect(self.toggle_secret_visibility)
        form_layout.addWidget(self.show_secret_cb, 1, 2)
        
        # Loại khóa
        form_layout.addWidget(QLabel("Loại khóa:"), 2, 0)
        self.key_type_combo = ModernComboBox()
        self.key_type_combo.addItems(["TOTP", "HOTP"])
        form_layout.addWidget(self.key_type_combo, 2, 1)
        
        # Nút thêm
        add_button = ModernButton("➕ Thêm tài khoản", "#2196F3", "#1976D2")
        add_button.clicked.connect(self.add_account)
        add_button.setMinimumHeight(45)
        form_layout.addWidget(add_button, 3, 0, 1, 3)
        
        layout.addLayout(form_layout)
        
        # Thông tin hướng dẫn
        info_text = QTextEdit()
        info_text.setMaximumHeight(150)
        info_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: #f9f9f9;
                font-size: 12px;
            }
        """)
        info_text.setPlainText("""
📋 Hướng dẫn:
• Tên tài khoản: Đặt tên dễ nhớ (VD: Gmail, Facebook)
• Khóa bí mật: Lấy từ dịch vụ khi bật 2FA
• TOTP: Mã thay đổi theo thời gian (30s)
• HOTP: Mã thay đổi theo số lần sử dụng
        """)
        info_text.setReadOnly(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return panel
    
    def create_right_panel(self):
        """Tạo panel bên phải - Danh sách tài khoản"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header với tìm kiếm
        header_layout = QHBoxLayout()
        
        panel_title = QLabel("📱 Danh sách tài khoản")
        panel_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
        """)
        header_layout.addWidget(panel_title)
        
        header_layout.addStretch()
        
        # Tìm kiếm
        search_label = QLabel("🔍 Tìm kiếm:")
        search_label.setStyleSheet("font-weight: bold; color: #666;")
        header_layout.addWidget(search_label)
        
        self.search_input = ModernLineEdit("Nhập tên tài khoản...")
        self.search_input.textChanged.connect(self.on_search)
        header_layout.addWidget(self.search_input)
        
        layout.addLayout(header_layout)
        
        # Bảng tài khoản
        self.accounts_table = QTableWidget()
        self.accounts_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #333;
            }
        """)
        
        # Thiết lập cột
        self.accounts_table.setColumnCount(6)
        self.accounts_table.setHorizontalHeaderLabels([
            "Tên tài khoản", "Mã 6 số", "Thời gian", "Loại", "Thao tác", ""
        ])
        
        # Cấu hình header
        header = self.accounts_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Tên
        header.setSectionResizeMode(1, QHeaderView.Fixed)    # Mã
        header.setSectionResizeMode(2, QHeaderView.Fixed)    # Thời gian
        header.setSectionResizeMode(3, QHeaderView.Fixed)    # Loại
        header.setSectionResizeMode(4, QHeaderView.Fixed)    # Thao tác
        header.setSectionResizeMode(5, QHeaderView.Fixed)    # Ẩn
        
        self.accounts_table.setColumnWidth(1, 120)  # Mã
        self.accounts_table.setColumnWidth(2, 100)  # Thời gian
        self.accounts_table.setColumnWidth(3, 80)   # Loại
        self.accounts_table.setColumnWidth(4, 200)  # Thao tác
        self.accounts_table.setColumnWidth(5, 0)    # Ẩn
        
        # Ẩn header dọc
        self.accounts_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.accounts_table)
        
        # Cập nhật danh sách ban đầu
        self.update_accounts_table()
        
        return panel
    
    def toggle_secret_visibility(self, checked):
        """Chuyển đổi hiển thị/ẩn khóa bí mật"""
        if checked:
            self.secret_input.setEchoMode(QLineEdit.Normal)
        else:
            self.secret_input.setEchoMode(QLineEdit.Password)
    
    def add_account(self):
        """Thêm tài khoản mới"""
        name = self.name_input.text().strip()
        secret = self.secret_input.text().strip()
        key_type = self.key_type_combo.currentText()
        
        success, message = self.controller.add_new_account(name, secret, key_type)
        
        if success:
            QMessageBox.information(self, "Thành công", message)
            self.name_input.clear()
            self.secret_input.clear()
            self.update_accounts_table()
        else:
            QMessageBox.critical(self, "Lỗi", message)
    
    def on_search(self):
        """Xử lý tìm kiếm"""
        query = self.search_input.text()
        self.update_accounts_table(query)
    
    def update_accounts_table(self, search_query=""):
        """Cập nhật bảng tài khoản"""
        # Lấy danh sách tài khoản
        if search_query:
            accounts = self.controller.search_accounts(search_query)
        else:
            accounts = self.controller.get_all_accounts()
        
        # Cập nhật số hàng
        self.accounts_table.setRowCount(len(accounts))
        
        # Thêm dữ liệu vào bảng
        for row, account in enumerate(accounts):
            account_with_code = self.controller.get_account_with_code(account)
            
            # Tên tài khoản
            name_item = QTableWidgetItem(account["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.accounts_table.setItem(row, 0, name_item)
            
            # Mã 6 số
            code_item = QTableWidgetItem(account_with_code["current_code"])
            code_item.setFlags(code_item.flags() & ~Qt.ItemIsEditable)
            code_item.setTextAlignment(Qt.AlignCenter)
            code_item.setStyleSheet("font-weight: bold; font-size: 16px; color: #4CAF50;")
            self.accounts_table.setItem(row, 1, code_item)
            
            # Thời gian còn lại
            time_item = QTableWidgetItem(f"{account_with_code['remaining_time']}s")
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            time_item.setTextAlignment(Qt.AlignCenter)
            time_item.setStyleSheet("font-weight: bold; color: #FF9800;")
            self.accounts_table.setItem(row, 2, time_item)
            
            # Loại khóa
            type_item = QTableWidgetItem(account["key_type"])
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            type_item.setTextAlignment(Qt.AlignCenter)
            self.accounts_table.setItem(row, 3, type_item)
            
            # Nút thao tác
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 5, 5, 5)
            actions_layout.setSpacing(5)
            
            # Nút copy mã
            copy_code_btn = ModernButton("📋 Copy mã", "#4CAF50", "#45a049")
            copy_code_btn.setFixedSize(80, 30)
            copy_code_btn.clicked.connect(
                lambda checked, sk=account["secret_key"]: self.copy_code(sk)
            )
            actions_layout.addWidget(copy_code_btn)
            
            # Nút copy khóa
            copy_key_btn = ModernButton("🔑 Copy khóa", "#2196F3", "#1976D2")
            copy_key_btn.setFixedSize(80, 30)
            copy_key_btn.clicked.connect(
                lambda checked, sk=account["secret_key"]: self.copy_key(sk)
            )
            actions_layout.addWidget(copy_key_btn)
            
            # Nút xóa
            delete_btn = ModernButton("🗑️ Xóa", "#f44336", "#d32f2f")
            delete_btn.setFixedSize(60, 30)
            delete_btn.clicked.connect(
                lambda checked, aid=account["id"]: self.delete_account(aid)
            )
            actions_layout.addWidget(delete_btn)
            
            actions_layout.addStretch()
            self.accounts_table.setCellWidget(row, 4, actions_widget)
    
    def copy_code(self, secret_key):
        """Copy mã TOTP"""
        if self.controller.copy_totp_code(secret_key):
            QMessageBox.information(self, "Thành công", "Đã copy mã vào clipboard")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể copy mã")
    
    def copy_key(self, secret_key):
        """Copy secret key"""
        if self.controller.copy_secret_key(secret_key):
            QMessageBox.information(self, "Thành công", "Đã copy khóa vào clipboard")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể copy khóa")
    
    def delete_account(self, account_id):
        """Xóa tài khoản"""
        reply = QMessageBox.question(
            self, "Xác nhận", 
            "Bạn có chắc muốn xóa tài khoản này?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.controller.delete_account(account_id)
            if success:
                QMessageBox.information(self, "Thành công", message)
                self.update_accounts_table()
            else:
                QMessageBox.critical(self, "Lỗi", message)
    
    def start_update_thread(self):
        """Bắt đầu thread cập nhật"""
        self.update_thread.update_signal.connect(self.update_accounts_table)
        self.update_thread.start()
    
    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng"""
        self.update_thread.stop()
        self.update_thread.wait()
        event.accept() 