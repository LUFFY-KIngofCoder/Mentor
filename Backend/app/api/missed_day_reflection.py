from app.core.exceptions import BadRequestException
from sqlalchemy.exc import IntegrityError
from app.schema.missed_day_reflection import MissedDayReflectionCreate, MissedDayReflectionResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta, date
from typing import List

from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, Commitment, DailyEntry, MissedDayReflection
from app.utils.time import now_ist
from app.core.dependencies import get_missed_day_service
from app.services.missed_day_service import MissedDayService

router = APIRouter(
    prefix="/missed-days", 
    tags=["Missed Days"]
    )

@router.get("/unresolved", response_model=List[date])
async def get_unresolved_missed_days(
    missed_day_service: MissedDayService = Depends(get_missed_day_service),
    current_user: User = Depends(get_current_user)
):
   return await missed_day_service.get_unresolved_missed_days(current_user)


@router.post("/", response_model = MissedDayReflectionResponse)
async def missed_day_reflection(
    reflection: MissedDayReflectionCreate,
    missed_day_service: MissedDayService = Depends(get_missed_day_service),
    current_user: User = Depends(get_current_user)
):
    
    new_reflection = MissedDayReflection(
        user_id=current_user.id,
        missed_date=reflection.missed_date,
        reason=reflection.reason,
        reflection=reflection.reflection
    )
  
    return await missed_day_service.create_missed_day_reflection(new_reflection)
    