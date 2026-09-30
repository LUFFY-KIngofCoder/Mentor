from typing import List
from fastapi import APIRouter, Depends
import asyncio

from app.core.dependencies import get_commitment_service, get_missed_day_service,get_execution_log_service,get_analytics_service
from app.auth.oauth2 import get_current_user
from app.models import User
from app.services.commitment_service import CommitmentService
from app.services.missed_day_service import MissedDayService
from app.services.execution_log_service import ExecutionLogService
from app.services.analytics_service import AnalyticsService
from app.schema.dashboard import DashboardResponse
from app.schema.user import UserResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/" ,response_model=DashboardResponse)
async def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    commitment_service: CommitmentService = Depends(get_commitment_service),
    missed_day_service: MissedDayService = Depends(get_missed_day_service),
    execution_log_service: ExecutionLogService = Depends(get_execution_log_service),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    active, missed, logs, analytics = await asyncio.gather(
        commitment_service.get_user_commitments(current_user.id, limit=50, cursor=None, status="active"),
        missed_day_service.get_unresolved_missed_days(current_user),
        execution_log_service.get_unified_execution_logs(current_user.id),
        analytics_service.calculate_streak(current_user)
    )

    return DashboardResponse(
        user=UserResponse.model_validate(current_user),
        active_commitments=active[0],
        missed_days=missed,
        logs=logs,
        analytics=analytics
    )