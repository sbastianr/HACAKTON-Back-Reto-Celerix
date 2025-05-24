import sqlite3
from typing import Any, List, Tuple, Optional

class Database:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self, query: str) -> None:
        """Crea una tabla pasando una query completa."""
        self.cursor.execute(query)
        self.conn.commit()