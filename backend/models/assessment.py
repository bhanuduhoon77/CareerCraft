from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float

from backend.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    roadmap_item_id = Column(
        Integer,
        ForeignKey("roadmap_items.id"),
        nullable=True
    )

    topic = Column(String(150), nullable=False)

    questions = Column(Text)
    answers = Column(Text)

    score = Column(Float, default=0.0)

    status = Column(
        String(50),
        default="pending"
    )