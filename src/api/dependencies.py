from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import JWTManager
from auth.session import SessionManager
from db.sqlite import get_db
from models.user import User
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def jwt_get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> User:
    jwt_manager = JWTManager()
    user_service = UserService()

    try:
        user_id = jwt_manager.verify_token(token)
        user = user_service.get_user_by_id(user_id, db)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.token_version != jwt_manager.get_token_version(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )
        
        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    

def session_get_current_user(request: Request, db=Depends(get_db)) -> User:
    session_manager = SessionManager()
    user_service = UserService()

    session_id = request.cookies.get("session_id")
    user_id = session_manager.verify_session(session_id, db)

    if user_id < 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )

    user = user_service.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user