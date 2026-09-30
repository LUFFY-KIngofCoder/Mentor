from fastapi import APIRouter, Depends
from typing import List
from datetime import date

from app.auth.oauth2 import get_current_user
from app.models import User
from app.schema.daily_entry import DailyEntryCreate, DailyEntryResponse
from app.core.dependencies import get_daily_entry_service
from app.services.daily_entry_service import DailyEntryService
from app.core.idempotency import check_idempotency

router = APIRouter(
    prefix="/daily-entries",
    tags = ["Daily Entries"]
)

@router.post("/", response_model=DailyEntryResponse, dependencies=[Depends(check_idempotency)])
async def create_or_update_daily_entry(
    entry_in: DailyEntryCreate,
    daily_entry_service: DailyEntryService = Depends(get_daily_entry_service),
    current_user: User = Depends(get_current_user)
):
    entry = await daily_entry_service.daily_entry_upsert(entry_in,current_user.id)
    await daily_entry_service.metric_logs_upsert(entry_in.custom_metrics,entry.id,current_user.id, entry_in.date)
    entry = await daily_entry_service.daily_entry_repo.get_daily_entry_by_id(entry.id, current_user.id)
    return DailyEntryResponse.model_validate(entry)
                            

@router.get("/", response_model = List[DailyEntryResponse])
async def get_daily_entries(
    daily_entry_service:DailyEntryService = Depends(get_daily_entry_service),
    current_user: User = Depends(get_current_user)
):

    entries = await daily_entry_service.daily_entry_repo.get_daily_entry_by_user_id(current_user.id)
    return entries

@router.get("/date", response_model = DailyEntryResponse | None)
async def get_daily_entry_by_date(
    date: date,
    daily_entry_service:DailyEntryService = Depends(get_daily_entry_service),
    current_user: User = Depends(get_current_user)
):
    return await daily_entry_service.get_daily_entry_by_date(date, current_user.id)