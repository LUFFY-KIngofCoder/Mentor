from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any
from sqlalchemy import select

from app.auth.oauth2 import get_current_user
from app.models import User
from app.core.dependencies import get_execution_log_service
from app.services.execution_log_service import ExecutionLogService
router = APIRouter(
    prefix="/execution-log",
    tags=["Execution Log"]
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_unified_execution_log(
    exec_log_service: ExecutionLogService = Depends(get_execution_log_service),
    current_user: User = Depends(get_current_user)
    ):
    return await exec_log_service.get_unified_execution_logs(current_user.id)
    