from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password_hash: str
    is_admin: bool = False

    @classmethod
    def get_instance(cls, data: dict):
        return cls(
            id=data[0],
            username=data[1],
            password_hash=data[2],
            is_admin=data[3]
        )