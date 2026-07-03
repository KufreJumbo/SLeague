import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class TierEnum(str, enum.Enum):
    bronze = "Bronze"
    silver = "Silver"
    gold = "Gold"
    platinum = "Platinum"
    scholar_elite = "Scholar Elite"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    xp_transactions = relationship("XPTransaction", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("UserStreak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    tutor_sessions = relationship("TutorSession", back_populates="user", cascade="all, delete-orphan")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    country = Column(String, default="Nigeria")
    grade = Column(String, nullable=True)        # e.g. "JSS 1", "SS 2", "Primary 4"
    school_name = Column(String, nullable=True)
    class_code = Column(String, nullable=True, index=True)
    tier = Column(Enum(TierEnum), default=TierEnum.bronze)
    total_xp = Column(Integer, default=0)
    is_onboarded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
