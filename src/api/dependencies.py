from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import JWTManager
from db.sqlite import get_db
from models.user import User
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> User:
    jwt_manager = JWTManager()
    user_service = UserService()

    try:
        user_id = jwt_manager.verify_token(token)
        user_data = user_service.get_user_by_id(user_id, db)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        user = User.get_instance(user_data)

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