import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.config import get_settings
from app.schemas.auth import TokenResponse, RefreshRequest
from app.services.auth import create_access_token, create_refresh_token, get_or_create_user

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@router.get("/google")
def google_login():
    """Redirect browser to Google OAuth consent screen."""
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return RedirectResponse(url=f"{GOOGLE_AUTH_URL}?{query}")


@router.get("/google/callback", response_model=TokenResponse)
def google_callback(code: str, db: Session = Depends(get_db)):
    """Exchange Google auth code for app JWT tokens."""
    # Exchange code for Google tokens
    async_client = httpx.Client()
    token_resp = async_client.post(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": settings.google_redirect_uri,
            "grant_type": "authorization_code",
        },
    )

    if token_resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to exchange Google code")

    google_tokens = token_resp.json()
    google_access_token = google_tokens.get("access_token")

    # Fetch user info from Google
    userinfo_resp = async_client.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {google_access_token}"},
    )
    async_client.close()

    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch Google user info")

    userinfo = userinfo_resp.json()
    google_id = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name", email)
    avatar_url = userinfo.get("picture")

    if not google_id or not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incomplete Google profile")

    user = get_or_create_user(db, google_id=google_id, email=email, name=name, avatar_url=avatar_url)

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(body: RefreshRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for new access + refresh tokens."""
    try:
        payload = jwt.decode(body.refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )
