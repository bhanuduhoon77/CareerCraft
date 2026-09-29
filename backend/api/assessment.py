from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from pydantic import BaseModel

from backend.database import get_db
from backend.models.user import User
from backend.models.roadmap import Roadmap, RoadmapItem
from backend.models.assessment import Assessment
from backend.utils.security import get_current_user
from backend.services.gemini_service import generate_assessment_questions
from backend.services.roadmap_service import update_roadmap_progress


router = APIRouter(
    prefix="/assessment",
    tags=["Skill Assessment"]
)


@router.post("/create/{roadmap_item_id}")
def create_assessment(
    roadmap_item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find roadmap item belonging to current user
    item = (
        db.query(RoadmapItem)
        .join(
            Roadmap,
            Roadmap.id == RoadmapItem.roadmap_id
        )
        .filter(
            RoadmapItem.id == roadmap_item_id,
            Roadmap.user_id == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Roadmap item not found"
        )

    # Extract topic from roadmap item
    topic = item.title.replace("Learn ", "")

    # Generate questions using Gemini
    questions_text = generate_assessment_questions(topic)

    try:
        questions = json.loads(questions_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned invalid question format"
        )

    if not isinstance(questions, list) or len(questions) != 5:
        raise HTTPException(
            status_code=500,
            detail="Gemini did not generate exactly 5 questions"
        )

    # Create assessment
    assessment = Assessment(
        user_id=current_user.id,
        roadmap_item_id=item.id,
        topic=topic,
        questions=json.dumps(questions),
        answers=json.dumps([]),
        score=0.0,
        status="pending"
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "status": "success",
        "message": "Assessment created successfully",
        "assessment_id": assessment.id,
        "roadmap_item_id": item.id,
        "topic": topic,
        "questions": questions,
        "status": assessment.status
    }


class AssessmentSubmission(BaseModel):
    answers: list


@router.post("/submit/{assessment_id}")
def submit_assessment(
    assessment_id: int,
    submission: AssessmentSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find assessment belonging to current user
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    # Assessment already completed
    if assessment.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Assessment already completed"
        )

    # Load questions
    try:
        questions = json.loads(assessment.questions)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid assessment questions"
        )

    # Validate number of answers
    if len(submission.answers) != len(questions):
        raise HTTPException(
            status_code=400,
            detail=f"Please submit exactly {len(questions)} answers"
        )

    # Calculate score
    correct_count = 0

    for question, user_answer in zip(
        questions,
        submission.answers
    ):

        if (
            user_answer.strip().lower()
            == question["correct_answer"].strip().lower()
        ):
            correct_count += 1

    score = (
        correct_count / len(questions)
    ) * 100

    # Save assessment result
    assessment.answers = json.dumps(
        submission.answers
    )

    assessment.score = round(score, 2)
    assessment.status = "completed"

    # Find roadmap item
    roadmap_item = (
        db.query(RoadmapItem)
        .filter(
            RoadmapItem.id == assessment.roadmap_item_id
        )
        .first()
    )

    if not roadmap_item:
        raise HTTPException(
            status_code=404,
            detail="Roadmap item not found"
        )

    # Update roadmap item score
    roadmap_item.score = round(score, 2)

    # 60% or above = completed
    if score >= 60:
        roadmap_item.status = "completed"
    else:
        roadmap_item.status = "pending"

    # Save assessment + roadmap item
    db.commit()

    # Update overall roadmap progress
    roadmap = update_roadmap_progress(
        roadmap_id=roadmap_item.roadmap_id,
        db=db
    )

    db.refresh(assessment)

    return {
        "status": "success",
        "message": "Assessment submitted successfully",
        "assessment_id": assessment.id,
        "total_questions": len(questions),
        "correct_answers": correct_count,
        "score": assessment.score,
        "roadmap_item_id": roadmap_item.id,
        "roadmap_item_score": roadmap_item.score,
        "roadmap_item_status": roadmap_item.status,
        "roadmap_progress": roadmap.progress,
        "roadmap_status": roadmap.status,
        "assessment_status": assessment.status
    }
@router.get("/history")
def get_assessment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assessments = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user.id
        )
        .order_by(
            Assessment.id.desc()
        )
        .all()
    )

    return {
        "status": "success",
        "total_assessments": len(assessments),
        "assessments": [
            {
                "assessment_id": assessment.id,
                "roadmap_item_id": assessment.roadmap_item_id,
                "topic": assessment.topic,
                "score": assessment.score,
                "status": assessment.status
            }
            for assessment in assessments
        ]
    }