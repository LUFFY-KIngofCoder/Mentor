from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, DailyEntry, MetricLog, TrackingMetric
from app.schema.daily_entry import DailyEntryCreate, DailyEntryResponse
from app.utils.metric import evaluate_metric_success

router = APIRouter(
    prefix="/daily-entries",
    tags = ["Daily Entries"]
)

@router.post("/", response_model=DailyEntryResponse)
async def create_or_update_daily_entry(
    entry_in: DailyEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. UPSERT LOGIC: Does a Daily Entry already exist for today?

    result1 = await db.execute(
        select(DailyEntry).where(
            DailyEntry.user_id == current_user.id,
            DailyEntry.date == entry_in.date
        ).options(selectinload(DailyEntry.metric_logs))
    )
    entry = result1.scalar_one_or_none()
    
    if entry:
        # IT EXISTS: (e.g. ticking off the 2nd habit, or doing evening reflection)
        # We UPDATE the existing entry with any new data they sent
        update_data = entry_in.model_dump(exclude_unset=True, exclude={"custom_metrics", "date"})
        for key, value in update_data.items():
            setattr(entry, key, value)
    else:
        # IT DOES NOT EXIST: (e.g. their 1st habit of the day)
        # We CREATE a new draft entry
        entry = DailyEntry(
            user_id=current_user.id,
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
        db.add(entry)
        await db.flush() # Instantly generate the ID so we can use it below
        
    # 2. METRIC LOG UPSERT LOGIC
    for custom_metric in entry_in.custom_metrics:
        # Did they already log this specific metric today?

        result3 = await db.execute(
            select(TrackingMetric).where(
                TrackingMetric.id == custom_metric.metric_id
            )
        )
        tracking_metric = result3.scalar_one_or_none()

        if not tracking_metric:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Tracking metric {custom_metric.metric_id} not found."
            )

        is_successful = evaluate_metric_success(
            value = custom_metric.value,
            operator = tracking_metric.operator,
            target = tracking_metric.target_value
        )


        result2 = await db.execute(
            select(MetricLog).where(
                MetricLog.daily_entry_id == entry.id,
                MetricLog.metric_id == custom_metric.metric_id
            )
        )
        existing_log = result2.scalar_one_or_none()
        
        if existing_log:
            # They are updating an existing log (e.g. studied 2 hours, now changed to 4)
            existing_log.value = custom_metric.value
            existing_log.is_successful = is_successful
        else:
            # First time checking off this specific metric today
            new_log = MetricLog(
                daily_entry_id=entry.id,
                metric_id=custom_metric.metric_id,
                value=custom_metric.value,
                is_successful=is_successful
            )
            db.add(new_log)

    await db.commit()
    result_final = await db.execute(
                                    select(DailyEntry)
                                    .where(DailyEntry.id == entry.id)
                                    .options(selectinload(DailyEntry.metric_logs))
                                )
    entry = result_final.scalar_one()
                                    
    return entry

@router.get("/", response_model = List[DailyEntryResponse])
async def get_daily_entries(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result3 = await db.execute(
        select(DailyEntry).where(
            DailyEntry.user_id == current_user.id
        ).options(selectinload(DailyEntry.metric_logs))
    )

    entries = result3.scalars().all()

    return entries