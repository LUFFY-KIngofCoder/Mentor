from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import DailyEntry, TrackingMetric, MetricLog

class DailyEntryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_daily_entry_by_date(self,date:date, current_user_id: UUID) -> DailyEntry | None:
        entry = await self.db.execute(
            select(DailyEntry).where(
                DailyEntry.user_id == current_user_id,
                DailyEntry.date == date
            ).options(selectinload(DailyEntry.metric_logs))
        )
        return entry.scalar_one_or_none()
    
    async def add_draft_entry(self, entry:DailyEntry) -> DailyEntry:
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def get_metric_logs_by_id(self, metric_id: UUID, daily_entry_id: UUID) -> MetricLog | None:
        result = await self.db.execute(select(MetricLog).where(MetricLog.metric_id == metric_id, MetricLog.daily_entry_id == daily_entry_id))
        return result.scalar_one_or_none()

    async def add_new_logs(self, logs:List[MetricLog]) -> None :
        self.db.add_all(logs)
        await self.db.commit()


    async def get_daily_entry_by_id(self, entry_id:UUID, current_user_id:UUID) -> DailyEntry | None:
        result = await self.db.execute(select(DailyEntry).where(DailyEntry.id == entry_id, DailyEntry.user_id == current_user_id).options(selectinload(DailyEntry.metric_logs)))
        return result.scalar_one_or_none()
    
    async def get_daily_entry_by_user_id(self, user_id:UUID) -> List[DailyEntry] | None:
        result = await self.db.execute(select(DailyEntry).where(DailyEntry.user_id == user_id).options(selectinload(DailyEntry.metric_logs)))
        return result.scalars().all()

    async def get_last_daily_entry_date(self, user_id:UUID) -> date | None:
        result = await self.db.execute(select(DailyEntry.date).where(DailyEntry.user_id == user_id).order_by(DailyEntry.date.desc()).limit(1))
        return result.scalar_one_or_none()