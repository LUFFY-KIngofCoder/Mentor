from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class TrackingMetricCreate(BaseModel):
    name:str
    metric_type: str
    operator: str = ">="
    target_value: float

class TrackingMetricUpdate(BaseModel):
    name: Optional[str] = None
    target_value: Optional[float] = None
    operator: Optional[str] = None

class TrackingMetricResponse(TrackingMetricCreate):
    id: UUID
    commitment_id: UUID

    model_config = ConfigDict(from_attributes=True)