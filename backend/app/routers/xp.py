from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.gamification import XPTransaction, UserBadge, Badge
from app.schemas.gamification import XPSummaryOut, XPTransactionOut, BadgeOut
from app.services.gamification import xp_to_next_tier

router = APIRouter(prefix="/xp", tags=["xp"])


@router.get("/summary", response_model=XPSummaryOut)
def get_xp_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = current_user.profile
    total_xp = profile.total_xp if profile else 0
    tier = profile.tier if profile else "Bronze"

    recent = (
        db.query(XPTransaction)
        .filter(XPTransaction.user_id == current_user.id)
        .order_by(XPTransaction.created_at.desc())
        .limit(10)
        .all()
    )

    return XPSummaryOut(
        total_xp=total_xp,
        tier=tier,
        xp_to_next_tier=xp_to_next_tier(total_xp),
        recent_transactions=recent,
    )


@router.get("/transactions", response_model=list[XPTransactionOut])
def get_xp_transactions(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(XPTransaction)
        .filter(XPTransaction.user_id == current_user.id)
        .order_by(XPTransaction.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/badges", response_model=list[BadgeOut])
def get_my_badges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_badges = (
        db.query(UserBadge, Badge)
        .join(Badge, UserBadge.badge_id == Badge.id)
        .filter(UserBadge.user_id == current_user.id)
        .all()
    )

    result = []
    for user_badge, badge in user_badges:
        result.append(BadgeOut(
            id=badge.id,
            name=badge.name,
            description=badge.description,
            icon=badge.icon,
            xp_bonus=badge.xp_bonus,
            earned_at=user_badge.earned_at,
        ))
    return result
