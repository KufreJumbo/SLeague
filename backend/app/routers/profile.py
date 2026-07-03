from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, StudentProfile
from app.schemas.user import UserOut, StudentProfileOut, StudentProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=StudentProfileOut)
def update_my_profile(
    body: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = current_user.profile
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    # Mark onboarded once grade and class_code are set
    if profile.grade and profile.class_code:
        profile.is_onboarded = True

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{user_id}", response_model=UserOut)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
