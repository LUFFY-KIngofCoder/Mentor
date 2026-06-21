from app.models.commitment import Commitment
from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, TrackingMetric
from app.schema.tracking_metric import TrackingMetricCreate, TrackingMetricResponse

router = APIRouter(
    prefix="/commitments/{commitment_id}/metrics",
    tags=["Tracking Metrics"]
)

def get_user_commitment(
    commitment_id: UUID,
    current_user: User,
    db: Session
):
    commitment = db.query(Commitment).filter(
        Commitment.id == commitment_id,
        Commitment.user_id == current_user.id
    ).first()

    if not commitment:
        raise HTTPException(status_code=404,
        detail="Commitment not found")

    return commitment

@router.post("/", response_model=TrackingMetricResponse)
def create_metric(
    commitment_id: UUID,
    metric_in: TrackingMetricCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    commitment = get_user_commitment(commitment_id, current_user, db)

    new_metric = TrackingMetric(
        commitment_id=commitment.id,
        name=metric_in.name,
        metric_type=metric_in.metric_type,
        operator=metric_in.operator,
        target_value=metric_in.target_value
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    
    return new_metric


@router.get("/", response_model=List[TrackingMetricResponse])
def get_metrics(
    commitment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_user_commitment(commitment_id, current_user, db)

    metrics = db.query(TrackingMetric).filter(
        TrackingMetric.commitment_id == commitment_id
        ).all()
    
    return metrics