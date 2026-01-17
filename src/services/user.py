from core.auth import hash_password, verify_password
from db.base import DatabaseInterface
from models.user import User, AuthCredentials

import uuid


class UserService:
    def create_user(
        self,
        db: DatabaseInterface,
        username: str,
        email: str,
        is_admin: bool,
        password: str | None = None,
        provider: str | None = None,
        provider_user_id: str | None = None,
    ):
        user_id = str(uuid.uuid4())
        auth_id = str(uuid.uuid4())
        password_hash = hash_password(password) if password else None

        query = "INSERT INTO users (id, username, email, is_admin) VALUES (?, ?, ?, ?)"
        db.execute_query(query, (user_id, username, email, is_admin))

        auth_query = "INSERT INTO auth_credentials (id, user_id, provider, provider_user_id, password_hash, token_version) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute_query(
            auth_query, (auth_id, user_id, provider, provider_user_id, password_hash, 0)
        )


    def get_user_by_id(self, user_id: str, db: DatabaseInterface) -> User | None:
        query = "SELECT * FROM users WHERE id = ?"
        result = db.execute_query(query, (user_id,))
        return User.get_instance(result[0]) if result else None


    def get_user_by_username(self, username: str, db: DatabaseInterface) -> User | None:
        query = "SELECT * FROM users WHERE username = ?"
        result = db.execute_query(query, (username,))
        return User.get_instance(result[0]) if result else None


    def get_user_by_email(self, email: str, db: DatabaseInterface) -> User | None:
        query = "SELECT * FROM users WHERE email = ?"
        result = db.execute_query(query, (email,))
        return User.get_instance(result[0]) if result else None


    def get_user_auth_credentials(self, user_id: str, db: DatabaseInterface) -> AuthCredentials | None:
        query = "SELECT * FROM auth_credentials WHERE user_id = ?"
        result = db.execute_query(query, (user_id,))

        return AuthCredentials.get_instance(result[0]) if result else None


    def validate_user_credentials(self, username: str, password: str, db: DatabaseInterface) -> bool:
        user = self.get_user_by_username(username, db)
        if not user:
            return False

        user_auth_credentials = self.get_user_auth_credentials(user.id, db)
        if not user_auth_credentials:
            return False

        stored_password_hash = user_auth_credentials.password_hash
        if stored_password_hash:
            return verify_password(password, stored_password_hash)

        return False

    def validate_user_credentials_oauth(self, provider: str, provider_user_id: str, db: DatabaseInterface) -> bool:
        query = (
            "SELECT * FROM auth_credentials WHERE provider = ? AND provider_user_id = ?"
        )
        result = db.execute_query(query, (provider, provider_user_id))

        if not result:
            return False

        return True

    def update_token_version(self, user_id: str, db: DatabaseInterface) -> int:
        user_auth_credentials = self.get_user_auth_credentials(user_id, db)
        if not user_auth_credentials:
            raise Exception("User not found")

        token_version = user_auth_credentials.token_version + 1
        query = "UPDATE auth_credentials SET token_version = ? WHERE user_id = ?"
        db.execute_query(query, (token_version, user_id))
        return token_version
