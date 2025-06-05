import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from gui.login import LoginWindow
from gui.dashboard import DashboardWindow
from database.db_manager import DatabaseManager

# Sample Challenges data
SAMPLE_CHALLENGES = [
    # Web Challenges
    {
        'title': 'SQL Injection Basics',
        'category': 'Web',
        'description': 'Find the admin password using SQL injection. The flag is in the admin table.',
        'flag': 'flag{sql_injection_master}',
        'points': 100,
        'difficulty': 'Easy'
    },
    {
        'title': 'XSS Challenge',
        'category': 'Web',
        'description': 'Inject a script that steals cookies. The flag is in the admin cookie.',
        'flag': 'flag{xss_expert}',
        'points': 150,
        'difficulty': 'Medium'
    },
    {
        'title': 'CSRF Attack',
        'category': 'Web',
        'description': 'Perform a Cross-Site Request Forgery attack to change the admin password.',
        'flag': 'flag{csrf_master}',
        'points': 200,
        'difficulty': 'Hard'
    },

    # Crypto Challenges
    {
        'title': 'Caesar Cipher',
        'category': 'Crypto',
        'description': 'Decrypt the message: "Khoor Zruog". The flag is the decrypted text.',
        'flag': 'flag{hello_world}',
        'points': 50,
        'difficulty': 'Easy'
    },
    {
        'title': 'RSA Challenge',
        'category': 'Crypto',
        'description': 'Decrypt the RSA encrypted message using the provided public key.',
        'flag': 'flag{rsa_master}',
        'points': 200,
        'difficulty': 'Hard'
    },
    {
        'title': 'Hash Collision',
        'category': 'Crypto',
        'description': 'Find two different inputs that produce the same MD5 hash.',
        'flag': 'flag{hash_collision}',
        'points': 150,
        'difficulty': 'Medium'
    },

    # Reversing Challenges
    {
        'title': 'Simple Crackme',
        'category': 'Reversing',
        'description': 'Find the password in this simple executable.',
        'flag': 'flag{reverse_engineering}',
        'points': 100,
        'difficulty': 'Easy'
    },
    {
        'title': 'Obfuscated Code',
        'category': 'Reversing',
        'description': 'Deobfuscate this JavaScript code to find the flag.',
        'flag': 'flag{deobfuscation}',
        'points': 150,
        'difficulty': 'Medium'
    },
    {
        'title': 'Anti-Debug',
        'category': 'Reversing',
        'description': 'Bypass the anti-debugging protection to find the flag.',
        'flag': 'flag{anti_debug_master}',
        'points': 250,
        'difficulty': 'Hard'
    },

    # Forensics Challenges
    {
        'title': 'Hidden in Plain Sight',
        'category': 'Forensics',
        'description': 'A secret message was hidden in this image using steganography.',
        'flag': 'flag{steganography_is_fun}',
        'points': 100,
        'difficulty': 'Easy'
    },
    {
        'title': 'Memory Dump',
        'category': 'Forensics',
        'description': 'Analyze this memory dump to find the flag.',
        'flag': 'flag{memory_forensics}',
        'points': 200,
        'difficulty': 'Medium'
    },
    {
        'title': 'Network Traffic',
        'category': 'Forensics',
        'description': 'Analyze this network capture to find the hidden communication.',
        'flag': 'flag{network_analysis}',
        'points': 250,
        'difficulty': 'Hard'
    },

    # Misc Challenges
    {
        'title': 'Binary to Text',
        'category': 'Misc',
        'description': 'Convert this binary string to text: 01000110 01001100 01000001 01000111',
        'flag': 'flag{FLAG}',
        'points': 50,
        'difficulty': 'Easy'
    },
    {
        'title': 'QR Code',
        'category': 'Misc',
        'description': 'Scan this QR code to find the flag.',
        'flag': 'flag{qr_master}',
        'points': 75,
        'difficulty': 'Easy'
    },
    {
        'title': 'Logic Puzzle',
        'category': 'Misc',
        'description': 'Solve this logic puzzle to find the flag.',
        'flag': 'flag{logic_master}',
        'points': 150,
        'difficulty': 'Medium'
    }
]

class CTFPlatform(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Educational CTF Platform")
        self.setMinimumSize(1200, 800)
        
        # Initialize database
        self.db = DatabaseManager()
        self.db.initialize_database()
        self.add_sample_challenges()
        
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
        
    def add_sample_challenges(self):
        # Clear existing challenges first
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM challenges')
        conn.commit()
        conn.close()
        
        # Add new challenges
        print("Adding sample challenges...")
        for challenge in SAMPLE_CHALLENGES:
            self.db.add_challenge(
                challenge['title'],
                challenge['category'],
                challenge['description'],
                challenge['flag'],
                challenge['points'],
                challenge['difficulty']
            )
        print("Sample challenges added.")

    def show_dashboard(self, username):
        self.dashboard.set_username(username)
        self.stacked_widget.setCurrentWidget(self.dashboard)

    def verify_flag(self, challenge_id, flag):
        return self.db.verify_flag(challenge_id, flag)

    def mark_challenge_solved(self, username, challenge_id):
        self.db.mark_challenge_solved(username, challenge_id)
        self.dashboard.load_challenges()

    def update_score_display(self):
        self.dashboard.update_score_display()

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