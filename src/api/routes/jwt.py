from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from auth.jwt import JWTManager
from db.sqlite import get_db
from api.dependencies import jwt_get_current_user
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
async def login(response: Response, user_in: UserLogin, db=Depends(get_db)):
    user_service = UserService()
    jwt_manager = JWTManager()

    username = user_in.username
    password = user_in.password

    if not user_service.validate_user_credentials(username, password, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user = user_service.get_user_by_username(username, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    token = jwt_manager.create_token(user)
    refresh_token = jwt_manager.create_refresh_token(user)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response, user: User = Depends(jwt_get_current_user), db=Depends(get_db)):
    user_service = UserService()
    user_service.update_token_version(user.id, db)
    response.delete_cookie(key="refresh_token")

    return {"message": "Successfully logged out"}


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
async def refresh_token(request: Request, response: Response, db=Depends(get_db)):
    jwt_manager = JWTManager()
    user_service = UserService()

    refresh_token_from_cookie = request.cookies.get("refresh_token")

    if not refresh_token_from_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    
    user_id = jwt_manager.verify_token(refresh_token_from_cookie)
    user = user_service.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    refresh_token = jwt_manager.create_refresh_token(user)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
    )


@router.get("/me")
async def protected_route(current_user: User = Depends(jwt_get_current_user)):
    return current_user.username