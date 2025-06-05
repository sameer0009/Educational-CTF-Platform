import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QScrollArea, QFrame,
                             QLineEdit, QMessageBox, QComboBox, QSpacerItem, 
                             QSizePolicy, QSplitter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QFontDatabase
from gui.leaderboard import LeaderboardWindow

# Custom styles (Dark Theme - Professional Look)
STYLES = {
    'dark': {
        'main': """
            QWidget {
                background-color: #2b2b2b; /* Deep Dark Gray */
                color: #cccccc; /* Light Gray Text */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #4a4a4a; /* Medium Dark Border */
                border-radius: 8px;
                background: #3c3c3c; /* Slightly Lighter Dark */
            }
            QTabBar::tab {
                background: #4a4a4a; /* Medium Dark */
                color: #cccccc; /* Light Gray */
                border: 1px solid #5a5a5a; /* Lighter Border */
                padding: 10px 20px; /* Increased Padding */
                margin-right: 4px; /* Increased Margin */
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                min-width: 100px; /* Minimum Tab Width */
            }
            QTabBar::tab:selected {
                background: #3c3c3c; /* Matches Pane */
                color: #ffffff; /* White Text */
                border-bottom-color: #3c3c3c; /* Hide Bottom Border */
                font-weight: bold;
            }
            QTabBar::tab:hover {
                 background: #555555; /* Hover effect */
            }
            QPushButton {
                background: #007acc; /* VS Code Blue */
                color: white; /* White Text */
                border: none;
                padding: 10px 20px; /* Increased Padding */
                border-radius: 5px; /* Rounded Corners */
                font-weight: bold;
                text-transform: uppercase; /* Uppercase Text */
            }
            QPushButton:hover {
                background: #005f99; /* Darker Blue on Hover */
            }
            QPushButton:pressed {
                background: #004b80; /* Even Darker Blue on Press */
            }
            QLineEdit {
                padding: 10px; /* Increased Padding */
                border: 1px solid #5a5a5a; /* Lighter Border */
                border-radius: 5px; /* Rounded Corners */
                background: #3c3c3c; /* Matches Pane */
                color: #cccccc; /* Light Gray Text */
            }
            QLineEdit:focus {
                border: 2px solid #007acc; /* Highlight on Focus */
                background: #4a4a4a; /* Slightly darker on focus */
            }
             QComboBox {
                padding: 10px; /* Increased Padding */
                border: 1px solid #5a5a5a; /* Lighter Border */
                border-radius: 5px; /* Rounded Corners */
                background: #3c3c3c; /* Matches Pane */
                color: #cccccc; /* Light Gray Text */
             }
             QComboBox::drop-down {
                border: none;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
             }
              QComboBox::down-arrow {
                 image: url(down_arrow_dark.png); /* Placeholder for a custom dark arrow icon */
                 width: 16px;
                 height: 16px;
             }
             QComboBox:focus {
                 border: 2px solid #007acc;
             }
             QMessageBox {
                 background-color: #3c3c3c;
                 color: #cccccc;
                 font-size: 14px;
             }
             QMessageBox QLabel {
                 color: #cccccc;
             }
             QMessageBox QPushButton {
                 min-width: 80px;
             }

        """,
        'header': """
            QFrame {
                background: #3c3c3c; /* Slightly Lighter Dark */
                border-bottom: 1px solid #4a4a4a; /* Medium Dark Border */
                padding: 15px 20px; /* Increased Padding */
            }
            QLabel {
                color: #ffffff; /* White Text */
                font-size: 18px; /* Increased Font Size */
                font-weight: bold;
            }
        """,
        'challenge_card': """
            QFrame {
                background: #3c3c3c; /* Slightly Lighter Dark */
                border: 1px solid #4a4a4a; /* Medium Dark Border */
                border-radius: 8px; /* Slightly Less Rounded */
                padding: 20px; /* Consistent Padding */
                margin: 8px; /* Reduced Margin */
            }
            QFrame:hover {
                border: 1px solid #007acc; /* Highlight Border on Hover */
                background: #4a4a4a; /* Darker on Hover */
            }
            QLabel {
                color: #cccccc; /* Light Gray Text */
            }
        """,
        'filter_frame': """
            QFrame {
                background: #3c3c3c; /* Slightly Lighter Dark */
                border-radius: 5px; /* Rounded Corners */
                padding: 15px; /* Increased Padding */
                 border: 1px solid #4a4a4a; /* Medium Dark Border */
            }
            QLabel {
               color: #cccccc; /* Light Gray Text */
               font-weight: normal;
            }
             QComboBox {
                padding: 8px; /* Standard Padding */
                border: 1px solid #5a5a5a; /* Lighter Border */
                border-radius: 4px; /* Slightly Less Rounded */
                background: #4a4a4a; /* Darker Background */
                color: #cccccc; /* Light Gray Text */
            }
        """
    },
     'light': { # Basic Light Theme for toggling
        'main': "",
        'header': "",
        'challenge_card': "",
        'filter_frame': "",
     }
}

class ChallengeCard(QFrame):
    def __init__(self, challenge_data, parent=None):
        super().__init__(parent)
        self.challenge_data = challenge_data
        # print(f"[DEBUG] Creating ChallengeCard for: {self.challenge_data[1]}") # Debug print
        self.init_ui()
        # print(f"[DEBUG] ChallengeCard initialized for '{self.challenge_data[1]}'. SizeHint: {self.sizeHint()}, MinimumSize: {self.minimumSize()}, Visible: {self.isVisible()}") # Debug print
        
    def init_ui(self):
        # Apply initial theme based on parent's dark_mode state
        if self.parent() and hasattr(self.parent(), 'dark_mode') and self.parent().dark_mode:
             self.setStyleSheet(STYLES['dark']['challenge_card'])
        else:
             # Use a basic default style if light mode or parent is not available
             self.setStyleSheet("")

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        
        # Title and points
        title_layout = QHBoxLayout()
        title = QLabel(self.challenge_data[1])
        title.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title.setStyleSheet("color: #007acc;") # VS Code Blue for title
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title.setMinimumWidth(1)
        title.setWordWrap(True)
        
        points = QLabel(f"{self.challenge_data[5]} pts")
        points.setStyleSheet("""
            background: #007acc; /* VS Code Blue */
            color: white;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 10px; /* Slightly more rounded */
        """)
        points.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(points)
        layout.addLayout(title_layout)
        
        # Category and difficulty
        info_layout = QHBoxLayout()
        category = QLabel(self.challenge_data[2])
        category.setStyleSheet("""
            background: #5a5a5a; /* Lighter Gray */
            color: white;
            padding: 4px 12px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: bold;
        """)
        category.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        difficulty = QLabel(self.challenge_data[6])
        difficulty.setStyleSheet("""
            background: #5a5a5a; /* Lighter Gray */
            color: white;
            padding: 4px 12px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: bold;
        """)
        difficulty.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        info_layout.addWidget(category)
        info_layout.addWidget(difficulty)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Description
        description = QLabel(self.challenge_data[3])
        description.setWordWrap(True)
        description.setStyleSheet("""
            color: #cccccc; /* Light Gray */
            font-size: 13px;
            line-height: 1.5; /* Note: line-height is not standard in Qt CSS */
            padding: 8px 0;
        """)
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(description)
        
        # Flag submission
        flag_layout = QHBoxLayout()
        self.flag_input = QLineEdit()
        self.flag_input.setPlaceholderText("Enter flag here...")
        self.flag_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Apply theme-specific styles to flag input
        # Using parent's dark_mode property check
        if self.parent() and hasattr(self.parent(), 'dark_mode') and self.parent().dark_mode:
            self.flag_input.setStyleSheet(STYLES['dark']['main'].split('QLineEdit')[1].split('QComboBox')[0]) # Apply dark LineEdit style
        else:
             self.flag_input.setStyleSheet("") # Default light style
        
        submit_button = QPushButton("Submit Flag")
        submit_button.setStyleSheet("""
            QPushButton {
                background: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #005f99;
            }
            QPushButton:pressed {
                background: #004b80;
            }
        """)
        submit_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        submit_button.clicked.connect(self.submit_flag)
        
        flag_layout.addWidget(self.flag_input)
        flag_layout.addWidget(submit_button)
        layout.addLayout(flag_layout)
        
        self.setLayout(layout)
        
    def submit_flag(self):
        flag = self.flag_input.text()
        main_window = self.window()
        if main_window and hasattr(main_window, 'verify_flag') and hasattr(main_window, 'mark_challenge_solved') and hasattr(main_window, 'username') and hasattr(main_window, 'update_score_display'):
            if main_window.verify_flag(self.challenge_data[0], flag):
                QMessageBox.information(self, "Success", "🎉 Correct flag! Challenge solved!")
                main_window.mark_challenge_solved(
                    main_window.username,
                    self.challenge_data[0]
                )
                main_window.update_score_display()
            else:
                QMessageBox.warning(self, "Error", "❌ Incorrect flag. Try again!")
        else:
             QMessageBox.warning(self, "Error", "Application not fully initialized.")

class DashboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.username = ""
        self.leaderboard_window = None
        self.dark_mode = True # Start in dark mode
        self.challenges_layouts = {} # Dictionary to store challenge layouts, scroll areas, and content widgets for each category
        
        # Create tab widget first
        self.tab_widget = QTabWidget()
        
        # Now initialize UI
        self.init_ui()
        
    def init_ui(self):
        # Create header elements early
        self.user_info = QLabel()
        self.user_info.setFont(QFont('Segoe UI', 12))

        self.score_label = QLabel("Score: 0")
        self.score_label.setFont(QFont('Segoe UI', 12, QFont.Bold))

        self.mode_btn = QPushButton("☀️ Light Mode") # Initial button text reflects the mode it switches to
        self.mode_btn.setCheckable(True)
        self.mode_btn.setChecked(False) # Initially unchecked because it's for switching to Light Mode
        self.mode_btn.clicked.connect(self.toggle_mode)

        # Create the content frame
        self.content = QFrame()
        self.content.setObjectName("content")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Create category tabs and challenge areas
        categories = ["All", "Web", "Crypto", "Reversing", "Forensics", "Misc"]
        for category in categories:
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(0, 0, 0, 0)
            tab_layout.setSpacing(12)
            
            # Filter controls
            filter_frame = QFrame()
            filter_frame.setObjectName(f"filter_frame_{category}")
            filter_layout = QHBoxLayout(filter_frame)
            filter_layout.setContentsMargins(12, 12, 12, 12)
            
            filter_label = QLabel("Difficulty:")
            filter_label.setStyleSheet("font-weight: bold;")
            
            difficulty_filter = QComboBox()
            difficulty_filter.addItems(["All Difficulties", "Easy", "Medium", "Hard"])
            difficulty_filter.currentTextChanged.connect(
                lambda text, cat=category: self.filter_challenges(cat, text)
            )
            
            filter_layout.addWidget(filter_label)
            filter_layout.addWidget(difficulty_filter)
            filter_layout.addStretch()
            tab_layout.addWidget(filter_frame)
            
            # Challenges scroll area
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background: transparent; /* Background will be handled by content_widget */
                }
                QScrollArea > QWidget > QWidget { /* Style for the scroll area's viewport widget */
                     background-color: #3c3c3c; /* Match tab pane background */
                     border-radius: 8px; /* Match tab pane border radius */
                }
            """)
            scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # Widget to hold the challenges layout within the scroll area
            scroll_content = QWidget()
            scroll_content.setObjectName(f"scroll_content_{category}")
            # scroll_content.setMinimumHeight(400) # Removed fixed minimum height, let layout decide

            challenges_layout = QVBoxLayout(scroll_content) # Set layout directly on scroll_content
            challenges_layout.setSpacing(12)
            challenges_layout.setAlignment(Qt.AlignTop)
            challenges_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
            # Removed scroll_content.setLayout(challenges_layout) as it's set in the constructor

            # Store layout, scroll area, and content widget
            self.challenges_layouts[category] = {
                'layout': challenges_layout,
                'scroll': scroll,
                'content_widget': scroll_content
            }

            scroll.setWidget(scroll_content)
            tab_layout.addWidget(scroll)
            self.tab_widget.addTab(tab, category)

        # Set initial theme (Dark Mode)
        self.apply_dark_mode()

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(20)
        header_layout.setAlignment(Qt.AlignVCenter)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_label = QLabel("🛡️") # Use a QLabel for the logo
        logo_label.setFont(QFont('Segoe UI', 24))
        logo_label.setAlignment(Qt.AlignCenter)
        # Apply header text color to logo label
        if self.dark_mode:
             logo_label.setStyleSheet(STYLES['dark']['header'].split('QLabel')[1].split('}')[0] + '}')
        else:
             logo_label.setStyleSheet(STYLES['light']['header'].split('QLabel')[1].split('}')[0] + '}')

        title_label = QLabel("CTF Platform") # Use a QLabel for the title
        title_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
         # Apply header text color to title label
        if self.dark_mode:
             title_label.setStyleSheet(STYLES['dark']['header'].split('QLabel')[1].split('}')[0] + '}')
        else:
             title_label.setStyleSheet(STYLES['light']['header'].split('QLabel')[1].split('}')[0] + '}')

        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(title_label)
        logo_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # User info, score, and buttons layout
        user_score_btn_layout = QHBoxLayout()
        user_score_btn_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.user_info.setStyleSheet(STYLES['dark']['header'].split('QLabel')[1].split('}')[0] + '}') # Apply header text color
        self.score_label.setStyleSheet(STYLES['dark']['header'].split('QLabel')[1].split('}')[0] + '}') # Apply header text color

        leaderboard_btn = QPushButton("📊 Leaderboard")
        leaderboard_btn.clicked.connect(self.show_leaderboard)

        user_score_btn_layout.addWidget(self.user_info)
        user_score_btn_layout.addSpacing(20) # Add spacing between user info and score
        user_score_btn_layout.addWidget(self.score_label)
        user_score_btn_layout.addSpacing(20) # Add spacing between score and buttons
        user_score_btn_layout.addWidget(leaderboard_btn)
        user_score_btn_layout.addWidget(self.mode_btn)

        # Add components to header layout
        header_layout.addLayout(logo_layout)
        header_layout.addStretch(1)
        header_layout.addLayout(user_score_btn_layout)
        
        self.layout.addWidget(header)
        content_layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.content)
        
        self.setLayout(self.layout)

    def set_username(self, username):
        self.username = username
        self.user_info.setText(f"Welcome, {username}!")
        self.load_challenges()

    def load_challenges(self):
        categories = ["All", "Web", "Crypto", "Reversing", "Forensics", "Misc"]

        # Clear challenges from all layouts first
        for category in categories:
            layout_info = self.challenges_layouts.get(category)
            if layout_info and 'layout' in layout_info:
                challenges_layout = layout_info['layout']
                # Remove widgets from the layout
                while challenges_layout.count():
                    item = challenges_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                    elif item.spacerItem():
                        challenges_layout.removeItem(item.spacerItem())

        # Load challenges for each category tab
        for category in categories:
            layout_info = self.challenges_layouts.get(category)
            if layout_info and 'layout' in layout_info and 'scroll' in layout_info and 'content_widget' in layout_info:
                challenges_layout = layout_info['layout']
                scroll_area = layout_info['scroll']
                scroll_content = layout_info['content_widget']

                if category == "All":
                    challenges = self.parent.db.get_challenges()
                else:
                    challenges = self.parent.db.get_challenges(category)

                # Add challenges to the layout
                for challenge in challenges:
                    card = ChallengeCard(challenge, self)
                    challenges_layout.addWidget(card)

                # Add a stretch to push challenges to the top
                challenges_layout.addStretch(1)
                
                # Explicitly update the layout and scroll area content
                challenges_layout.update()
                scroll_content.update()
                scroll_content.adjustSize()
                scroll_area.update()
                scroll_area.adjustSize()

        self.update_score_display()
        
    def filter_challenges(self, category, difficulty):
        layout_info = self.challenges_layouts.get(category)
        if layout_info and 'layout' in layout_info and 'scroll' in layout_info and 'content_widget' in layout_info:
            challenges_layout = layout_info['layout']
            scroll_area = layout_info['scroll']
            scroll_content = layout_info['content_widget']

            # Remove widgets from the layout
            while challenges_layout.count():
                item = challenges_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.spacerItem():
                    challenges_layout.removeItem(item.spacerItem())

            # Get challenges for the category
            if category == "All":
                challenges = self.parent.db.get_challenges()
            else:
                challenges = self.parent.db.get_challenges(category)

            # Filter by difficulty if needed
            if difficulty != "All Difficulties":
                challenges = [c for c in challenges if c[6] == difficulty]

            # Add filtered challenges to the layout
            for challenge in challenges:
                card = ChallengeCard(challenge, self)
                challenges_layout.addWidget(card)

            # Add a stretch to push challenges to the top
            challenges_layout.addStretch(1)

            # Explicitly update the layout and scroll area content
            challenges_layout.update()
            scroll_content.update()
            scroll_content.adjustSize()
            scroll_area.update()
            scroll_area.adjustSize()

    def update_score_display(self):
        score = self.parent.db.get_user_score(self.username)
        self.score_label.setText(f"Score: {score}")
        
    def show_leaderboard(self):
        if self.leaderboard_window is None:
            self.leaderboard_window = LeaderboardWindow(self.parent)
        self.leaderboard_window.update_leaderboards(self.username)
        self.leaderboard_window.show()
        self.leaderboard_window.raise_()
        self.leaderboard_window.activateWindow()
        
    def toggle_mode(self):
        if self.dark_mode:
            self.apply_light_mode()
            self.mode_btn.setText("☀️ Light Mode")
        else:
            self.apply_dark_mode()
            self.mode_btn.setText("🌙 Dark Mode")
        self.dark_mode = not self.dark_mode
        
    def apply_dark_mode(self):
        # Apply dark theme to all widgets
        self.setStyleSheet(STYLES['dark']['main'])
        
        # Apply specific styles
        header_frame = self.findChild(QFrame, "header")
        if header_frame:
            header_frame.setStyleSheet(STYLES['dark']['header'])
            
        content_frame = self.findChild(QFrame, "content")
        if content_frame:
            content_frame.setStyleSheet("background-color: #1e1e1e;")
            
        # Apply styles to filter frames
        categories = ["All", "Web", "Crypto", "Reversing", "Forensics", "Misc"]
        for category in categories:
            filter_frame = self.findChild(QFrame, f"filter_frame_{category}")
            if filter_frame:
                filter_frame.setStyleSheet(STYLES['dark']['filter_frame'])
                
        # Reload challenges to update card styles
        self.load_challenges()
        
    def apply_light_mode(self):
        # Apply light theme to all widgets
        self.setStyleSheet(STYLES['light']['main'])
        
        # Apply specific styles
        header_frame = self.findChild(QFrame, "header")
        if header_frame:
            header_frame.setStyleSheet(STYLES['light']['header'])
            
        content_frame = self.findChild(QFrame, "content")
        if content_frame:
            content_frame.setStyleSheet("background-color: #f0f0f0;")
            
        # Apply styles to filter frames
        categories = ["All", "Web", "Crypto", "Reversing", "Forensics", "Misc"]
        for category in categories:
            filter_frame = self.findChild(QFrame, f"filter_frame_{category}")
            if filter_frame:
                filter_frame.setStyleSheet(STYLES['light']['filter_frame'])
                
        # Reload challenges to update card styles
        self.load_challenges() 