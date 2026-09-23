from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.repositories.commitment_repository import CommitmentRepository
from app.services.commitment_service import CommitmentService
from app.services.analytics_service import AnalyticsService

#Users
def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)


#Commitment
def get_commitment_repository(db: AsyncSession = Depends(get_db)) -> CommitmentRepository:
    return CommitmentRepository(db)

def get_commitment_service(commitment_repo: CommitmentRepository = Depends(get_commitment_repository)) -> CommitmentService:
    return CommitmentService(commitment_repo)

# Analytics
def get_analytics_service(db: AsyncSession = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(db)