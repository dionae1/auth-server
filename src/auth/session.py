import uuid
from db.base import DatabaseInterface


class SessionManager:
    def __init__(self):
        self.secret_key = "your_session_secret_key"
        
    def create_session(self, user_id, db: DatabaseInterface):
        session_id = f"session_{uuid.uuid4()}"
        db.execute_query("INSERT INTO sessions (session_id, user_id) VALUES (?, ?)", (session_id, user_id))
        return session_id

    def verify_session(self, session_id, db: DatabaseInterface) -> int:
        result = db.execute_query("SELECT user_id FROM sessions WHERE session_id = ?", (session_id,))
        return result[0][0] if result else -1
    
    def delete_session(self, session_id, db: DatabaseInterface):
        db.execute_query("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        return True