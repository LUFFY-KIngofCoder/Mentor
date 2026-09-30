from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date

from app.schema.user import UserResponse
from app.schema.commitment import CommitmentResponse
from app.schema.analytics import CommitmentAnalyticsResponse

class DashboardResponse(BaseModel):
    user: UserResponse
    active_commitments: List[CommitmentResponse]
    missed_days: List[date]
    logs: List[Dict[str, Any]]
    analytics: List[CommitmentAnalyticsResponse]
