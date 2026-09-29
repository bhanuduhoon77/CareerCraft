from sqlalchemy import Column, Integer, String, Text, ForeignKey

from backend.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    company = Column(
        String(200),
        nullable=False
    )

    location = Column(
        String(200)
    )

    description = Column(
        Text
    )

    required_skills = Column(
        Text
    )

    apply_url = Column(
        String(500),
        nullable=False
    )

    source = Column(
        String(100)
    )

    career_id = Column(
        Integer,
        ForeignKey("careers.id"),
        nullable=True
    )