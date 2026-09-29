from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.models.career import Career
from backend.models.resume_analysis import ResumeAnalysis
from backend.models.roadmap import Roadmap, RoadmapItem
from backend.utils.security import get_current_user
from backend.services.roadmap_service import (
    create_personalized_roadmap,
    update_roadmap_progress
)


router = APIRouter(
    prefix="/roadmap",
    tags=["Career Roadmap"]
)


# =========================================================
# GENERATE ROADMAP
# =========================================================

@router.post("/generate/{career_id}")
def generate_roadmap(
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

    # Get latest resume analysis
    resume_analysis = (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.user_id == current_user.id
        )
        .order_by(ResumeAnalysis.id.desc())
        .first()
    )

    if not resume_analysis:
        raise HTTPException(
            status_code=404,
            detail="Please analyze your resume first"
        )

    # Get missing skills
    missing_skills = resume_analysis.missing_skills or []

    # Create personalized roadmap
    roadmap = create_personalized_roadmap(
        user_id=current_user.id,
        career_id=career_id,
        missing_skills=missing_skills,
        db=db
    )

    if not roadmap:
        raise HTTPException(
            status_code=500,
            detail="Could not create roadmap"
        )

    return {
        "status": "success",
        "message": "Personalized roadmap created successfully",
        "roadmap_id": roadmap.id,
        "career": career.title,
        "missing_skills": missing_skills
    }


# =========================================================
# COMPLETE ROADMAP ITEM
# =========================================================

@router.put("/item/{item_id}/complete")
def complete_roadmap_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    item = (
        db.query(RoadmapItem)
        .join(
            Roadmap,
            Roadmap.id == RoadmapItem.roadmap_id
        )
        .filter(
            RoadmapItem.id == item_id,
            Roadmap.user_id == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Roadmap item not found"
        )

    item.status = "completed"

    db.commit()

    roadmap = update_roadmap_progress(
        roadmap_id=item.roadmap_id,
        db=db
    )

    return {
        "status": "success",
        "message": "Roadmap item completed",
        "item_id": item.id,
        "item_status": item.status,
        "roadmap_id": roadmap.id,
        "progress": roadmap.progress,
        "roadmap_status": roadmap.status
    }


# =========================================================
# GET CURRENT USER'S ROADMAP
# =========================================================

@router.get("/current")
def get_current_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Get latest roadmap belonging to logged-in user
    roadmap = (
        db.query(Roadmap)
        .filter(
            Roadmap.user_id == current_user.id
        )
        .order_by(
            Roadmap.id.desc()
        )
        .first()
    )

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail="No roadmap found for current user"
        )

    # Get roadmap items
    items = (
        db.query(RoadmapItem)
        .filter(
            RoadmapItem.roadmap_id == roadmap.id
        )
        .order_by(
            RoadmapItem.order_number
        )
        .all()
    )

    return {
        "status": "success",

        "roadmap": {
            "id": roadmap.id,
            "career_id": roadmap.career_id,
            "title": roadmap.title,
            "description": roadmap.description,
            "progress": roadmap.progress,
            "status": roadmap.status
        },

        "items": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "order_number": item.order_number,
                "status": item.status,
                "score": item.score
            }
            for item in items
        ]
    }


# =========================================================
# GET ROADMAP BY ID
# =========================================================

@router.get("/{roadmap_id}")
def get_roadmap(
    roadmap_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    roadmap = (
        db.query(Roadmap)
        .filter(
            Roadmap.id == roadmap_id,
            Roadmap.user_id == current_user.id
        )
        .first()
    )

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found"
        )

    items = (
        db.query(RoadmapItem)
        .filter(
            RoadmapItem.roadmap_id == roadmap.id
        )
        .order_by(
            RoadmapItem.order_number
        )
        .all()
    )

    return {
        "status": "success",

        "roadmap": {
            "id": roadmap.id,
            "career_id": roadmap.career_id,
            "title": roadmap.title,
            "description": roadmap.description,
            "progress": roadmap.progress,
            "status": roadmap.status
        },

        "items": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "order_number": item.order_number,
                "status": item.status,
                "score": item.score
            }
            for item in items
        ]
    }