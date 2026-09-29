from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.models.career import Career
from backend.models.job import Job
from backend.utils.security import get_current_user


router = APIRouter(
    prefix="/jobs",
    tags=["Job Recommendations"]
)


@router.get("/recommend/{career_id}")
def recommend_jobs(
    career_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Check career
    career = (
        db.query(Career)
        .filter(Career.id == career_id)
        .first()
    )

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    # Find jobs for selected career
    jobs = (
        db.query(Job)
        .filter(Job.career_id == career_id)
        .all()
    )

    return {
        "status": "success",
        "career": career.title,
        "total_jobs": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "required_skills": job.required_skills,
                "apply_url": job.apply_url,
                "source": job.source
            }
            for job in jobs
        ]
    }