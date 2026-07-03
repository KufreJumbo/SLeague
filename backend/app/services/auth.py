from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.user import User, StudentProfile
from app.models.gamification import UserStreak

settings = get_settings()


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "type": "access"},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_refresh_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "type": "refresh"},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def get_or_create_user(db: Session, google_id: str, email: str, name: str, avatar_url: str | None) -> User:
    user = db.query(User).filter(User.google_id == google_id).first()
    if user:
        user.name = name
        user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
        return user

    user = User(google_id=google_id, email=email, name=name, avatar_url=avatar_url)
    db.add(user)
    db.flush()

    profile = StudentProfile(user_id=user.id)
    db.add(profile)

    streak = UserStreak(user_id=user.id)
    db.add(streak)

    db.commit()
    db.refresh(user)
    return user
