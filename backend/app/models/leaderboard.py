from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_code = Column(String, nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)  # null = overall
    total_xp = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="leaderboard_entries")
    subject = relationship("Subject")

    __table_args__ = (
        UniqueConstraint("user_id", "class_code", "subject_id", name="uq_leaderboard_user_class_subject"),
    )
