from sqlalchemy import desc, func,select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import timedelta
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.auth.oauth2 import get_current_user
from app.models import User, Commitment, MetricLog, DailyEntry
from app.schema.commitment import CommitmentResponse
from app.utils.time import now_ist
from app.schema.analytics import CommitmentAnalyticsResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/", response_model=List[CommitmentAnalyticsResponse])
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = await db.execute(select(Commitment).filter(
        Commitment.user_id == current_user.id,
        Commitment.status == "active").options(selectinload(Commitment.metrics)))
    commitments = result.scalars().all()
    
    analytics = []
    
    for com in commitments:
        commitment = CommitmentResponse.model_validate(com).model_dump()
        
        total_active_days = min((now_ist().date() - commitment['start_date']).days + 1,com.duration_days)

        required_metric_count = len(com.metrics)


        result1 = await db.execute(select(DailyEntry.date
                                    ).join(MetricLog, MetricLog.daily_entry_id == DailyEntry.id
                                    ).filter(
                                        DailyEntry.user_id == current_user.id,
                                        MetricLog.metric_id.in_([m.id for m in com.metrics]),
                                        MetricLog.is_successful == True
                                    ).group_by(DailyEntry.date
                                    ).having(
                                        func.count(MetricLog.id) == required_metric_count
                                    ).order_by(desc(DailyEntry.date)))

        successful_dates = result1.scalars().all()
                                                
        successful_days = len(successful_dates)
        
        consistency_score = (successful_days/total_active_days)*100

        if successful_dates:
            last_date = now_ist().date() if successful_dates[0] == now_ist().date() else now_ist().date() - timedelta(days=1)
        
        streak = 0
        for date in successful_dates:
            if date == last_date:
                streak+=1
                last_date -= timedelta(days=1)
            else:
                break 
        
        analytic = {"commitment_id" : com.id,
                    "commitment_title": com.title,
                    "analytic": {
                        "total_active_days": total_active_days,
                        "successful_days": successful_days,
                        "consistency_score": consistency_score,
                        "streak": streak,
                        }}
        analytics.append(analytic)
    

    return analytics
        
            

