from fastapi import FastAPI
from sqlalchemy import text
from backend.api.roadmap import router as roadmap_router

from backend.database import Base, engine

# Import models so SQLAlchemy knows about them
from backend.models.user import User
from backend.models.profile import Profile
from backend.models.skill import Skill, UserSkill
from backend.models.career import Career, CareerSkill
from backend.models.roadmap import Roadmap, RoadmapItem
from backend.models.assessment import Assessment
from backend.api.auth import router as auth_router
from backend.models.resume import Resume
from backend.api.resume import router as resume_router
from backend.api.career import router as career_router
from backend.api.assessment import router as assessment_router
from backend.models.resume_analysis import ResumeAnalysis
from backend.models.job import Job
from backend.api.job import router as job_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CareerCraft API",
    description="AI-Powered Career Intelligence Platform",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(roadmap_router)
app.include_router(career_router)
app.include_router(assessment_router)
app.include_router(job_router)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "CareerCraft API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "success",
            "message": "MySQL connected successfully!"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }