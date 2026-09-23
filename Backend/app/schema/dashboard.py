from pydantic import BaseModel
from typing import List
from app.schema.user import UserResponse
from app.schema.commitment import CommitmentResponse
from app.schema.analytics import CommitmentAnalyticsResponse

class DashboardResponse(BaseModel):
    user: UserResponse
    active_commitments: List[CommitmentResponse]
    analytics: List[CommitmentAnalyticsResponse]
