from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func

from backend.database import Base


class ResumeAnalysis(Base):

    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(String(255))

    education = Column(JSON)
    skills = Column(JSON)
    experience = Column(JSON)
    projects = Column(JSON)
    certifications = Column(JSON)
    career_preferences = Column(JSON)
    strengths = Column(JSON)
    missing_skills = Column(JSON)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )