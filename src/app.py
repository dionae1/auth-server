from fastapi import FastAPI
from api.routes.jwt import router as jwt_router
from services.user import UserService
from db.sqlite import get_db


user_service = UserService()
user_service.create(get_db())

app = FastAPI()

app.include_router(jwt_router)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}