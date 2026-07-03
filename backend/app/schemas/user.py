from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import TierEnum


class StudentProfileBase(BaseModel):
    country: str = "Nigeria"
    grade: str | None = None
    school_name: str | None = None
    class_code: str | None = None


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(StudentProfileBase):
    country: str | None = None


class StudentProfileOut(StudentProfileBase):
    id: int
    user_id: int
    tier: TierEnum
    total_xp: int
    is_onboarded: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    avatar_url: str | None
    created_at: datetime
    profile: StudentProfileOut | None

    model_config = {"from_attributes": True}


class UserSummary(BaseModel):
    id: int
    name: str
    avatar_url: str | None

    model_config = {"from_attributes": True}
