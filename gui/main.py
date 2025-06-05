import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from gui.login import LoginWindow
from gui.dashboard import DashboardWindow
from database.db_manager import DatabaseManager

class CTFPlatform(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Educational CTF Platform")
        self.setMinimumSize(1200, 800)
        
        # Initialize database
        self.db = DatabaseManager()
        self.db.initialize_database()
        
        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize windows
        self.login_window = LoginWindow(self)
        self.dashboard = DashboardWindow(self)
        
        # Add windows to stacked widget
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.dashboard)
        
        # Show login window initially
        self.stacked_widget.setCurrentWidget(self.login_window)
        
        # Connect signals
        self.login_window.login_successful.connect(self.show_dashboard)
        
    def show_dashboard(self, username):
        self.dashboard.set_username(username)
        self.stacked_widget.setCurrentWidget(self.dashboard)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = CTFPlatform()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 