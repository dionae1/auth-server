from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password_hash: str
    is_admin: bool = False
    token_version: int = 0

    @classmethod
    def get_instance(cls, data: dict):
        return cls(
            id=data[0],
            username=data[1],
            password_hash=data[2],
            is_admin=data[3],
            token_version=data[4]
        )