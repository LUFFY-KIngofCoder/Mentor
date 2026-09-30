from app.core.exceptions import BadRequestException
from sqlalchemy.exc import IntegrityError
from app.schema.missed_day_reflection import MissedDayReflectionCreate, MissedDayReflectionResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta, date
from typing import List

from app.models import User, Commitment, DailyEntry, MissedDayReflection
from app.utils.time import now_ist
from app.repositories.daily_entry_repository import DailyEntryRepository
from app.repositories.commitment_repository import CommitmentRepository
from app.repositories.missed_day_repository import MissedDayRepository

class MissedDayService:
    def __init__(self,missed_day_repo:MissedDayRepository, daily_entry_repo: DailyEntryRepository, commitment_repo: CommitmentRepository):
        self.missed_day_repo = missed_day_repo
        self.daily_entry_repo = daily_entry_repo
        self.commitment_repo = commitment_repo
    
    async def get_unresolved_missed_days(self, current_user: User) -> List[date]:

        behavioral_today_datetime= now_ist() - timedelta(hours=current_user.day_reset_hour)
    
        behavioral_yesterday = (behavioral_today_datetime-timedelta(days=1)).date()

        # 2. Get the very first commitment start date
        first_commitment = await self.commitment_repo.get_oldest_active_commitment(current_user.id)

        if not first_commitment or first_commitment.start_date > behavioral_yesterday:
            return [] 

        # Step 4: Run 1 query to get all dates from DailyEntry for this user
        last_daily_entry_dates = await self.daily_entry_repo.get_last_daily_entry_date(current_user.id)

        # Step 5: Run 1 query to get all missed_dates from MissedDayReflection for this user
        last_missed_day_dates = await self.missed_day_repo.get_last_missed_day(current_user.id)
        
        last_logged_date = max(last_daily_entry_dates, last_missed_day_dates) if (last_missed_day_dates!=None and last_daily_entry_dates!=None) else last_daily_entry_dates or last_missed_day_dates
        
        missing_dates = [behavioral_yesterday] if ((not last_logged_date) or (last_logged_date < behavioral_yesterday)) else []

        return missing_dates

    async def create_missed_day_reflection(self, new_reflection: MissedDayReflection) -> MissedDayReflectionResponse:
        try:
            new_reflection = await self.missed_day_repo.add_missed_day_reflection(new_reflection)
            return new_reflection
        except IntegrityError:
            raise BadRequestException("You have already logged a reflection for this date")