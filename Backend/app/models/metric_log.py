import uuid
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.time import now_ist

class MetricLog(Base):
    """
    A bridge table mapping dynamic commitment metrics to a specific daily entry.
    Example: User logs 4.0 hours (value) for "Deep Work" (metric_id) on Tuesday (daily_entry_id).
    """
    __tablename__ = "metric_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    daily_entry_id = Column(UUID(as_uuid=True), ForeignKey("daily_entries.id", ondelete="CASCADE"), nullable=False)
    metric_id = Column(UUID(as_uuid=True), ForeignKey("tracking_metrics.id", ondelete="CASCADE"), nullable=False)

    value = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), default=now_ist)

    #Relationship
    daily_entry = relationship("DailyEntry", back_populates="metric_logs")
    metric = relationship("TrackingMetric", back_populates="logs")
