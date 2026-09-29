from sqlalchemy import Column, Integer, String, Float, ForeignKey

from backend.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )

    proficiency = Column(Float, default=0.0)
    source = Column(String(50))