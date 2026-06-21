from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date
from uuid import UUID

# 1. The Schema for an individual Metric Log
class MetricLogCreate(BaseModel):
    metric_id: UUID
    value: float

class MetricLogResponse(MetricLogCreate):
    id: UUID
    daily_entry_id: UUID
    
    model_config = ConfigDict(from_attributes=True)


# 2. The Schema for creating a Daily Entry (The big payload from the frontend)
class DailyEntryCreate(BaseModel):
    date: date
    sleep_hours: Optional[float] = None
    deep_work_hours: Optional[float] = None
    distraction_hours: Optional[float] = None
    mood_score: Optional[int] = None
    energy_score: Optional[int] = None
    
    journal_entry: Optional[str] = None
    what_avoided: Optional[str] = None
    biggest_win: Optional[str] = None
    biggest_failure: Optional[str] = None
    what_can_be_different: Optional[str] = None
    
    # Notice this! The frontend sends a list of metric logs ALONG WITH the daily entry!
    custom_metrics: List[MetricLogCreate] = []


# 3. The Schema for returning the Daily Entry back to the frontend
class DailyEntryResponse(DailyEntryCreate):
    id: UUID
    user_id: UUID
    
    # When returning, we give them the full logs with their IDs
    metric_logs: List[MetricLogResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
