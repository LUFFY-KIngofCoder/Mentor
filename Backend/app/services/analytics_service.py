from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from datetime import timedelta
from uuid import UUID
from typing import List

from app.models import User, Commitment, DailyEntry, MetricLog, TrackingMetric
from app.utils.time import now_ist
from app.core.exceptions import NotFoundException
from app.schema.analytics import AnalyticMetrics, CommitmentAnalyticsResponse

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_streak(self, current_user: User) -> List[CommitmentAnalyticsResponse]:
        # Get active commitments
        result = await self.db.execute(select(Commitment).filter_by(user_id=current_user.id, status='active'))
        active_commitments = result.scalars().all()

        if not active_commitments:
            raise NotFoundException(message="No active commitments found to calculate streak.")

        commitment_analytics = []

        for commitment in active_commitments:

            # Calculate active days
            required_metric_count = await self.db.execute(select(func.count(TrackingMetric.id)).filter_by(commitment_id=commitment.id)) 
            required_metric_count = required_metric_count.scalar()

            start_date = commitment.start_date
            total_active_days = (now_ist().date() - start_date).days + 1

            # Calculate streak logic
            result1 = await self.db.execute(select(DailyEntry.date)
                                        .join(MetricLog, DailyEntry.id == MetricLog.daily_entry_id)
                                        .join(TrackingMetric, and_(MetricLog.metric_id == TrackingMetric.id, TrackingMetric.commitment_id==commitment.id))
                                        .filter(
                                            DailyEntry.user_id == current_user.id,
                                            MetricLog.is_successful == True,
                                            DailyEntry.date >= start_date,
                                        ).group_by(DailyEntry.date)
                                        .having(func.count(MetricLog.id) == required_metric_count)
                                        .order_by(desc(DailyEntry.date)))

            successful_dates = result1.scalars().all()
            successful_days = len(successful_dates)
            consistency_score = (successful_days / total_active_days) * 100 if total_active_days > 0 else 0

            if successful_dates:
                last_date = now_ist().date() if successful_dates[0] == now_ist().date() else now_ist().date() - timedelta(days=1)
            
            streak = 0
            for date in successful_dates:
                if date == last_date:
                    streak += 1
                    last_date -= timedelta(days=1)
                else:
                    break

            commitment_analytics.append(
                CommitmentAnalyticsResponse(
                    commitment_id=commitment.id,
                    commitment_title=commitment.title,
                    analytic=AnalyticMetrics(
                        total_active_days=total_active_days,
                        successful_days=successful_days,
                        consistency_score=round(consistency_score, 2),
                        streak=streak,
                    )
                )
            ) 
            
        return commitment_analytics
