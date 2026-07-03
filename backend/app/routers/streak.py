from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.gamification import UserStreak
from app.schemas.gamification import StreakOut

router = APIRouter(prefix="/streak", tags=["streak"])


@router.get("/me", response_model=StreakOut)
def get_my_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    streak = db.query(UserStreak).filter(UserStreak.user_id == current_user.id).first()
    if not streak:
        return StreakOut(current_streak=0, longest_streak=0, last_activity_date=None)
    return streak
