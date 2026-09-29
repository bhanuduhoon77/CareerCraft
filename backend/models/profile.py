from sqlalchemy import Column, Integer, String, Text, ForeignKey

from backend.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    education = Column(String(200))
    degree = Column(String(100))
    branch = Column(String(100))
    experience = Column(String(100))
    interests = Column(Text)
    preferred_career = Column(String(150))
    preferred_location = Column(String(150))
    learning_hours_per_week = Column(Integer)