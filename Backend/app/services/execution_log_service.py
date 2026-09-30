from typing import List, Dict, Any
from uuid import UUID

from app.schema.daily_entry import DailyEntryResponse
from app.schema.missed_day_reflection import MissedDayReflectionResponse
from app.repositories.daily_entry_repository import DailyEntryRepository
from app.repositories.missed_day_repository import MissedDayRepository

class ExecutionLogService:
    def __init__(self, daily_entry_repo:DailyEntryRepository, missed_day_repo:MissedDayRepository):
        self.daily_entry_repo = daily_entry_repo
        self.missed_day_repo = missed_day_repo

    async def get_unified_execution_logs(self, current_user_id: UUID) -> List[Dict[str, Any]]:
        
        entries = await self.daily_entry_repo.get_daily_entry_by_user_id(current_user_id)
        missed_days = await self.missed_day_repo.get_missed_days_by_user_id(current_user_id)
        
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
        