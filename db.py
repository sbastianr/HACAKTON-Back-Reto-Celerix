import sqlite3
from typing import Any, List, Tuple, Optional

class Database:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def add_user(self, username, password_hash):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()