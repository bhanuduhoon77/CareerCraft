from sqlalchemy.orm import Session

from backend.models.roadmap import Roadmap, RoadmapItem
from backend.models.career import Career, CareerSkill
from backend.models.skill import Skill


# =========================================================
# CREATE PERSONALIZED ROADMAP
# =========================================================

def create_personalized_roadmap(
    user_id: int,
    career_id: int,
    missing_skills: list,
    db: Session
):

    # -----------------------------------------------------
    # GET SELECTED CAREER
    # -----------------------------------------------------

    career = (
        db.query(Career)
        .filter(Career.id == career_id)
        .first()
    )

    if not career:
        return None


    # -----------------------------------------------------
    # GET CAREER REQUIRED SKILLS
    # -----------------------------------------------------

    career_skills = (
        db.query(Skill, CareerSkill)
        .join(
            CareerSkill,
            CareerSkill.skill_id == Skill.id
        )
        .filter(
            CareerSkill.career_id == career_id
        )
        .order_by(
            CareerSkill.required_proficiency.desc()
        )
        .all()
    )


    # -----------------------------------------------------
    # NORMALIZE USER MISSING SKILLS
    # -----------------------------------------------------

    missing_skill_names = {
        str(skill).lower().strip()
        for skill in (missing_skills or [])
    }


    # -----------------------------------------------------
    # FIND CAREER-RELEVANT MISSING SKILLS
    # -----------------------------------------------------

    relevant_missing_skills = []

    for skill, career_skill in career_skills:

        skill_name = skill.name.lower().strip()

        if skill_name in missing_skill_names:

            relevant_missing_skills.append(
                skill.name
            )


    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------
    #
    # If Gemini's missing_skills don't match the
    # selected career's skills, use the selected
    # career's required skills.
    #
    # This prevents unrelated skills from appearing
    # in the roadmap.
    #
    # Example:
    # Java Backend Developer
    # ❌ Deep Learning
    # ❌ MLOps
    #
    # Instead:
    # ✅ Java
    # ✅ Spring Boot
    # ✅ REST API
    # ✅ SQL
    # etc.
    # -----------------------------------------------------

    if not relevant_missing_skills:

        relevant_missing_skills = [
            skill.name
            for skill, career_skill in career_skills
        ]


    # -----------------------------------------------------
    # CREATE ROADMAP
    # -----------------------------------------------------

    roadmap = Roadmap(
        user_id=user_id,
        career_id=career_id,
        title=f"{career.title} Career Roadmap",
        description=(
            f"Personalized roadmap for becoming "
            f"{career.title}"
        ),
        progress=0.0,
        status="active"
    )

    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)


    # -----------------------------------------------------
    # CREATE ROADMAP ITEMS
    # -----------------------------------------------------

    order_number = 1

    for skill_name in relevant_missing_skills:

        skill = (
            db.query(Skill)
            .filter(
                Skill.name.ilike(skill_name)
            )
            .first()
        )

        roadmap_item = RoadmapItem(
            roadmap_id=roadmap.id,
            skill_id=skill.id if skill else None,
            title=f"Learn {skill_name}",
            description=(
                f"Learn and practice {skill_name} "
                f"to become job-ready for "
                f"{career.title}."
            ),
            order_number=order_number,
            status="pending",
            score=0.0
        )

        db.add(roadmap_item)

        order_number += 1


    db.commit()

    return roadmap


# =========================================================
# UPDATE ROADMAP PROGRESS
# =========================================================

def update_roadmap_progress(
    roadmap_id: int,
    db: Session
):

    # -----------------------------------------------------
    # GET ROADMAP
    # -----------------------------------------------------

    roadmap = (
        db.query(Roadmap)
        .filter(
            Roadmap.id == roadmap_id
        )
        .first()
    )

    if not roadmap:
        return None


    # -----------------------------------------------------
    # GET ROADMAP ITEMS
    # -----------------------------------------------------

    items = (
        db.query(RoadmapItem)
        .filter(
            RoadmapItem.roadmap_id == roadmap_id
        )
        .all()
    )


    # -----------------------------------------------------
    # NO ITEMS
    # -----------------------------------------------------

    if not items:

        roadmap.progress = 0.0
        roadmap.status = "active"

        db.commit()
        db.refresh(roadmap)

        return roadmap


    # -----------------------------------------------------
    # COUNT COMPLETED ITEMS
    # -----------------------------------------------------

    completed_items = sum(
        1
        for item in items
        if item.status == "completed"
    )


    # -----------------------------------------------------
    # CALCULATE PROGRESS
    # -----------------------------------------------------

    roadmap.progress = round(
        (completed_items / len(items)) * 100,
        2
    )


    # -----------------------------------------------------
    # UPDATE ROADMAP STATUS
    # -----------------------------------------------------

    if completed_items == len(items):

        roadmap.status = "completed"

    else:

        roadmap.status = "active"


    db.commit()
    db.refresh(roadmap)

    return roadmap