from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime

from backend.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    extracted_text = Column(
        Text,
        nullable=True
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )