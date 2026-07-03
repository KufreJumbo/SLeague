from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.leaderboard import LeaderboardEntry
from app.schemas.leaderboard import LeaderboardOut, LeaderboardEntryOut
from app.services.leaderboard import get_leaderboard

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/{class_code}", response_model=LeaderboardOut)
def get_class_leaderboard(
    class_code: str,
    subject_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entries_data = get_leaderboard(db, class_code, subject_id)

    entries = [LeaderboardEntryOut(**e) for e in entries_data]

    my_rank = None
    my_entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.user_id == current_user.id,
        LeaderboardEntry.class_code == class_code,
        LeaderboardEntry.subject_id == subject_id,
    ).first()
    if my_entry:
        my_rank = my_entry.rank

    updated_at = entries_data[0]["updated_at"] if entries_data else None

    return LeaderboardOut(
        class_code=class_code,
        subject_id=subject_id,
        entries=entries,
        my_rank=my_rank,
        updated_at=updated_at,
    )
