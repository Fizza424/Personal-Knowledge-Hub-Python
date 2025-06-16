import sqlite3
import hashlib

DB_PATH = "hub.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # Notes Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                tag TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Flashcards Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                answer TEXT,
                subject TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Pomodoro Sessions Table (Optional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                work_minutes INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Insert sample user if not exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           ("testuser", hash_password("testpass")))

        # Insert sample flashcards if not exists
        cursor.execute("SELECT COUNT(*) FROM flashcards")
        if cursor.fetchone()[0] == 0:
            cursor.execute("SELECT id FROM users WHERE username=?", ("testuser",))
            user_id = cursor.fetchone()[0]
            sample_cards = [
                (user_id, "What is Python?", "A programming language.", "Programming"),
                (user_id, "What does HTML stand for?", "HyperText Markup Language.", "Web"),
                (user_id, "Capital of France?", "Paris", "Geography")
            ]
            cursor.executemany("INSERT INTO flashcards (user_id, question, answer, subject) VALUES (?, ?, ?, ?)", sample_cards)

        conn.commit()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

# Auto-run DB init if this file is run directly
if __name__ == "__main__":
    init_db()
    print("Database initialized with sample data.")
