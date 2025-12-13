from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from jose import jwt
import os
from datetime import datetime, timedelta

from app.dependencies import get_current_user

router = APIRouter()

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
APP_JWT_SECRET = os.getenv("APP_JWT_SECRET")

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def create_app_jwt(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, APP_JWT_SECRET, algorithm="HS256")


@router.get("/login/google")
async def login(request: Request):
    redirect_uri = f"{os.getenv('BACKEND_URL')}/api/v1/oauth/callback"
    resp = await oauth.google.authorize_redirect(request, redirect_uri)
    print("STATE SENT:", request.session.get("oauth_google_state"))
    return resp


@router.get("/callback")
async def auth_callback(request: Request):

    returned_state = request.query_params.get("state")
    stored_state = request.session.get("oauth_google_state")

    print("STATE RETURNED:", returned_state)
    print("STATE STORED:", stored_state)
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = await oauth.google.parse_id_token(request, token)

    email = userinfo.get("email")
    if not email:
        return JSONResponse({"error": "no email"}, status_code=400)

    app_token = create_app_jwt(email)

    frontend = os.getenv("FRONTEND_URL")
    return RedirectResponse(url=f"{frontend}/auth?token={app_token}")


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"email": user}
