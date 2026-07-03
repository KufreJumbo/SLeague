from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

from app.models.user import StudentProfile, TierEnum
from app.models.gamification import XPTransaction, XPReasonEnum, UserStreak, Badge, UserBadge

# XP thresholds for each tier
TIER_THRESHOLDS = {
    TierEnum.bronze: 0,
    TierEnum.silver: 500,
    TierEnum.gold: 1500,
    TierEnum.platinum: 4000,
    TierEnum.scholar_elite: 10000,
}

TIER_ORDER = [TierEnum.bronze, TierEnum.silver, TierEnum.gold, TierEnum.platinum, TierEnum.scholar_elite]


def calculate_tier(total_xp: int) -> TierEnum:
    tier = TierEnum.bronze
    for t in TIER_ORDER:
        if total_xp >= TIER_THRESHOLDS[t]:
            tier = t
    return tier


def xp_to_next_tier(total_xp: int) -> int | None:
    for i, t in enumerate(TIER_ORDER):
        if total_xp < TIER_THRESHOLDS[t]:
            return TIER_THRESHOLDS[t] - total_xp
    return None  # already at Scholar Elite


def award_xp(db: Session, user_id: int, amount: int, reason: XPReasonEnum, description: str | None = None) -> XPTransaction:
    tx = XPTransaction(user_id=user_id, amount=amount, reason=reason, description=description)
    db.add(tx)

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if profile:
        profile.total_xp += amount
        profile.tier = calculate_tier(profile.total_xp)

    db.commit()
    db.refresh(tx)
    return tx


def update_streak(db: Session, user_id: int) -> UserStreak:
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    today = date.today()

    if streak.last_activity_date == today:
        return streak  # already logged today

    if streak.last_activity_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1  # streak broken or first time

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_activity_date = today
    db.commit()
    db.refresh(streak)

    # Award streak XP
    award_xp(db, user_id, 10, XPReasonEnum.daily_streak, f"{streak.current_streak}-day streak")

    # Check for streak badges
    _check_streak_badges(db, user_id, streak.current_streak)

    return streak


def _check_streak_badges(db: Session, user_id: int, streak: int):
    milestones = {5: "5-Day Streak", 10: "10-Day Streak", 30: "30-Day Streak"}
    badge_name = milestones.get(streak)
    if not badge_name:
        return

    badge = db.query(Badge).filter(Badge.name == badge_name).first()
    if not badge:
        return

    already_earned = db.query(UserBadge).filter(
        UserBadge.user_id == user_id, UserBadge.badge_id == badge.id
    ).first()

    if not already_earned:
        user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
        db.add(user_badge)
        db.commit()

        if badge.xp_bonus:
            award_xp(db, user_id, badge.xp_bonus, XPReasonEnum.badge_earned, f"Badge: {badge_name}")
