from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool = False

    @classmethod
    def get_instance(cls, data: dict):
        return cls(
            id=data[0],
            username=data[1],
            email=data[2],
            is_admin=data[3],
        )
    

class AuthCredentials(BaseModel):
    id: str
    user_id: str
    provider: str | None = None
    provider_user_id: str | None = None
    password_hash: str | None = None
    token_version: int

    @classmethod
    def get_instance(cls, data: dict):
        return cls(
            id=data[0],
            user_id=data[1],
            provider=data[2],
            provider_user_id=data[3],
            password_hash=data[4],
            token_version=data[5],
        )


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False