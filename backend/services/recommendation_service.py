from sqlalchemy.orm import Session

from backend.models.career import Career ,CareerSkill

from backend.models.skill import Skill


def recommend_careers(
    user_skills: list,
    db: Session
):

    results = []

    # User ke skills ko lowercase mein convert karna
    user_skill_names = {
        skill.lower().strip()
        for skill in user_skills
    }

    # Database se saare careers
    careers = db.query(Career).all()

    for career in careers:

        # Career ki required skills
        career_skills = (
            db.query(Skill, CareerSkill)
            .join(
                CareerSkill,
                CareerSkill.skill_id == Skill.id
            )
            .filter(
                CareerSkill.career_id == career.id
            )
            .all()
        )

        if not career_skills:
            continue

        total_weight = 0
        matched_weight = 0

        matched_skills = []
        missing_skills = []

        for skill, career_skill in career_skills:

            importance = (
                career_skill.importance or "medium"
            ).lower()

            if importance == "high":
                weight = 3
            elif importance == "medium":
                weight = 2
            else:
                weight = 1

            total_weight += weight

            skill_name = skill.name.lower().strip()

            if skill_name in user_skill_names:

                matched_weight += weight
                matched_skills.append(skill.name)

            else:

                missing_skills.append(skill.name)

        # Match percentage
        if total_weight > 0:
            match_score = (
                matched_weight / total_weight
            ) * 100
        else:
            match_score = 0

        results.append({
            "career_id": career.id,
            "career": career.title,
            "match_score": round(match_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # Highest score first
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results