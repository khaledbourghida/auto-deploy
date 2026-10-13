import sqlite3
import os
import sys
from pathlib import Path

class DataBase:
    def __init__(self):
        self.db_path = self.get_db_path()
        
    def get_db_path(self):
        # # Check if we're running as a packaged app
        # if getattr(sys, 'frozen', False):
        #     # Running as compiled executable
        #     # Use user's home directory for writable database
        #     base_dir = Path.home() / ".automation_app" / "data"
        # else:
        #     # Running in development
        base_dir = Path(__file__).parent
        
        base_dir.mkdir(parents=True, exist_ok=True)
        return str(base_dir / "my_db.db")

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def close(self, conn):
        if conn:
            conn.close()

    def execute(self, query, params=()):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            self.close(conn)

    def fetch_all(self, query, params=()):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            self.close(conn)