from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "Scholars League API"
    debug: bool = False
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # Database
    database_url: str

    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"

    # Google Gemini
    gemini_api_key: str

    # Redis (optional — for leaderboard caching)
    redis_url: str = "redis://localhost:6379"

    # Frontend URL (for OAuth redirects)
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
