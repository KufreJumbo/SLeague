from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.leaderboard import LeaderboardEntry
from app.models.user import User, StudentProfile


def refresh_leaderboard(db: Session, class_code: str, subject_id: int | None = None):
    """Recalculate ranks for all entries in a class leaderboard."""
    entries = (
        db.query(LeaderboardEntry)
        .filter(
            LeaderboardEntry.class_code == class_code,
            LeaderboardEntry.subject_id == subject_id,
        )
        .order_by(LeaderboardEntry.total_xp.desc())
        .all()
    )

    for i, entry in enumerate(entries, start=1):
        entry.rank = i

    db.commit()


def upsert_leaderboard_entry(
    db: Session, user_id: int, class_code: str, xp_delta: int, subject_id: int | None = None
):
    """Add XP to a user's leaderboard entry and refresh ranks."""
    entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.user_id == user_id,
        LeaderboardEntry.class_code == class_code,
        LeaderboardEntry.subject_id == subject_id,
    ).first()

    if entry:
        entry.total_xp += xp_delta
    else:
        entry = LeaderboardEntry(
            user_id=user_id,
            class_code=class_code,
            subject_id=subject_id,
            total_xp=xp_delta,
        )
        db.add(entry)

    db.commit()
    refresh_leaderboard(db, class_code, subject_id)


def get_leaderboard(db: Session, class_code: str, subject_id: int | None = None, limit: int = 50) -> list[dict]:
    entries = (
        db.query(LeaderboardEntry, User, StudentProfile)
        .join(User, LeaderboardEntry.user_id == User.id)
        .join(StudentProfile, StudentProfile.user_id == User.id)
        .filter(
            LeaderboardEntry.class_code == class_code,
            LeaderboardEntry.subject_id == subject_id,
        )
        .order_by(LeaderboardEntry.rank.asc())
        .limit(limit)
        .all()
    )

    result = []
    for entry, user, profile in entries:
        result.append({
            "rank": entry.rank,
            "user_id": user.id,
            "name": user.name,
            "avatar_url": user.avatar_url,
            "total_xp": entry.total_xp,
            "tier": profile.tier,
            "updated_at": entry.updated_at,
        })
    return result
