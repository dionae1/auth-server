from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from auth.jwt import JWTManager
from db.sqlite import get_db
from api.dependencies import get_current_user
from models.user import User
from services.user import UserService


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str
    is_admin: bool = False


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_in: UserLogin, db=Depends(get_db)):
    user_service = UserService()
    jwt_manager = JWTManager()

    username = user_in.username
    password = user_in.password

    if not user_service.validate_user_credentials(username, password, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password", 
        )

    user_data = user_service.get_user_by_username(username, db)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user = User.get_instance(user_data)
    token = jwt_manager.create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    pass


@router.post("/register")
async def register(user_in: UserRegister, db=Depends(get_db)):
    user_service = UserService()

    username = user_in.username
    password = user_in.password
    is_admin = user_in.is_admin

    if user_service.get_user_by_username(username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    user_service.create_user(username, password, is_admin=is_admin, db=db)
    return {"message": "User registered successfully"}


@router.post("/refresh")
async def refresh_token():
    pass


@router.get("/me")
async def protected_route(user_id = Depends(get_current_user), db=Depends(get_db)):
    user_service = UserService()
    user_data = user_service.get_user_by_id(user_id, db)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = User.get_instance(user_data)
    return user