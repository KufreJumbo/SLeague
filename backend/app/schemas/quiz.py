from datetime import datetime
from pydantic import BaseModel
from app.models.quiz import DifficultyEnum


class QuestionOut(BaseModel):
    id: int
    text: str
    options: dict
    difficulty: DifficultyEnum
    points: int
    order: int
    # correct_answer and explanation are NOT exposed during an active quiz

    model_config = {"from_attributes": True}


class QuestionWithAnswerOut(QuestionOut):
    correct_answer: str
    explanation: str | None


class QuizOut(BaseModel):
    id: int
    topic_id: int
    title: str
    time_limit_seconds: int
    is_ranked: bool
    passing_score: int
    xp_reward: int
    question_count: int = 0

    model_config = {"from_attributes": True}


class SubmitAnswerItem(BaseModel):
    question_id: int
    selected_answer: str | None = None   # None = skipped
    time_taken_seconds: int | None = None


class QuizSubmitRequest(BaseModel):
    answers: list[SubmitAnswerItem]


class QuizAnswerOut(BaseModel):
    question_id: int
    selected_answer: str | None
    is_correct: bool
    correct_answer: str
    explanation: str | None

    model_config = {"from_attributes": True}


class QuizResultOut(BaseModel):
    attempt_id: int
    score: float
    total_questions: int
    correct_count: int
    xp_earned: int
    passed: bool
    answers: list[QuizAnswerOut]


class QuizAttemptSummary(BaseModel):
    id: int
    quiz_id: int
    score: float
    correct_count: int
    total_questions: int
    xp_earned: int
    passed: bool
    completed_at: datetime | None

    model_config = {"from_attributes": True}
