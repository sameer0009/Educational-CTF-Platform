from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QMessageBox, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import bcrypt

# Custom styles (Dark Theme)
STYLES = {
    'main': """
        QWidget {
            background-color: #1e1e1e;
            color: #cccccc;
            font-family: 'Segoe UI', Arial;
        }
        QFrame {
            background: white;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
        }
        QLabel {
            color: #cccccc;
        }
        QLineEdit {
            padding: 8px;
            border: 1px solid #4a4a4a;
            border-radius: 6px;
            background: #333333;
            color: #cccccc;
        }
        QLineEdit:focus {
            border: 2px solid #0078d4;
        }
        QPushButton {
            background: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #005a9e;
        }
        QPushButton:pressed {
            background: #004578;
        }
    """
}

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(STYLES['main'])
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        title_label = QLabel('CTF Platform Login')
        title_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        
        register_button = QPushButton('Register')
        register_button.clicked.connect(self.register)
        
        layout.addWidget(title_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        
        self.setLayout(layout)
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if self.parent.db.verify_user(username, password):
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.parent.show_dashboard(username)
            self.hide()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')
            
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return
            
        if self.parent.db.user_exists(username):
            QMessageBox.warning(self, 'Error', 'Username already exists')
        else:
            self.parent.db.add_user(username, password)
            QMessageBox.information(self, 'Success', 'Registration successful! You can now log in.')
            self.username_input.clear()
            self.password_input.clear() 