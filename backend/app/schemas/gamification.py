from datetime import datetime, date
from pydantic import BaseModel
from app.models.gamification import XPReasonEnum
from app.models.user import TierEnum


class XPTransactionOut(BaseModel):
    id: int
    amount: int
    reason: XPReasonEnum
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class XPSummaryOut(BaseModel):
    total_xp: int
    tier: TierEnum
    xp_to_next_tier: int | None   # None if at max tier
    recent_transactions: list[XPTransactionOut]


class BadgeOut(BaseModel):
    id: int
    name: str
    description: str | None
    icon: str | None
    xp_bonus: int
    earned_at: datetime | None = None

    model_config = {"from_attributes": True}


class StreakOut(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: date | None

    model_config = {"from_attributes": True}
