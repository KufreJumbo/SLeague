from datetime import datetime
from pydantic import BaseModel
from app.models.user import TierEnum


class LeaderboardEntryOut(BaseModel):
    rank: int | None
    user_id: int
    name: str
    avatar_url: str | None
    total_xp: int
    tier: TierEnum

    model_config = {"from_attributes": True}


class LeaderboardOut(BaseModel):
    class_code: str
    subject_id: int | None
    entries: list[LeaderboardEntryOut]
    my_rank: int | None = None
    updated_at: datetime | None = None
