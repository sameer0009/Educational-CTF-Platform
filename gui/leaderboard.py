from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class LeaderboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Leaderboard")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #f1f3f5;
                border: 1px solid #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: none;
            }
            QTableWidget {
                border: none;
                background: white;
                gridline-color: #e9ecef;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            QHeaderView::section {
                background: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e9ecef;
                font-weight: bold;
                color: #495057;
            }
            QPushButton {
                background: #228be6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1c7ed6;
            }
            QPushButton:pressed {
                background: #1971c2;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        header_layout = QHBoxLayout()
        
        title = QLabel("Leaderboard")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setStyleSheet("color: #1a1a1a;")
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        header.setLayout(header_layout)
        layout.addWidget(header)
        
        # Tabs
        self.tab_widget = QTabWidget()
        
        # Global leaderboard tab
        global_tab = QWidget()
        global_layout = QVBoxLayout()
        self.global_table = QTableWidget()
        self.global_table.setColumnCount(4)
        self.global_table.setHorizontalHeaderLabels(["Rank", "Username", "Score", "Challenges Solved"])
        self.global_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.global_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: white;
            }
            QTableWidget::item {
                padding: 12px;
            }
        """)
        global_layout.addWidget(self.global_table)
        global_tab.setLayout(global_layout)
        
        # Category leaderboard tab
        category_tab = QWidget()
        category_layout = QVBoxLayout()
        self.category_table = QTableWidget()
        self.category_table.setColumnCount(4)
        self.category_table.setHorizontalHeaderLabels(["Rank", "Username", "Category", "Score"])
        self.category_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        category_layout.addWidget(self.category_table)
        category_tab.setLayout(category_layout)
        
        # User stats tab
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(3)
        self.stats_table.setHorizontalHeaderLabels(["Category", "Challenges Solved", "Score"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        stats_layout.addWidget(self.stats_table)
        stats_tab.setLayout(stats_layout)
        
        self.tab_widget.addTab(global_tab, "Global Rankings")
        self.tab_widget.addTab(category_tab, "Category Rankings")
        self.tab_widget.addTab(stats_tab, "Your Statistics")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
    def update_leaderboards(self, username):
        # Update global leaderboard
        global_rankings = self.parent.db.get_global_rankings()
        self.global_table.setRowCount(len(global_rankings))
        for i, (rank, user, score, solved) in enumerate(global_rankings):
            self.global_table.setItem(i, 0, QTableWidgetItem(str(rank)))
            self.global_table.setItem(i, 1, QTableWidgetItem(user))
            self.global_table.setItem(i, 2, QTableWidgetItem(str(score)))
            self.global_table.setItem(i, 3, QTableWidgetItem(str(solved)))
            
            # Highlight current user
            if user == username:
                for j in range(4):
                    item = self.global_table.item(i, j)
                    item.setBackground(QColor("#e7f5ff"))
                    item.setForeground(QColor("#228be6"))
        
        # Update category leaderboard
        category_rankings = self.parent.db.get_category_rankings()
        self.category_table.setRowCount(len(category_rankings))
        for i, (rank, user, category, score) in enumerate(category_rankings):
            self.category_table.setItem(i, 0, QTableWidgetItem(str(rank)))
            self.category_table.setItem(i, 1, QTableWidgetItem(user))
            self.category_table.setItem(i, 2, QTableWidgetItem(category))
            self.category_table.setItem(i, 3, QTableWidgetItem(str(score)))
            
            # Highlight current user
            if user == username:
                for j in range(4):
                    item = self.category_table.item(i, j)
                    item.setBackground(QColor("#e7f5ff"))
                    item.setForeground(QColor("#228be6"))
        
        # Update user statistics
        user_stats = self.parent.db.get_user_statistics(username)
        self.stats_table.setRowCount(len(user_stats))
        for i, (category, solved, score) in enumerate(user_stats):
            self.stats_table.setItem(i, 0, QTableWidgetItem(category))
            self.stats_table.setItem(i, 1, QTableWidgetItem(str(solved)))
            self.stats_table.setItem(i, 2, QTableWidgetItem(str(score)))
            
            # Highlight rows with solved challenges
            if solved > 0:
                for j in range(3):
                    item = self.stats_table.item(i, j)
                    item.setBackground(QColor("#e7f5ff"))
                    item.setForeground(QColor("#228be6")) 