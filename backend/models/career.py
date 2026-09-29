from sqlalchemy import Column, Integer, String, Text, ForeignKey

from backend.database import Base


class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(100))


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id = Column(Integer, primary_key=True, index=True)

    career_id = Column(
        Integer,
        ForeignKey("careers.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )

    importance = Column(String(50))
    required_proficiency = Column(Integer, default=50)