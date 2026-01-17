from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from auth.oauth import OAuthManager
from db.sqlite import get_db

from settings import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get("/generate-url")
async def generate_oauth_url():
    oauth_url = settings.REDIRECT_URI
    return {"oauth_url": oauth_url}


@router.get("/callback")
async def auth_callback(code: str, state: str, db=Depends(get_db)):
    oauth_manager = OAuthManager()
    token_response = await oauth_manager.exchange_code_for_token(
        code=code,
        google_redirect_uri=settings.GOOGLE_CALLBACK_URI,
        google_client_id=settings.GOOGLE_CLIENT_ID,
        google_client_secret=settings.GOOGLE_CLIENT_SECRET,
    )

    id_token = token_response.get("id_token")
    if not id_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID token not found in response")
    
    external_user_info = oauth_manager.verify_google_id_token(id_token, settings.GOOGLE_CLIENT_ID)

    username = str(external_user_info.get("name"))
    email = str(external_user_info.get("email"))
    provider_user_id = str(external_user_info.get("sub"))

    user = oauth_manager.get_user_from_external(
        db=db,
        username=username,
        email=email,
        provider_user_id=provider_user_id,
        is_admin=False,
    )

    return {"message": "User authenticated successfully", "user": user, "external_user_info": external_user_info}