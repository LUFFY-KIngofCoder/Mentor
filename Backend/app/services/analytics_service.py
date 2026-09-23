from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import timedelta
from uuid import UUID

from app.models import User, Commitment, DailyEntry, MetricLog
from app.utils.time import now_ist
from app.core.exceptions import NotFoundException

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_streak(self, current_user: User) -> dict:
        # Get active commitments
        result = await self.db.execute(select(Commitment).filter_by(user_id=current_user.id, status='active'))
        active_commitments = result.scalars().all()

        if not active_commitments:
            raise NotFoundException(message="No active commitments found to calculate streak.")

        required_metric_count = len(active_commitments)
        
        # Calculate active days
        start_dates = [c.start_date for c in active_commitments]
        earliest_start = min(start_dates) if start_dates else now_ist().date()
        total_active_days = (now_ist().date() - earliest_start).days + 1

        # Calculate streak logic
        result1 = await self.db.execute(select(DailyEntry.date)
                                    .join(MetricLog, DailyEntry.id == MetricLog.daily_entry_id)
                                    .filter(
                                        DailyEntry.user_id == current_user.id,
                                        MetricLog.is_successful == True,
                                        DailyEntry.date >= earliest_start
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

        return {
            "current_streak": streak,
            "total_active_days": total_active_days,
            "consistency_score": round(consistency_score, 2),
            "successful_days": successful_days,
            "required_daily_metrics": required_metric_count,
        }
