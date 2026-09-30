from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from arq import ArqRedis

from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.repositories.commitment_repository import CommitmentRepository
from app.services.commitment_service import CommitmentService
from app.services.analytics_service import AnalyticsService
from app.repositories.daily_entry_repository import DailyEntryRepository
from app.services.daily_entry_service import DailyEntryService
from app.services.missed_day_service import MissedDayService
from app.repositories.missed_day_repository import MissedDayRepository
from app.services.execution_log_service import ExecutionLogService
from app.core.redis import redis_client, get_arq_pool


async def get_task_queue(pool: ArqRedis = Depends(get_arq_pool)) -> ArqRedis:
    return pool

# Redis
def get_redis_client() -> Redis:
    return redis_client

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
def get_analytics_service(db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis_client)) -> AnalyticsService:
    return AnalyticsService(db, redis)

# Daily Entry
def get_daily_entry_repository(db: AsyncSession = Depends(get_db)) -> DailyEntryRepository:
    return DailyEntryRepository(db)

def get_daily_entry_service(daily_entry_repo: DailyEntryRepository = Depends(get_daily_entry_repository), commitment_repo: CommitmentRepository = Depends(get_commitment_repository), redis : Redis = Depends(get_redis_client)) -> DailyEntryService:
    return DailyEntryService(daily_entry_repo, commitment_repo, redis)

# Missed Day
def get_missed_day_repository(db: AsyncSession = Depends(get_db)) -> MissedDayRepository:
    return MissedDayRepository(db)

def get_missed_day_service(missed_day_repo: MissedDayRepository = Depends(get_missed_day_repository), daily_entry_repo: DailyEntryRepository = Depends(get_daily_entry_repository), commitment_repo: CommitmentRepository = Depends(get_commitment_repository)) -> MissedDayService:
    return MissedDayService(missed_day_repo, daily_entry_repo, commitment_repo)

# Execution Log
def get_execution_log_service(daily_entry_repo: DailyEntryRepository = Depends(get_daily_entry_repository), missed_day_repo: MissedDayRepository = Depends(get_missed_day_repository)) -> ExecutionLogService:
    return ExecutionLogService(daily_entry_repo, missed_day_repo)

