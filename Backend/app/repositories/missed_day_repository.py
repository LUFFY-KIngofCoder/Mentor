from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date
from app.models import MissedDayReflection
from sqlalchemy import select

class MissedDayRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_last_missed_day(self,current_user_id:UUID) -> date | None: 
        result = await self.db.execute(select(MissedDayReflection.missed_date).filter(
            MissedDayReflection.user_id == current_user_id
            ).order_by(MissedDayReflection.missed_date.desc()).limit(1))
        return result.scalar_one_or_none()   
    
    async def add_missed_day_reflection(self, reflection:MissedDayReflection) -> MissedDayReflection:
        self.db.add(reflection)
        await self.db.commit()
        await self.db.refresh(reflection)
        return reflection
    
    async def get_missed_days_by_user_id(self, user_id: UUID) -> MissedDayReflection | None:
        result = await self.db.execute(select(MissedDayReflection).where(MissedDayReflection.user_id == user_id))
        return result.scalars().all()