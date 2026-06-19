from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Date, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.time import now_ist

class DailyEntry(Base):
    """
    Stores the daily check-in. Includes fixed behaviors and subjective reflections.
    Enforces temporal integrity: Only one entry per calendar date per user.
    """
    __tablename__ = "daily_entries"

    id = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid = True), ForeignKey("users.id"), nullable=False)

    # This is a Date (YYYY-MM-DD), not a DateTime, because it represents the behavioral day!
    date = Column(Date, nullable=False)

    #Core quantitative metrics
    sleep_hours = Column(Float, nullable = False)
    deep_work_hours = Column(Float, nullable = True)
    distraction_hours = Column(Float, nullable = True)
    mood_score = Column(Integer, nullable = True)
    energy_score = Column(Integer, nullable = True)

    # Qualitative reflection data
    journal_entry = Column(String, nullable=True)
    what_avoided = Column(String, nullable=True)
    biggest_win = Column(String, nullable=True)
    biggest_failure = Column(String, nullable=True)
    what_can_be_different = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=now_ist)
    updated_at = Column(DateTime(timezone=True), default=now_ist, onupdate=now_ist)

    #Relationships
    user = relationship("User", back_populates="daily_entries")
    metric_logs = relationship("MetricLog", back_populates="daily_entry", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("user_id", "date", name = "uq_user_daily_entry"),
    )

