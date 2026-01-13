from services.user import UserService
from db.sqlite import get_db
from core.auth import create_token, verify_token
from models.user import User

# def test():
#     db = get_db()
#     user_service = UserService()

#     # Create users table
#     user_service.create(db)
#     user_data = user_service.get_user_by_id(1, db)
#     user = User.get_instance(*user_data)

#     token = create_token(user.id)
#     print(f"Generated Token: {token}")

#     verified_user_id = verify_token(token)
#     print(f"Verified User ID: {verified_user_id}")

# if __name__ == "__main__":
#     test()

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}