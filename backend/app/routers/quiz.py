import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, StudentProfile
from app.models.quiz import Quiz, Question, QuizAttempt, QuizAnswer
from app.models.curriculum import Topic
from app.schemas.quiz import (
    QuizOut, QuestionOut, QuizSubmitRequest, QuizResultOut, QuizAnswerOut, QuizAttemptSummary
)
from app.services.gamification import award_xp, update_streak
from app.services.leaderboard import upsert_leaderboard_entry
from app.models.gamification import XPReasonEnum

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/topic/{topic_id}", response_model=list[QuizOut])
def list_quizzes_for_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    quizzes = db.query(Quiz).filter(Quiz.topic_id == topic_id).all()
    result = []
    for q in quizzes:
        out = QuizOut.model_validate(q)
        out.question_count = len(q.questions)
        result.append(out)
    return result


@router.get("/{quiz_id}/start", response_model=list[QuestionOut])
def start_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    random.shuffle(questions)  # randomize order each attempt
    return questions


@router.post("/{quiz_id}/submit", response_model=QuizResultOut)
def submit_quiz(
    quiz_id: int,
    body: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    questions = {q.id: q for q in quiz.questions}
    if not questions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz has no questions")

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        total_questions=len(questions),
        started_at=datetime.utcnow(),
    )
    db.add(attempt)
    db.flush()

    correct_count = 0
    answer_outs = []

    for item in body.answers:
        question = questions.get(item.question_id)
        if not question:
            continue

        is_correct = item.selected_answer == question.correct_answer
        if is_correct:
            correct_count += 1

        answer = QuizAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_answer=item.selected_answer,
            is_correct=is_correct,
            time_taken_seconds=item.time_taken_seconds,
        )
        db.add(answer)

        answer_outs.append(QuizAnswerOut(
            question_id=question.id,
            selected_answer=item.selected_answer,
            is_correct=is_correct,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
        ))

    score = (correct_count / len(questions)) * 100
    passed = score >= quiz.passing_score
    is_perfect = correct_count == len(questions)

    # Calculate XP
    xp_earned = quiz.xp_reward if passed else quiz.xp_reward // 2
    if is_perfect:
        xp_earned += 50  # bonus for perfect score

    attempt.score = score
    attempt.correct_count = correct_count
    attempt.xp_earned = xp_earned
    attempt.passed = passed
    attempt.completed_at = datetime.utcnow()

    db.commit()

    # Award XP
    reason = XPReasonEnum.quiz_perfect if is_perfect else XPReasonEnum.quiz_pass
    award_xp(db, current_user.id, xp_earned, reason, f"Quiz: {quiz.title}")

    # Update daily streak
    update_streak(db, current_user.id)

    # Update leaderboard if ranked quiz and user has a class
    if quiz.is_ranked and current_user.profile and current_user.profile.class_code:
        upsert_leaderboard_entry(
            db, current_user.id, current_user.profile.class_code, xp_earned
        )

    return QuizResultOut(
        attempt_id=attempt.id,
        score=score,
        total_questions=len(questions),
        correct_count=correct_count,
        xp_earned=xp_earned,
        passed=passed,
        answers=answer_outs,
    )


@router.get("/history", response_model=list[QuizAttemptSummary])
def my_quiz_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == current_user.id, QuizAttempt.completed_at.isnot(None))
        .order_by(QuizAttempt.completed_at.desc())
        .limit(20)
        .all()
    )
    return attempts
