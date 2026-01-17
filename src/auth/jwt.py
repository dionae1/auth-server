import jwt
from datetime import datetime, timedelta, timezone

from models.user import User, AuthCredentials

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


class JWTManager:
    def create_token(self, user: AuthCredentials) -> str:
        payload = {
            "user_id": user.id,
            "token_version": user.token_version,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=3600),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def create_refresh_token(self, user: AuthCredentials) -> str:
        payload = {
            "user_id": user.id,
            "token_version": user.token_version,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def verify_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("user_id")

        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    def get_token_version(self, token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("token_version")

        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
