from urllib3 import response
from ast import operator
from typing import List
from uuid import UUID
from redis.asyncio import Redis
from datetime import date
import json


from app.schema.daily_entry import DailyEntryCreate, DailyEntryResponse, MetricLogCreate
from app.models import DailyEntry, MetricLog
from app.core.exceptions import NotFoundException
from app.repositories.daily_entry_repository import DailyEntryRepository
from app.repositories.commitment_repository import CommitmentRepository

class DailyEntryService:
    def __init__(self, daily_entry_repo: DailyEntryRepository, commitment_repo: CommitmentRepository , redis: Redis):
        self.daily_entry_repo = daily_entry_repo
        self.commitment_repo = commitment_repo
        self.redis = redis
    
    async def daily_entry_upsert(self, entry_in: DailyEntryCreate, current_user_id: UUID) -> DailyEntryResponse:
        existing_entry = await self.daily_entry_repo.get_daily_entry_by_date(entry_in.date, current_user_id)
        
        if existing_entry:
            update_data = entry_in.model_dump(exclude_unset=True, exclude_none=True, exclude={"custom_metrics", "date"})
            for key, value in update_data.items():
                setattr(existing_entry, key, value)
            return existing_entry        
        else:
            entry = DailyEntry(
                                user_id=current_user_id,
                                date=entry_in.date,
                                sleep_hours=entry_in.sleep_hours,
                                deep_work_hours=entry_in.deep_work_hours,
                                distraction_hours=entry_in.distraction_hours,
                                mood_score=entry_in.mood_score,
                                energy_score=entry_in.energy_score,
                                journal_entry=entry_in.journal_entry,
                                what_avoided=entry_in.what_avoided,
                                biggest_win=entry_in.biggest_win,
                                biggest_failure=entry_in.biggest_failure,
                                what_can_be_different=entry_in.what_can_be_different
                            )
            return await self.daily_entry_repo.add_draft_entry(entry)

    @staticmethod
    def evaluate_metric_success(value: float,operator: str,target: float) -> bool:
        if operator == ">=" and value >= target:
            return True
        elif operator == "<=" and value <= target:
            return True
        elif operator == "==" and value == target:
            return True
        return False

    async def metric_logs_upsert(self, custom_metrics: List[MetricLogCreate], daily_entry_id: UUID, current_user_id:UUID , date: date) -> None:
        metric_logs_to_add = []

        for metric_log_item in custom_metrics:
            tracking_metric = await self.commitment_repo.get_tracking_metric_by_id(metric_log_item.metric_id, current_user_id)
            
            if not tracking_metric:
                raise NotFoundException(f"Tracking metric {metric_log_item.metric_id} not found.")
            
            is_successful = self.evaluate_metric_success(
                                        value=metric_log_item.value,
                                        operator=tracking_metric.operator,
                                        target=tracking_metric.target_value
            )

            existing_log = await self.daily_entry_repo.get_metric_logs_by_id(metric_log_item.metric_id, daily_entry_id)
            
            if existing_log:
                existing_log.value = metric_log_item.value
                existing_log.is_successful = is_successful
            else:
                metric_logs_to_add.append(MetricLog(
                    daily_entry_id=daily_entry_id,
                    metric_id=metric_log_item.metric_id,
                    value=metric_log_item.value,
                    is_successful=is_successful
                    )
                )
        await self.daily_entry_repo.add_new_logs(metric_logs_to_add)

        await self.redis.delete(f"user:{current_user_id}:streak")
        await self.redis.delete(f"daily_entry:{date}:{current_user_id}")
    
    async def get_daily_entry_by_date(self, date: date, current_user_id: UUID) -> DailyEntryResponse | None:
        cache_key = f"daily_entry:{date}:{current_user_id}"
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return DailyEntryResponse.model_validate_json(cached_data)

        entry = await self.daily_entry_repo.get_daily_entry_by_date(date, current_user_id)
        if not entry:
            return None
        
        response = DailyEntryResponse.model_validate(entry)

        await self.redis.set(cache_key, response.model_dump_json(), ex=300)
        return response