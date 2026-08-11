from pydantic import BaseModel
from uuid import UUID

class AnalyticMetrics(BaseModel):
    total_active_days: int
    successful_days: int
    consistency_score: float
    streak: int

class CommitmentAnalyticsResponse(BaseModel):
    commitment_id: UUID
    commitment_title: str
    analytic: AnalyticMetrics