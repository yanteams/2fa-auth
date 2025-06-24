import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFrame, QScrollArea,
                             QGridLayout, QCheckBox, QSplitter, QTextEdit,
                             QToolButton, QMenu, QAction, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QMutex
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
import time
from datetime import datetime

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.twofa_controller import TwoFAController

class UpdateWorker(QThread):
    """Worker thread để cập nhật mã và thời gian"""
    update_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.mutex = QMutex()
        self.update_interval = 1.0  # 1 giây
    
    def run(self):
        """Chạy worker thread"""
        while self.running:
            try:
                self.mutex.lock()
                if self.running:
                    self.update_signal.emit()
                self.mutex.unlock()
                
                # Sleep với interval có thể điều chỉnh
                time.sleep(self.update_interval)
            except Exception as e:
                self.error_signal.emit(f"Lỗi cập nhật: {str(e)}")
                time.sleep(2)  # Đợi lâu hơn nếu có lỗi
    
    def stop(self):
        """Dừng worker thread"""
        self.mutex.lock()
        self.running = False
        self.mutex.unlock()
        self.wait()  # Đợi thread kết thúc
    
    def set_update_interval(self, interval):
        """Thiết lập interval cập nhật"""
        self.update_interval = interval

class DataWorker(QThread):
    """Worker thread để load dữ liệu từ database"""
    data_loaded = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    
    def __init__(self, controller, search_query=""):
        super().__init__()
        self.controller = controller
        self.search_query = search_query
    
    def run(self):
        """Load dữ liệu trong background"""
        try:
            if self.search_query:
                accounts = self.controller.search_accounts(self.search_query)
            else:
                accounts = self.controller.get_all_accounts()
            
            # Thêm mã TOTP cho mỗi account
            accounts_with_codes = []
            for account in accounts:
                account_with_code = self.controller.get_account_with_code(account)
                accounts_with_codes.append(account_with_code)
            
            self.data_loaded.emit(accounts_with_codes)
        except Exception as e:
            self.error_signal.emit(f"Lỗi load dữ liệu: {str(e)}")

class ModernButton(QPushButton):
    """Nút hiện đại với hiệu ứng hover"""
    def __init__(self, text, color="#4CAF50", hover_color="#45a049", icon_text=""):
        super().__init__(text)
        self.color = color
        self.hover_color = hover_color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-height: 32px;
                text-align: center;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 1px solid #2e7d32;
            }}
            QPushButton:pressed {{
                background-color: #3d8b40;
                border: 1px solid #1b5e20;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)

class ActionButton(QToolButton):
    """Nút thao tác hiện đại với menu dropdown"""
    def __init__(self, text, icon_text, color="#4CAF50", hover_color="#45a049"):
        super().__init__()
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setPopupMode(QToolButton.InstantPopup)
        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-height: 32px;
                min-width: 85px;
                text-align: center;
                margin: 2px;
            }}
            QToolButton:hover {{
                background-color: {hover_color};
                border: 1px solid #2e7d32;
            }}
            QToolButton:pressed {{
                background-color: #3d8b40;
                border: 1px solid #1b5e20;
            }}
            QToolButton::menu-button {{
                border: none;
                width: 12px;
            }}
            QToolButton:disabled {{
                background-color: #cccccc;
                color: #666666;
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

class AutoCloseMessageBox(QMessageBox):
    """MessageBox tự động đóng sau 3 giây"""
    def __init__(self, title, message, icon=QMessageBox.Information):
        super().__init__(icon, title, message)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Timer để tự động đóng
        self.timer = QTimer()
        self.timer.timeout.connect(self.accept)
        self.timer.start(3000)  # 3000ms = 3 giây
        
        # Hiển thị message box
        self.show()

class EditAccountDialog(QDialog):
    """Dialog chỉnh sửa tài khoản"""
    def __init__(self, parent=None, account_data=None):
        super().__init__(parent)
        self.account_data = account_data
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("✏️ Chỉnh sửa tài khoản")
        self.setFixedSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tiêu đề
        title_label = QLabel("✏️ Chỉnh sửa tài khoản")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                text-align: center;
            }
        """)
        layout.addWidget(title_label)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Tên tài khoản
        self.name_input = ModernLineEdit()
        if self.account_data:
            self.name_input.setText(self.account_data.get("name", ""))
        form_layout.addRow("📱 Tên tài khoản:", self.name_input)
        
        # Loại khóa
        self.key_type_combo = ModernComboBox()
        self.key_type_combo.addItems(["TOTP", "HOTP"])
        if self.account_data:
            current_type = self.account_data.get("key_type", "TOTP")
            index = self.key_type_combo.findText(current_type)
            if index >= 0:
                self.key_type_combo.setCurrentIndex(index)
        form_layout.addRow("🔐 Loại khóa:", self.key_type_combo)
        
        # Ghi chú
        self.note_input = QTextEdit()
        self.note_input.setMaximumHeight(80)
        self.note_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #4CAF50;
            }
        """)
        if self.account_data:
            self.note_input.setPlainText(self.account_data.get("note", ""))
        form_layout.addRow("📝 Ghi chú:", self.note_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = ModernButton("❌ Hủy", "#6c757d", "#5a6268")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = ModernButton("💾 Lưu thay đổi", "#4CAF50", "#45a049")
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            "name": self.name_input.text().strip(),
            "key_type": self.key_type_combo.currentText(),
            "note": self.note_input.toPlainText().strip()
        }

class TwoFAView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = TwoFAController()
        
        # Khởi tạo workers
        self.update_worker = UpdateWorker()
        self.data_worker = None
        
        # Cache dữ liệu để tránh load lại
        self.cached_accounts = []
        self.is_updating = False
        
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
                border-radius: 12px;
                border: 2px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header với tìm kiếm và thống kê
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-radius: 10px;
                border: 1px solid #dee2e6;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(15)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tiêu đề và thống kê
        title_layout = QHBoxLayout()
        
        panel_title = QLabel("📱 Danh sách tài khoản 2FA")
        panel_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        title_layout.addWidget(panel_title)
        
        title_layout.addStretch()
        
        # Thống kê
        self.stats_label = QLabel("Tổng: 0 tài khoản")
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #6c757d;
                padding: 8px 15px;
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        title_layout.addWidget(self.stats_label)
        
        header_layout.addLayout(title_layout)
        
        # Tìm kiếm
        search_layout = QHBoxLayout()
        
        search_label = QLabel("🔍 Tìm kiếm:")
        search_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                color: #495057;
                font-size: 14px;
            }
        """)
        search_layout.addWidget(search_label)
        
        self.search_input = ModernLineEdit("Nhập tên tài khoản để tìm kiếm...")
        self.search_input.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        
        # Nút làm mới
        refresh_btn = ModernButton("🔄 Làm mới", "#17a2b8", "#138496")
        refresh_btn.setFixedSize(100, 35)
        refresh_btn.clicked.connect(lambda: self.update_accounts_table())
        search_layout.addWidget(refresh_btn)
        
        header_layout.addLayout(search_layout)
        layout.addWidget(header_frame)
        
        # Bảng tài khoản với styling nâng cao
        self.accounts_table = QTableWidget()
        self.accounts_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                background-color: white;
                gridline-color: #f8f9fa;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }
            QTableWidget::item {
                padding: 15px 10px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: bold;
            }
            QTableWidget::item:hover {
                background-color: #f5f5f5;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                padding: 15px 10px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                border-right: 1px solid #dee2e6;
                font-weight: bold;
                color: #495057;
                font-size: 13px;
                text-align: center;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e9ecef, stop:1 #dee2e6);
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #adb5bd;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6c757d;
            }
        """)
        
        # Thiết lập cột với thông tin chi tiết hơn
        self.accounts_table.setColumnCount(7)
        self.accounts_table.setHorizontalHeaderLabels([
            "📱 Tên tài khoản", "🔢 Mã", "⏱️ Thời gian", 
            "🔐 Loại khóa", "📅 Ngày tạo", "⚡ Thao tác", ""
        ])
        
        # Cấu hình header
        header = self.accounts_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Tên
        header.setSectionResizeMode(1, QHeaderView.Fixed)    # Mã
        header.setSectionResizeMode(2, QHeaderView.Fixed)    # Thời gian
        header.setSectionResizeMode(3, QHeaderView.Fixed)    # Loại
        header.setSectionResizeMode(4, QHeaderView.Fixed)    # Ngày tạo
        header.setSectionResizeMode(5, QHeaderView.Fixed)    # Thao tác
        header.setSectionResizeMode(6, QHeaderView.Fixed)    # Ẩn
        
        self.accounts_table.setColumnWidth(1, 130)  # Mã
        self.accounts_table.setColumnWidth(2, 130)  # Thời gian
        self.accounts_table.setColumnWidth(3, 100)  # Loại
        self.accounts_table.setColumnWidth(4, 120)  # Ngày tạo
        self.accounts_table.setColumnWidth(5, 250)  # Thao tác (giảm vì dùng icon)
        self.accounts_table.setColumnWidth(6, 0)    # Ẩn
        
        # Ẩn header dọc
        self.accounts_table.verticalHeader().setVisible(False)
        
        # Bật alternating row colors
        self.accounts_table.setAlternatingRowColors(True)
        
        # Thiết lập selection mode
        self.accounts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.accounts_table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(self.accounts_table)
        
        # Footer với thông tin bổ sung
        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(15, 10, 15, 10)
        
        info_label = QLabel("💡 Mẹo: Click chuột phải vào hàng để mở menu thao tác")
        info_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-style: italic;
            }
        """)
        footer_layout.addWidget(info_label)
        
        footer_layout.addStretch()
        
        # Thời gian cập nhật
        self.update_time_label = QLabel("Cập nhật lần cuối: --")
        self.update_time_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
            }
        """)
        footer_layout.addWidget(self.update_time_label)
        
        layout.addWidget(footer_frame)
        
        # Cập nhật danh sách ban đầu
        self.update_accounts_table()
        
        # Thiết lập context menu cho table
        self.accounts_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.accounts_table.customContextMenuRequested.connect(self.show_context_menu)
        
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
            AutoCloseMessageBox("Thành công", message)
            self.name_input.clear()
            self.secret_input.clear()
            self.update_accounts_table()
        else:
            AutoCloseMessageBox("Lỗi", message, QMessageBox.Critical)
    
    def on_search(self):
        """Xử lý tìm kiếm với threading"""
        query = self.search_input.text()
        self.load_accounts_data(query)
    
    def load_accounts_data(self, search_query=""):
        """Load dữ liệu tài khoản với threading"""
        if self.is_updating:
            return  # Tránh load nhiều lần cùng lúc
        
        self.is_updating = True
        
        # Dừng worker cũ nếu đang chạy
        if self.data_worker and self.data_worker.isRunning():
            self.data_worker.quit()
            self.data_worker.wait()
        
        # Tạo worker mới
        self.data_worker = DataWorker(self.controller, search_query)
        self.data_worker.data_loaded.connect(self.update_accounts_table_finished)
        self.data_worker.error_signal.connect(self.handle_data_error)
        self.data_worker.finished.connect(lambda: setattr(self, 'is_updating', False))
        
        # Bắt đầu load dữ liệu
        self.data_worker.start()
    
    def update_accounts_table(self, search_query=""):
        """Cập nhật bảng tài khoản (deprecated - sử dụng load_accounts_data)"""
        self.load_accounts_data(search_query)
    
    def update_accounts_table_finished(self, accounts_with_codes):
        """Callback khi load dữ liệu hoàn thành"""
        try:
            # Cập nhật cache
            self.cached_accounts = accounts_with_codes
            
            # Cập nhật thống kê
            self.stats_label.setText(f"Tổng: {len(accounts_with_codes)} tài khoản")
            
            # Cập nhật thời gian cập nhật
            current_time = datetime.now().strftime("%H:%M:%S")
            self.update_time_label.setText(f"Cập nhật lần cuối: {current_time}")
            
            # Cập nhật số hàng
            self.accounts_table.setRowCount(len(accounts_with_codes))
            
            # Thêm dữ liệu vào bảng
            for row, account in enumerate(accounts_with_codes):
                self._populate_table_row(row, account)
                
        except Exception as e:
            print(f"Lỗi khi cập nhật bảng: {e}")
    
    def _populate_table_row(self, row, account):
        """Populate một hàng trong bảng"""
        try:
            # Tên tài khoản với styling đặc biệt
            name_item = QTableWidgetItem(account["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            name_font = QFont()
            name_font.setBold(True)
            name_font.setPointSize(12)
            name_item.setFont(name_font)
            name_item.setForeground(QColor("#2c3e50"))
            self.accounts_table.setItem(row, 0, name_item)
            
            # Mã 6 số với styling nổi bật
            code_item = QTableWidgetItem(account["current_code"])
            code_item.setFlags(code_item.flags() & ~Qt.ItemIsEditable)
            code_item.setTextAlignment(Qt.AlignCenter)
            code_font = QFont()
            code_font.setBold(True)
            code_font.setPointSize(16)
            code_font.setFamily("Courier New")
            code_item.setFont(code_font)
            code_item.setForeground(QColor("#28a745"))
            code_item.setBackground(QColor("#f8fff9"))
            self.accounts_table.setItem(row, 1, code_item)
            
            # Thời gian còn lại với màu sắc động
            remaining_time = account['remaining_time']
            time_text = f"{remaining_time}s"
            time_item = QTableWidgetItem(time_text)
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            time_item.setTextAlignment(Qt.AlignCenter)
            time_font = QFont()
            time_font.setBold(True)
            time_font.setPointSize(12)
            time_item.setFont(time_font)
            
            # Màu sắc theo thời gian còn lại
            if remaining_time <= 5:
                time_item.setForeground(QColor("#dc3545"))  # Đỏ
                time_item.setBackground(QColor("#fff5f5"))
            elif remaining_time <= 10:
                time_item.setForeground(QColor("#fd7e14"))  # Cam
                time_item.setBackground(QColor("#fff8f0"))
            else:
                time_item.setForeground(QColor("#28a745"))  # Xanh
                time_item.setBackground(QColor("#f8fff9"))
            
            self.accounts_table.setItem(row, 2, time_item)
            
            # Loại khóa với badge styling
            type_item = QTableWidgetItem(account["key_type"])
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            type_item.setTextAlignment(Qt.AlignCenter)
            type_font = QFont()
            type_font.setBold(True)
            type_item.setFont(type_font)
            
            if account["key_type"] == "TOTP":
                type_item.setForeground(QColor("#007bff"))
                type_item.setBackground(QColor("#f0f8ff"))
            else:
                type_item.setForeground(QColor("#6f42c1"))
                type_item.setBackground(QColor("#f8f5ff"))
            
            self.accounts_table.setItem(row, 3, type_item)
            
            # Ngày tạo
            if account.get("created_at"):
                try:
                    if isinstance(account["created_at"], str):
                        created_date = datetime.fromisoformat(account["created_at"].replace('Z', '+00:00'))
                    else:
                        created_date = account["created_at"]
                    date_text = created_date.strftime("%d/%m/%Y")
                except:
                    date_text = "N/A"
            else:
                date_text = "N/A"
            
            date_item = QTableWidgetItem(date_text)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setForeground(QColor("#6c757d"))
            self.accounts_table.setItem(row, 4, date_item)
            
            # Cột thao tác - hiển thị icon menu
            action_item = QTableWidgetItem("⚙️")
            action_item.setFlags(action_item.flags() & ~Qt.ItemIsEditable)
            action_item.setTextAlignment(Qt.AlignCenter)
            action_item.setToolTip("Click chuột phải để mở menu thao tác")
            
            # Thiết lập màu nền cho cột thao tác
            action_item.setBackground(QColor("#f8f9fa"))
            action_item.setForeground(QColor("#6c757d"))
            
            # Lưu account data vào item để sử dụng trong context menu
            action_item.setData(Qt.UserRole, account)
            
            self.accounts_table.setItem(row, 5, action_item)
            
        except Exception as e:
            print(f"Lỗi khi populate row {row}: {e}")
    
    def copy_code(self, secret_key):
        """Copy mã TOTP"""
        if self.controller.copy_totp_code(secret_key):
            AutoCloseMessageBox("Thành công", "Đã copy mã vào clipboard")
        else:
            AutoCloseMessageBox("Lỗi", "Không thể copy mã", QMessageBox.Critical)
    
    def copy_key(self, secret_key):
        """Copy secret key"""
        if self.controller.copy_secret_key(secret_key):
            AutoCloseMessageBox("Thành công", "Đã copy khóa vào clipboard")
        else:
            AutoCloseMessageBox("Lỗi", "Không thể copy khóa", QMessageBox.Critical)
    
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
                AutoCloseMessageBox("Thành công", message)
                self.update_accounts_table()
            else:
                AutoCloseMessageBox("Lỗi", message, QMessageBox.Critical)
    
    def edit_account(self, account_id):
        """Chỉnh sửa tài khoản"""
        account_data = self.controller.get_account(account_id)
        dialog = EditAccountDialog(self, account_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            success, message = self.controller.update_account(account_id, data)
            if success:
                AutoCloseMessageBox("Thành công", message)
                self.update_accounts_table()
            else:
                AutoCloseMessageBox("Lỗi", message, QMessageBox.Critical)
    
    def export_key(self, secret_key):
        """Xuất khóa"""
        AutoCloseMessageBox("Thông báo", "Tính năng xuất khóa sẽ được phát triển sau", QMessageBox.Information)
    
    def start_update_thread(self):
        """Bắt đầu thread cập nhật với threading hiệu quả"""
        # Kết nối signals
        self.update_worker.update_signal.connect(self.refresh_codes_only)
        self.update_worker.error_signal.connect(self.handle_update_error)
        
        # Thiết lập interval cập nhật
        self.update_worker.set_update_interval(1.0)  # 1 giây
        
        # Bắt đầu worker
        self.update_worker.start()
        
        # Load dữ liệu ban đầu
        self.load_accounts_data()
    
    def refresh_codes_only(self):
        """Chỉ cập nhật mã và thời gian, không load lại toàn bộ dữ liệu"""
        try:
            if not self.cached_accounts:
                return
            
            # Cập nhật mã và thời gian cho các hàng hiện tại
            for row in range(self.accounts_table.rowCount()):
                if row < len(self.cached_accounts):
                    account = self.cached_accounts[row]
                    account_with_code = self.controller.get_account_with_code(account)
                    
                    # Cập nhật mã
                    code_item = self.accounts_table.item(row, 1)
                    if code_item:
                        code_item.setText(account_with_code["current_code"])
                    
                    # Cập nhật thời gian
                    time_item = self.accounts_table.item(row, 2)
                    if time_item:
                        remaining_time = account_with_code['remaining_time']
                        time_item.setText(f"{remaining_time}s")
                        
                        # Cập nhật màu sắc theo thời gian
                        if remaining_time <= 5:
                            time_item.setForeground(QColor("#dc3545"))
                            time_item.setBackground(QColor("#fff5f5"))
                        elif remaining_time <= 10:
                            time_item.setForeground(QColor("#fd7e14"))
                            time_item.setBackground(QColor("#fff8f0"))
                        else:
                            time_item.setForeground(QColor("#28a745"))
                            time_item.setBackground(QColor("#f8fff9"))
                            
        except Exception as e:
            print(f"Lỗi khi refresh codes: {e}")
    
    def handle_update_error(self, error_message):
        """Xử lý lỗi khi cập nhật"""
        print(f"Lỗi cập nhật: {error_message}")
    
    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng với cleanup đầy đủ"""
        try:
            # Dừng update worker
            if hasattr(self, 'update_worker'):
                self.update_worker.stop()
            
            # Dừng data worker nếu đang chạy
            if hasattr(self, 'data_worker') and self.data_worker and self.data_worker.isRunning():
                self.data_worker.quit()
                self.data_worker.wait()
            
            # Đợi tất cả threads kết thúc
            if hasattr(self, 'update_worker'):
                self.update_worker.wait()
            
            print("Đã đóng ứng dụng an toàn")
            event.accept()
        except Exception as e:
            print(f"Lỗi khi đóng ứng dụng: {e}")
            event.accept()
    
    def handle_data_error(self, error_message):
        """Xử lý lỗi khi load dữ liệu"""
        print(f"Lỗi load dữ liệu: {error_message}")
        self.is_updating = False
    
    def show_context_menu(self, position):
        """Hiển thị context menu khi click chuột phải"""
        try:
            # Lấy item được click
            item = self.accounts_table.itemAt(position)
            if not item:
                return
            
            # Lấy row của item
            row = item.row()
            if row < 0 or row >= len(self.cached_accounts):
                return
            
            # Lấy account data
            account = self.cached_accounts[row]
            
            # Tạo context menu
            context_menu = QMenu(self)
            context_menu.setStyleSheet("""
                QMenu {
                    background-color: white;
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 12px;
                }
                QMenu::item {
                    padding: 10px 20px;
                    border-radius: 6px;
                    margin: 2px;
                }
                QMenu::item:selected {
                    background-color: #e3f2fd;
                    color: #1976d2;
                    font-weight: bold;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #dee2e6;
                    margin: 5px 0px;
                }
            """)
            
            # Thêm các action
            copy_code_action = QAction("📋 Copy mã 6 số", self)
            copy_code_action.triggered.connect(lambda: self.copy_code(account["secret_key"]))
            context_menu.addAction(copy_code_action)
            
            copy_key_action = QAction("🔑 Copy secret key", self)
            copy_key_action.triggered.connect(lambda: self.copy_key(account["secret_key"]))
            context_menu.addAction(copy_key_action)
            
            context_menu.addSeparator()
            
            edit_action = QAction("✏️ Chỉnh sửa tài khoản", self)
            edit_action.triggered.connect(lambda: self.edit_account(account["id"]))
            context_menu.addAction(edit_action)
            
            context_menu.addSeparator()
            
            export_action = QAction("📤 Xuất secret key", self)
            export_action.triggered.connect(lambda: self.export_key(account["secret_key"]))
            context_menu.addAction(export_action)
            
            context_menu.addSeparator()
            
            delete_action = QAction("🗑️ Xóa tài khoản", self)
            delete_action.triggered.connect(lambda: self.delete_account(account["id"]))
            context_menu.addAction(delete_action)
            
            # Hiển thị menu tại vị trí click
            context_menu.exec_(self.accounts_table.mapToGlobal(position))
            
        except Exception as e:
            print(f"Lỗi khi hiển thị context menu: {e}") 