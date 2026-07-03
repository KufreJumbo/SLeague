from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # e.g. "Mathematics"
    country = Column(String, default="Nigeria")
    grade = Column(String, nullable=False)           # e.g. "JSS 1"
    icon = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    terms = relationship("Term", back_populates="subject", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    tutor_sessions = relationship("TutorSession", back_populates="subject")


class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    number = Column(Integer, nullable=False)         # 1, 2, or 3
    name = Column(String, nullable=False)            # e.g. "Term 1"

    subject = relationship("Subject", back_populates="terms")
    topics = relationship("Topic", back_populates="term", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    difficulty = Column(Integer, default=1)          # 1=easy, 2=medium, 3=hard
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    subject = relationship("Subject", back_populates="topics")
    term = relationship("Term", back_populates="topics")
    quizzes = relationship("Quiz", back_populates="topic", cascade="all, delete-orphan")
    tutor_sessions = relationship("TutorSession", back_populates="topic")
