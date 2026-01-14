from core.auth import hash_password, verify_password
from db.base import DatabaseInterface


class UserService:
    def create(self, db: DatabaseInterface):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            token_version INTEGER NOT NULL DEFAULT 0
        )
        """
        db.execute_query(query)

    def get_user_by_id(self, user_id: int, db: DatabaseInterface):
        query = "SELECT * FROM users WHERE id = ?"
        result = db.execute_query(query, (user_id,))
        return result[0] if result else None

    def get_user_by_username(self, username: str, db: DatabaseInterface):
        query = "SELECT * FROM users WHERE username = ?"
        result = db.execute_query(query, (username,))
        return result[0] if result else None

    def create_user(
        self, username: str, password: str, is_admin: bool, db: DatabaseInterface
    ):
        password_hash = hash_password(password)
        query = "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)"
        db.execute_query(query, (username, password_hash, is_admin))

    def validate_user_credentials(
        self, username: str, password: str, db: DatabaseInterface
    ) -> bool:
        user_data = self.get_user_by_username(username, db)
        if not user_data:
            return False

        stored_password_hash = user_data[2]
        return verify_password(password, stored_password_hash)

    def update_token_version(self, user_id, db: DatabaseInterface) -> int:

        user = self.get_user_by_id(user_id, db)
        if not user:
            raise Exception("User not found")

        token_version = user[4] + 1

        query = "UPDATE users SET token_version = ? WHERE id = ?"
        db.execute_query(query, (token_version, user_id))
        return token_version