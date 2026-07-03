from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth, profile, quiz, xp, leaderboard, streak, ai

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Backend API for Scholars League — AI-powered K-12 academic platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(quiz.router)
app.include_router(xp.router)
app.include_router(leaderboard.router)
app.include_router(streak.router)
app.include_router(ai.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
