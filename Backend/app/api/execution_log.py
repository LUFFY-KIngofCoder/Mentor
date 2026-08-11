from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any
from sqlalchemy import select

from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, DailyEntry, MissedDayReflection
from app.schema.daily_entry import DailyEntryResponse
from app.schema.missed_day_reflection import MissedDayReflectionResponse

router = APIRouter(
    prefix="/execution-log",
    tags=["Execution Log"]
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_unified_execution_log(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result1 = await db.execute(select(DailyEntry).filter(DailyEntry.user_id == current_user.id).options(selectinload(DailyEntry.metric_logs)))

    entries = result1.scalars().all()
    
    result2 = await db.execute(select(MissedDayReflection).filter(MissedDayReflection.user_id == current_user.id))

    missed_days = result2.scalars().all()
    
    unified_log = []

    for entry in entries:

        entry_dict = DailyEntryResponse.model_validate(entry).model_dump()
        entry_dict['type'] = 'daily_entry'
        unified_log.append(entry_dict)
    
    for missed in missed_days:

        missed_dict = MissedDayReflectionResponse.model_validate(missed).model_dump()
        missed_dict['type'] = 'missed_day'
        missed_dict["date"] = missed_dict.pop("missed_date")
        unified_log.append(missed_dict)

    unified_log.sort(key=lambda x: x['date'], reverse=True)
    
    return unified_log
    