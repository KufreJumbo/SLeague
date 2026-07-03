import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class MessageRoleEnum(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class TutorSession(Base):
    __tablename__ = "tutor_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tutor_sessions")
    subject = relationship("Subject", back_populates="tutor_sessions")
    topic = relationship("Topic", back_populates="tutor_sessions")
    messages = relationship("TutorMessage", back_populates="session", cascade="all, delete-orphan", order_by="TutorMessage.created_at")


class TutorMessage(Base):
    __tablename__ = "tutor_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("tutor_sessions.id"), nullable=False)
    role = Column(Enum(MessageRoleEnum), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("TutorSession", back_populates="messages")
