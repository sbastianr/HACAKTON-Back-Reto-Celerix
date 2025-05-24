import sqlite3
from typing import Any, List, Tuple, Optional

class Database:
    def __init__(self):
        self.db_path = "../resources/database.sqlite"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    # Función para obtener o crear usuario
    def get_or_create_user(self, nombre, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = self.cursor.fetchone()
        if not user:
            self.cursor.execute("INSERT INTO users (id, nombre, email) VALUES (?, ?, ?)", (nombre, email))
            self.conn.commit()
        return {"nombre": nombre, "email": email}