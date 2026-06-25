from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from uuid import UUID

class MissedDayReflectionCreate(BaseModel):
    missed_date:date
    reason: str
    reflection: str

class MissedDayReflectionResponse(MissedDayReflectionCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    