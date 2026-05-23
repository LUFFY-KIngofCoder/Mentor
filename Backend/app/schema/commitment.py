from pydantic import BaseModel
from datetime import date
from uuid import UUID
from datetime import datetime

class CommitmentCreate(BaseModel):
    title: str
    description: str | None = None
    duration_days: int
    start_date: date


class CommitmentResponse(BaseModel):
    id: UUID
    user_id: UUID

    title: str
    description: str | None
    duration_days: int

    start_date: date
    end_date: date

    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommitmentUpdate(BaseModel):
    title: str | None = None

    description: str | None = None

    duration_days: int | None = None

    start_date: date | None = None
