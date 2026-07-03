import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base


class XPReasonEnum(str, enum.Enum):
    quiz_pass = "quiz_pass"
    quiz_perfect = "quiz_perfect"
    daily_streak = "daily_streak"
    study_complete = "study_complete"
    challenge_win = "challenge_win"
    onboarding = "onboarding"
    badge_earned = "badge_earned"


class XPTransaction(Base):
    __tablename__ = "xp_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    reason = Column(Enum(XPReasonEnum), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="xp_transactions")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)      # "Maths Wizard", "5-Day Streak"
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    xp_bonus = Column(Integer, default=0)

    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")


class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="streak")
