import sqlite3
import bcrypt
import os

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join('database', 'ctf.db')
        os.makedirs('database', exist_ok=True)
        
    def initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                score INTEGER DEFAULT 0
            )
        ''')
        
        # Create challenges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                flag TEXT NOT NULL,
                points INTEGER NOT NULL,
                difficulty TEXT NOT NULL
            )
        ''')
        
        # Create solved_challenges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solved_challenges (
                user_id INTEGER,
                challenge_id INTEGER,
                solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (challenge_id) REFERENCES challenges (id),
                PRIMARY KEY (user_id, challenge_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_user(self, username, password):
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                         (username, password_hash))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            # Username likely already exists due to UNIQUE constraint
            return False
            
    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            stored_hash = result[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False
        
    def user_exists(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
        
    def get_user_score(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT score FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
        
    def update_user_score(self, username, points):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET score = score + ? WHERE username = ?',
                      (points, username))
        conn.commit()
        conn.close()
        
    def add_challenge(self, title, category, description, flag, points, difficulty):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO challenges (title, category, description, flag, points, difficulty)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, category, description, flag, points, difficulty))
        conn.commit()
        conn.close()
        
    def get_challenges(self, category=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category and category != "All":
            cursor.execute('SELECT * FROM challenges WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT * FROM challenges')
            
        challenges = cursor.fetchall()
        conn.close()
        return challenges
        
    def verify_flag(self, challenge_id, flag):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT flag FROM challenges WHERE id = ?', (challenge_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result and result[0] == flag
        
    def mark_challenge_solved(self, username, challenge_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user_id
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        
        # Get challenge points
        cursor.execute('SELECT points FROM challenges WHERE id = ?', (challenge_id,))
        points = cursor.fetchone()[0]
        
        # Add to solved_challenges
        cursor.execute('''
            INSERT OR IGNORE INTO solved_challenges (user_id, challenge_id)
            VALUES (?, ?)
        ''', (user_id, challenge_id))
        
        # Update user score
        cursor.execute('UPDATE users SET score = score + ? WHERE id = ?',
                      (points, user_id))
        
        conn.commit()
        conn.close()
        
    def get_global_rankings(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                ROW_NUMBER() OVER (ORDER BY u.score DESC) as rank,
                u.username,
                u.score,
                COUNT(sc.challenge_id) as solved_count
            FROM users u
            LEFT JOIN solved_challenges sc ON u.id = sc.user_id
            GROUP BY u.id, u.username, u.score
            ORDER BY u.score DESC
        ''')
        rankings = cursor.fetchall()
        conn.close()
        return rankings
        
    def get_category_rankings(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Get all categories
        cursor.execute('SELECT DISTINCT category FROM challenges')
        categories = [row[0] for row in cursor.fetchall()]

        all_category_rankings = []
        for category in categories:
             cursor.execute('''
                SELECT
                    ROW_NUMBER() OVER (ORDER BY SUM(c.points) DESC) as rank,
                    u.username,
                    c.category,
                    SUM(c.points) as category_score
                FROM users u
                JOIN solved_challenges sc ON u.id = sc.user_id
                JOIN challenges c ON sc.challenge_id = c.id
                WHERE c.category = ?
                GROUP BY u.id, u.username, c.category
                ORDER BY category_score DESC
             ''', (category,))
             category_rankings = cursor.fetchall()
             all_category_rankings.extend(category_rankings)

        conn.close()
        # Note: This returns a list of rankings across all categories, not separate rankings per category.
        # The LeaderboardWindow will need to handle displaying this correctly.
        return all_category_rankings
        
    def get_user_statistics(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id_row = cursor.fetchone()
        if not user_id_row:
            conn.close()
            return [] # Return empty list if user not found
        user_id = user_id_row[0]

        # Get category-wise stats for the user
        cursor.execute('''
            SELECT
                c.category,
                COUNT(sc.challenge_id) as solved_count,
                SUM(c.points) as category_score
            FROM challenges c
            LEFT JOIN solved_challenges sc ON c.id = sc.challenge_id AND sc.user_id = ?
            GROUP BY c.category
            ORDER BY c.category
        ''', (user_id,))
        stats = cursor.fetchall()

        conn.close()
        # Return a list of tuples: (category, solved_count, category_score)
        return stats 