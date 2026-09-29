from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.models.career import Career
from backend.models.resume_analysis import ResumeAnalysis
from backend.utils.security import get_current_user
from backend.services.recommendation_service import recommend_careers


router = APIRouter(
    prefix="/career",
    tags=["Career Recommendation"]
)


# =========================================================
# CAREER RECOMMENDATIONS
# =========================================================

@router.get("/recommend")
def get_career_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    resume_analysis = (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.user_id == current_user.id
        )
        .order_by(
            ResumeAnalysis.id.desc()
        )
        .first()
    )

    if not resume_analysis:

        raise HTTPException(
            status_code=404,
            detail="Please analyze your resume first"
        )

    user_skills = resume_analysis.skills or []

    if not user_skills:

        raise HTTPException(
            status_code=400,
            detail="No skills found in resume analysis"
        )

    recommendations = recommend_careers(
        user_skills=user_skills,
        db=db
    )

    return {
        "status": "success",
        "user_id": current_user.id,
        "skills": user_skills,
        "selected_career_id": current_user.career_id,
        "recommendations": recommendations
    }


# =========================================================
# SELECT CAREER
# =========================================================

@router.post("/select/{career_id}")
def select_career(
    career_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Check career exists
    career = (
        db.query(Career)
        .filter(
            Career.id == career_id
        )
        .first()
    )

    if not career:

        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    # Save selected career
    current_user.career_id = career_id

    db.commit()
    db.refresh(current_user)

    return {
        "status": "success",
        "message": "Career selected successfully",
        "user_id": current_user.id,
        "career_id": career.id,
        "career": career.title
    }