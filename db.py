import sqlite3
from datetime import datetime
import hashlib


class Database:
    """
    Handles SQLite database operations for habits and completions.
    """

    def __init__(self, db_path: str = "habits.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Initialize database tables: Users, Habits, Completions.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                type TEXT NOT NULL,  -- 'daily' or 'weekly'
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE
            )
        ''')

        # Completions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Completions (
                completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                mood_score INTEGER,
                FOREIGN KEY (habit_id) REFERENCES Habits (habit_id) ON DELETE CASCADE
            )
        ''')

        # Index for faster streak queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_habit_timestamp 
            ON Completions (habit_id, timestamp)
        ''')

        conn.commit()
        conn.close()

    def get_connection(self):
        """Return a new database connection."""
        return sqlite3.connect(self.db_path)

    def register_user(self, username: str, email: str, password: str) -> bool:
        """
        Register a new user with hashed password.
        """
        try:
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Username or email already exists
            return False
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    def authenticate_user(self, username: str, password: str) -> int:
        """
        Authenticate user and return user_id if successful.
        """
        try:
            # Hash the provided password
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id FROM Users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            result = cursor.fetchone()
            conn.close()

            return result[0] if result else None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def user_exists(self, username: str) -> bool:
        """
        Check if a username already exists.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None