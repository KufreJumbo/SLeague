from datetime import datetime
from pydantic import BaseModel
from app.models.ai_session import MessageRoleEnum


class TutorMessageOut(BaseModel):
    id: int
    role: MessageRoleEnum
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TutorSessionOut(BaseModel):
    id: int
    subject_id: int | None
    topic_id: int | None
    title: str | None
    created_at: datetime
    messages: list[TutorMessageOut] = []

    model_config = {"from_attributes": True}


class AskRequest(BaseModel):
    message: str
    session_id: int | None = None     # continue existing session or start new
    subject_id: int | None = None
    topic_id: int | None = None


class ExplainTopicRequest(BaseModel):
    topic_id: int
    mode: str = "simple"              # "simple", "exam_style", "step_by_step"


class ExplanationOut(BaseModel):
    topic_id: int
    topic_title: str
    mode: str
    explanation: str
