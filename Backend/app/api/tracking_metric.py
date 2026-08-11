from sqlalchemy import select
from app.models.commitment import Commitment
from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, TrackingMetric
from app.schema.tracking_metric import TrackingMetricCreate, TrackingMetricResponse

router = APIRouter(
    prefix="/commitments/{commitment_id}/metrics",
    tags=["Tracking Metrics"]
)

async def get_user_commitment(
    commitment_id: UUID,
    current_user: User,
    db: AsyncSession
):

    result = await db.execute(select(Commitment).filter_by(id=commitment_id, user_id=current_user.id))
    commitment = result.scalar_one_or_none()
    if not commitment:
        raise HTTPException(status_code=404,
        detail="Commitment not found")

    return commitment

@router.post("/", response_model=TrackingMetricResponse)
async def create_metric(
    commitment_id: UUID,
    metric_in: TrackingMetricCreate,
    db:AsyncSession = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    commitment = await get_user_commitment(commitment_id, current_user, db)

    new_metric = TrackingMetric(
        commitment_id=commitment.id,
        name=metric_in.name,
        metric_type=metric_in.metric_type,
        operator=metric_in.operator,
        target_value=metric_in.target_value
    )

    db.add(new_metric)
    await db.commit()
    await db.refresh(new_metric)
    
    return new_metric


@router.get("/", response_model=List[TrackingMetricResponse])
async def get_metrics(
    commitment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    result = await db.execute(select(TrackingMetric
                                ).join(Commitment, Commitment.id==TrackingMetric.commitment_id
                                ).filter(Commitment.user_id==current_user.id,
                                         TrackingMetric.commitment_id==commitment_id)
                                )
    metrics = result.scalars().all()
    
    return metrics