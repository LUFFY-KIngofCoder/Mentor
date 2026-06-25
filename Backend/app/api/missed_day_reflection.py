from sqlalchemy.exc import IntegrityError
from app.schema.missed_day_reflection import MissedDayReflectionCreate, MissedDayReflectionResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, date
from typing import List

from app.db.session import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, Commitment, DailyEntry, MissedDayReflection
from app.utils.time import now_ist

router = APIRouter(
    prefix="/missed-days", 
    tags=["Missed Days"]
    )

@router.get("/unresolved", response_model=List[date])
def get_unresolved_missed_days(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Figure out "Behavioral Yesterday"
    behavioral_today_datetime= now_ist() - timedelta(hours=current_user.day_reset_hour)
    
    behavioral_yesterday = (behavioral_today_datetime-timedelta(days=1)).date()

    # 2. Get the very first commitment start date
    first_commitment = db.query(Commitment).filter(
        Commitment.user_id == current_user.id
    ).order_by(Commitment.start_date.asc()).first()

    if not first_commitment or first_commitment.start_date > behavioral_yesterday:
        return [] # No commitments, or they just started today

    start_date = first_commitment.start_date

    # --- YOUR TURN: BUILD THE ALGORITHM ---

    # Step 3: Generate expected_dates set from start_date to behavioral_yesterday (inclusive)
    expected_dates = {start_date+timedelta(days=i) for i in range((behavioral_yesterday-start_date).days+1)}
    
    # Step 4: Run 1 query to get all dates from DailyEntry for this user
    daily_entry_dates = {row[0] for row in db.query(DailyEntry.date).filter(
        DailyEntry.user_id == current_user.id
        ).all()}
    
    # Step 5: Run 1 query to get all missed_dates from MissedDayReflection for this user
    missed_day_dates = {row[0] for row in db.query(MissedDayReflection.missed_date).filter(
        MissedDayReflection.user_id == current_user.id
        ).all()}
    
    # Step 6: Combine them into logged_dates set
    logged_dates = daily_entry_dates | missed_day_dates
    
    # Step 7: missing_dates = expected_dates - logged_dates

    missing_dates = list(expected_dates - logged_dates)

    return sorted(missing_dates)


@router.post("/", response_model = MissedDayReflectionResponse)
def missed_day_reflection(
    reflection: MissedDayReflectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    new_reflection = MissedDayReflection(
        user_id=current_user.id,
        missed_date=reflection.missed_date,
        reason=reflection.reason,
        reflection=reflection.reflection
    )
    try:
        db.add(new_reflection)
        db.commit()
        db.refresh(new_reflection)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already logged a reflection for this date")

    return new_reflection