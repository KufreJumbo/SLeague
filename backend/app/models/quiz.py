import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean, Float, JSON, Text
from sqlalchemy.orm import relationship
from app.database import Base


class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String, nullable=False)
    time_limit_seconds = Column(Integer, default=600)   # 10 minutes default
    is_ranked = Column(Boolean, default=False)           # ranked = affects leaderboard
    passing_score = Column(Integer, default=60)          # percentage
    xp_reward = Column(Integer, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)       # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer = Column(String(1), nullable=False)  # "A", "B", "C", or "D"
    explanation = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyEnum), default=DifficultyEnum.medium)
    points = Column(Integer, default=1)
    order = Column(Integer, default=0)

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, default=0.0)           # percentage 0–100
    total_questions = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    passed = Column(Boolean, default=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan")


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(String(1), nullable=True)  # null = unanswered
    is_correct = Column(Boolean, default=False)
    time_taken_seconds = Column(Integer, nullable=True)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")
