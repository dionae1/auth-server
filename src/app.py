from fastapi import FastAPI
from api.routes.jwt import router as jwt_router
from api.routes.session import router as session_router
from api.routes.oauth import router as oauth_router

app = FastAPI()

app.include_router(jwt_router)
app.include_router(session_router)
app.include_router(oauth_router)

@app.get("/")
async def read_root():
    return {"message": "The Auth Server is running. Visit /docs for API documentation."}