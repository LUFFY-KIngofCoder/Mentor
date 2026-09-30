from app.models import TrackingMetric
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime

from app.models.commitment import Commitment

class CommitmentRepository:

    def __init__(self, db : AsyncSession):
        self.db = db

    async def create(self, commitment: Commitment) -> Commitment:
        self.db.add(commitment)
        await self.db.commit()
        await self.db.refresh(commitment)

        return commitment

    async def get_by_id(self, commitment_id: UUID) -> Commitment | None:
        result = await self.db.execute(select(Commitment).filter(Commitment.id == commitment_id))
        commitment = result.scalars().one_or_none()
        return commitment

    async def get_all_for_user(
        self, user_id: UUID, limit: int = 10, cursor: datetime | None = None, status: str | None = None
    ) -> tuple[list[Commitment], datetime | None]:
        
        query = select(Commitment).filter(Commitment.user_id == user_id)
        
        if status:
            query = query.filter(Commitment.status == status)
        # 1. Apply Cursor (Give me items created BEFORE the cursor timestamp)
        if cursor:
            query = query.filter(Commitment.created_at < cursor)
            
        # 2. ALWAYS sort by Newest First, and apply the limit
        query = query.order_by(Commitment.created_at.desc()).limit(limit)
        
        result = await self.db.execute(query)
        commitments = list(result.scalars().all())
        
        # 3. Figure out what the next cursor is for the frontend
        next_cursor = commitments[-1].created_at if len(commitments) == limit else None
        
        return commitments, next_cursor
        
    async def update(self,commitment:Commitment) -> Commitment:
        await self.db.commit()
        await self.db.refresh(commitment)
        return commitment
    
    async def delete(self,commitment:Commitment):
        await self.db.delete(commitment)
        await self.db.commit()
        return {
            "message": "Commitment deleted successfully"
        }

    async def get_tracking_metric_by_id(self, tracking_metric_id: UUID, current_user_id: UUID) -> TrackingMetric | None:
        result = await self.db.execute(select(TrackingMetric).where(TrackingMetric.id == tracking_metric_id, Commitment.user_id == current_user_id).join(Commitment, Commitment.id == TrackingMetric.commitment_id))
        return result.scalar_one_or_none()
    
    async def get_oldest_active_commitment(self, user_id: UUID) -> Commitment | None:
        result = await self.db.execute(select(Commitment).filter(Commitment.user_id==user_id, Commitment.status=="active").order_by(Commitment.start_date.asc()).limit(1))
        return result.scalar_one_or_none()