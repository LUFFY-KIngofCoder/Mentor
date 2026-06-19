import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class TrackingMetric(Base):
    """
    Represents a commitment-specific target metric (e.g., Deep Work >= 4 hours, gym = True).
    Allows dynamic custom behaviors rather than hardcoding static check-in columns.
    """
    __tablename__ = "tracking_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    commitment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("commitments.id", ondelete="CASCADE"),
        nullable=False
    )
    
    name = Column(String, nullable=False)            # e.g., "Deep Work", "Gym", "Smoking"
    metric_type = Column(String, nullable=False)     # e.g., "boolean", "float", "integer"
    operator = Column(String, nullable=False, default=">=")  # e.g., ">=", "<=", "=="
    target_value = Column(Float, nullable=False)     # e.g., 4.0, 1.0 (for True), 2.0

    # Relationships
    commitment = relationship("Commitment", back_populates="metrics")
    logs = relationship(
        "MetricLog",
        back_populates="metric",
        cascade="all, delete-orphan"
    )
