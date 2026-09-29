from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from backend.database import get_db
from backend.models.user import User
from backend.models.career import Career
from backend.models.job import Job
from backend.models.resume_analysis import ResumeAnalysis
from backend.utils.security import get_current_user
from backend.services.job_matching_service import calculate_job_match


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

    # =====================================================
    # CHECK CAREER
    # =====================================================

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


    # =====================================================
    # GET LATEST RESUME ANALYSIS
    # =====================================================

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


    # =====================================================
    # GET USER SKILLS
    # =====================================================

    user_skills = resume_analysis.skills or []


    # Skills may be stored as JSON string
    if isinstance(user_skills, str):

        try:

            user_skills = json.loads(
                user_skills
            )

        except json.JSONDecodeError:

            user_skills = []


    # Make sure skills are a list
    if not isinstance(user_skills, list):

        user_skills = []


    # =====================================================
    # FIND JOBS FOR SELECTED CAREER
    # =====================================================

    jobs = (
        db.query(Job)
        .filter(
            Job.career_id == career_id
        )
        .all()
    )


    # =====================================================
    # CALCULATE JOB MATCH
    # =====================================================

    job_results = []


    for job in jobs:

        required_skills = job.required_skills or []


        # Required skills may be stored as JSON string
        if isinstance(
            required_skills,
            str
        ):

            try:

                required_skills = json.loads(
                    required_skills
                )

            except json.JSONDecodeError:

                required_skills = []


        if not isinstance(
            required_skills,
            list
        ):

            required_skills = []


        match_percentage, matched_skills = (
            calculate_job_match(
                user_skills=user_skills,
                required_skills=required_skills
            )
        )


        job_results.append(
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "required_skills": required_skills,
                "matched_skills": matched_skills,
                "match_percentage": match_percentage,
                "apply_url": job.apply_url,
                "source": job.source
            }
        )


    # =====================================================
    # SORT BY MATCH SCORE
    # =====================================================

    job_results.sort(
        key=lambda job: job[
            "match_percentage"
        ],
        reverse=True
    )


    # =====================================================
    # RESPONSE
    # =====================================================

    return {
        "status": "success",
        "career": career.title,
        "total_jobs": len(job_results),
        "jobs": job_results
    }