from fastapi import APIRouter, Depends
from typing import List
from app.auth.oauth2 import get_current_user
from app.models import User
from app.core.dependencies import get_analytics_service
from app.services.analytics_service import AnalyticsService
from app.schema.analytics import CommitmentAnalyticsResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/streak")
async def calculate_streak(
    current_user: User = Depends(get_current_user),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> List[CommitmentAnalyticsResponse]:
    return await analytics_service.calculate_streak(current_user)
