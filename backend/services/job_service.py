from sqlalchemy.orm import Session

from backend.models.job import Job


def recommend_jobs(
    user_skills: list,
    career_id: int,
    db: Session
):

    # =====================================================
    # NORMALIZE USER SKILLS
    # =====================================================

    normalized_user_skills = {
        str(skill).lower().strip()
        for skill in (user_skills or [])
    }

    if not normalized_user_skills:
        return []


    # =====================================================
    # GET JOBS FOR SELECTED CAREER
    # =====================================================

    jobs = (
        db.query(Job)
        .filter(
            Job.career_id == career_id
        )
        .all()
    )


    recommendations = []


    # =====================================================
    # MATCH USER SKILLS WITH JOB SKILLS
    # =====================================================

    for job in jobs:

        required_skills = [
            skill.strip()
            for skill in job.required_skills.split(",")
            if skill.strip()
        ]

        normalized_required_skills = {
            skill.lower()
            for skill in required_skills
        }


        # =================================================
        # FIND MATCHED SKILLS
        # =================================================

        matched_skills = [
            skill
            for skill in required_skills
            if skill.lower() in normalized_user_skills
        ]


        # =================================================
        # FIND MISSING SKILLS
        # =================================================

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower() not in normalized_user_skills
        ]


        # =================================================
        # CALCULATE MATCH SCORE
        # =================================================

        if normalized_required_skills:

            match_score = (
                len(matched_skills)
                / len(normalized_required_skills)
            ) * 100

        else:

            match_score = 0


        # =================================================
        # ADD RECOMMENDATION
        # =================================================

        recommendations.append({

            "job_id": job.id,

            "title": job.title,

            "company": job.company,

            "location": job.location,

            "description": job.description,

            "required_skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_score": round(
                match_score,
                2
            ),

            "apply_url": job.apply_url,

            "source": job.source

        })


    # =====================================================
    # SORT BY MATCH SCORE
    # =====================================================

    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )


    return recommendations