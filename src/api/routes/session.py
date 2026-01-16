from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from auth.session import SessionManager
from db.sqlite import get_db
from api.dependencies import session_get_current_user
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
    prefix="/session",
    tags=["session"],
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(response: Response, user_in: UserLogin, db=Depends(get_db)):
    user_service = UserService()
    session_manager = SessionManager()

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

    session_id = session_manager.create_session(user.id, db)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        path="/",
    )

    return {"detail": "Successfully logged in"}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, current_user: User = Depends(session_get_current_user), db=Depends(get_db)):
    session_manager = SessionManager()
    session_manager.delete_session(current_user.id, db)

    response.delete_cookie(key="refresh_token")

    return {"detail": "Successfully logged out"}



@router.post("/register", status_code=status.HTTP_200_OK)
async def register(user_in: UserRegister, db=Depends(get_db)):
    user_service = UserService()

    existing_user = user_service.get_user_by_username(user_in.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    user_service.create_user(username=user_in.username, password=user_in.password, is_admin=user_in.is_admin, db=db)

    return {"detail": "User registered successfully"}


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_session_user(current_user: User = Depends(session_get_current_user)):
    return current_user.username