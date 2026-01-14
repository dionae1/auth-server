import jwt
from datetime import datetime, timedelta, timezone

from models.user import User

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


class JWTManager:
    def create_token(self, user: User) -> str:
        payload = {
            "user_id": user.id,
            "token_version": user.token_version,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=3600),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def verify_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("user_id")

        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        
    def revoke_token(self, user: User) -> None:
        user.token_version += 1
        pass

    def get_token_version(self, token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("token_version")

        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
