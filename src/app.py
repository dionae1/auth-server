from fastapi import FastAPI
from api.routes.jwt import router as jwt_router

app = FastAPI()

app.include_router(jwt_router)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}