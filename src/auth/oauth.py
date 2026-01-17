import httpx

import uuid

from google.oauth2 import id_token
from google.auth.transport import requests

from models.user import User
from services.user import UserService

from db.base import DatabaseInterface

class OAuthManager:
    async def exchange_code_for_token(self, code: str, google_client_id: str, google_client_secret: str, google_redirect_uri: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": google_client_id,
                    "client_secret": google_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": google_redirect_uri,
                },
            )
        resp.raise_for_status()
        return resp.json()


    def verify_google_id_token(self, token: str, client_id: str):
        return id_token.verify_oauth2_token(token, requests.Request(), client_id)


    def get_user_from_external(self, db: DatabaseInterface, username: str, email: str, provider_user_id: str, is_admin: bool = False) -> User | None:
        user_service = UserService()
        username = username.split()[0] + '_'+ str(uuid.uuid4())[:8]
        user = user_service.get_user_by_email(email, db)

        if not user:
            user = user_service.create_user(
                db=db,
                username=username,
                email=email,
                is_admin=is_admin,
                provider="google",
                provider_user_id=provider_user_id,
            )

            user = user_service.get_user_by_email(email, db)

        return user