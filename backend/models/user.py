from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    # Selected career of the user
    career_id = Column(
        Integer,
        ForeignKey("careers.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )