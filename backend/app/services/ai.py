import google.generativeai as genai
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.curriculum import Topic, Subject
from app.models.ai_session import TutorSession, TutorMessage, MessageRoleEnum

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)
_model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are an expert academic tutor for Scholars League, an AI-powered learning platform for K-12 students in Nigeria and Africa.

Your role:
- Explain curriculum-aligned topics clearly and accurately
- Adapt your language to the student's grade level
- Use relatable African examples and contexts when helpful
- Stay focused on the subject and topic at hand
- Be encouraging, patient, and supportive
- For exam-style explanations, use structured notes with key points
- Never provide harmful, inappropriate, or off-topic content

Always ground your answers in the Nigerian NERDC curriculum where applicable."""


def _build_explanation_prompt(topic: Topic, subject: Subject, mode: str) -> str:
    mode_instructions = {
        "simple": "Explain this topic in simple, easy-to-understand language suitable for the student's grade level.",
        "exam_style": "Provide a structured exam-style explanation with: key definitions, main points, worked examples, and likely exam questions.",
        "step_by_step": "Break down this topic step by step, explaining each concept before moving to the next.",
    }
    instruction = mode_instructions.get(mode, mode_instructions["simple"])

    return f"""{SYSTEM_PROMPT}

Subject: {subject.name} | Grade: {subject.grade} | Country: {subject.country}
Topic: {topic.title}
{f"Summary: {topic.summary}" if topic.summary else ""}

Task: {instruction}"""


def explain_topic(db: Session, topic_id: int, mode: str = "simple") -> str:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        return "Topic not found."

    subject = db.query(Subject).filter(Subject.id == topic.subject_id).first()
    prompt = _build_explanation_prompt(topic, subject, mode)

    response = _model.generate_content(prompt)
    return response.text


def chat_with_tutor(
    db: Session,
    user_id: int,
    message: str,
    session_id: int | None = None,
    subject_id: int | None = None,
    topic_id: int | None = None,
) -> tuple[TutorSession, str]:
    # Get or create session
    if session_id:
        session = db.query(TutorSession).filter(
            TutorSession.id == session_id,
            TutorSession.user_id == user_id,
        ).first()
    else:
        session = None

    if not session:
        session = TutorSession(
            user_id=user_id,
            subject_id=subject_id,
            topic_id=topic_id,
        )
        db.add(session)
        db.flush()

    # Build conversation history for Gemini
    history = []
    for msg in session.messages:
        role = "user" if msg.role == MessageRoleEnum.user else "model"
        history.append({"role": role, "parts": [msg.content]})

    # Build context prefix for the first message
    context = SYSTEM_PROMPT
    if subject_id:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if subject:
            context += f"\n\nSubject context: {subject.name} ({subject.grade}, {subject.country})"
    if topic_id:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if topic:
            context += f"\nCurrent topic: {topic.title}"
            if topic.summary:
                context += f"\nTopic summary: {topic.summary}"

    # If this is the first message, prepend the system context
    if not history:
        full_message = f"{context}\n\nStudent question: {message}"
    else:
        full_message = message

    # Save the user message
    user_msg = TutorMessage(session_id=session.id, role=MessageRoleEnum.user, content=message)
    db.add(user_msg)

    # Call Gemini with history
    chat = _model.start_chat(history=history)
    response = chat.send_message(full_message)
    reply = response.text

    # Save the assistant reply
    assistant_msg = TutorMessage(session_id=session.id, role=MessageRoleEnum.assistant, content=reply)
    db.add(assistant_msg)

    # Set session title from first message if not set
    if not session.title and len(session.messages) == 0:
        session.title = message[:80]

    db.commit()
    db.refresh(session)

    return session, reply
