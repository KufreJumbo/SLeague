from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.ai_session import TutorSession
from app.models.curriculum import Topic
from app.schemas.ai_session import (
    TutorSessionOut, AskRequest, ExplainTopicRequest, ExplanationOut
)
from app.services.ai import explain_topic, chat_with_tutor
from app.services.gamification import update_streak

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/explain", response_model=ExplanationOut)
def explain(
    body: ExplainTopicRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = db.query(Topic).filter(Topic.id == body.topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    explanation_text = explain_topic(db, body.topic_id, body.mode)

    # Count AI interaction as daily activity
    update_streak(db, current_user.id)

    return ExplanationOut(
        topic_id=topic.id,
        topic_title=topic.title,
        mode=body.mode,
        explanation=explanation_text,
    )


@router.post("/chat", response_model=TutorSessionOut)
def chat(
    body: AskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session, _ = chat_with_tutor(
        db=db,
        user_id=current_user.id,
        message=body.message,
        session_id=body.session_id,
        subject_id=body.subject_id,
        topic_id=body.topic_id,
    )

    update_streak(db, current_user.id)
    return session


@router.get("/sessions", response_model=list[TutorSessionOut])
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(TutorSession)
        .filter(TutorSession.user_id == current_user.id)
        .order_by(TutorSession.created_at.desc())
        .limit(20)
        .all()
    )
    return sessions


@router.get("/sessions/{session_id}", response_model=TutorSessionOut)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(TutorSession).filter(
        TutorSession.id == session_id,
        TutorSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session
