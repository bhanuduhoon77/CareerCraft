from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float

from backend.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    career_id = Column(
        Integer,
        ForeignKey("careers.id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)
    description = Column(Text)

    progress = Column(Float, default=0.0)
    status = Column(String(50), default="active")


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)

    roadmap_id = Column(
        Integer,
        ForeignKey("roadmaps.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=True
    )

    title = Column(String(200), nullable=False)
    description = Column(Text)

    order_number = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")

    score = Column(Float, default=0.0)