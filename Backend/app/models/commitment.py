import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.time import now_ist

class Commitment(Base):
    __tablename__ = "commitments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)

    description = Column(String, nullable=True)

    duration_days = Column(Integer, nullable=False)

    start_date = Column(Date, nullable=False)

    end_date = Column(Date, nullable=False)

    status = Column(String, nullable=False, default="active")

    created_at = Column(DateTime(timezone=True), default=now_ist)

    updated_at = Column(DateTime(timezone=True), default=now_ist, onupdate=now_ist)

    user = relationship("User", back_populates="commitments")