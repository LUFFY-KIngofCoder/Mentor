from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.utils.time import now_ist

class MissedDayReflection(Base):
    __tablename__ = "missed_day_reflections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    missed_date = Column(Date, nullable=False)

    reason = Column(String, nullable=False)
    reflection = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), default=now_ist)
    updated_at = Column(DateTime(timezone=True), default=now_ist, onupdate=now_ist)

    user = relationship("User", back_populates="missed_reflections")

    __table_args__ = (UniqueConstraint('user_id', 'missed_date', name='uq_user_missed_date'),)