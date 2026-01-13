import sqlite3
from db.base import DatabaseInterface

def get_db():
    return SQLiteDB('database.db')

class SQLiteDB(DatabaseInterface):
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()