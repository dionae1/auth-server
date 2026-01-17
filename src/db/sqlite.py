import sqlite3
from db.base import DatabaseInterface

def get_db():
    return SQLiteDB('database.db')

class SQLiteDB(DatabaseInterface):
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
                            
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL
        );
                  
        """)

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        );
        
        """)

        self.cursor.execute("""
                            
        CREATE TABLE IF NOT EXISTS auth_credentials (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            provider TEXT,
            provider_user_id TEXT,
            password_hash TEXT,
            token_version INTEGER NOT NULL DEFAULT 0
        );
        
        """)

        self.connection.commit()


    def execute_query(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()