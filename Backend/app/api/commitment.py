from fastapi import APIRouter , Depends, Query
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.auth.oauth2 import get_current_user

from app.models import Commitment , User
from app.schema.commitment import (
    CommitmentCreate,
    CommitmentResponse, 
    CommitmentUpdate
)
from app.services.commitment_service import CommitmentService
from app.core.dependencies import get_commitment_service
from app.schema.commitment import PaginationResponse



router = APIRouter(
    prefix = "/commitments",
    tags = ["Commitments"]
)

@router.post("/", response_model=CommitmentResponse)
async def create_commitment(
        commitment: CommitmentCreate,
        commitment_service: CommitmentService = Depends(get_commitment_service),
        current_user: User = Depends(get_current_user)
                      ):
    
    new_commitment = Commitment(
        user_id=current_user.id,
        title=commitment.title,
        description=commitment.description,
        duration_days=commitment.duration_days,
        start_date=commitment.start_date,
    )

    return await commitment_service.create_commitment(new_commitment)

@router.get("/", response_model=PaginationResponse[CommitmentResponse])
async def get_commitments(
        cursor: datetime | None = Query(None, description="Cursor for infinite scrolling"),
        limit: int = Query(10, ge=1, le=50, description="Items per page"),
        status: str | None = Query(None, description="Filter by status (active, completed)"),
        current_user: User = Depends(get_current_user),
        commitment_service: CommitmentService = Depends(get_commitment_service)
):

    commitments, next_cursor = await commitment_service.get_user_commitments(
        current_user.id, limit=limit, cursor=cursor, status=status
    )
    
    return PaginationResponse(
        items=commitments,
        size=len(commitments),
        next_cursor=next_cursor
    )


@router.get("/{commitment_id}", response_model=CommitmentResponse)
async def get_commitment(
        commitment_id: UUID,
        commitment_service: CommitmentService = Depends(get_commitment_service),
        current_user: User = Depends(get_current_user)
):

    return await commitment_service.get_user_commitment(commitment_id,current_user.id)


@router.patch("/{commitment_id}", response_model=CommitmentResponse)
async def update_commitment(
        commitment_id: UUID,
        commitment_update: CommitmentUpdate,

        commitment_service: CommitmentService = Depends(get_commitment_service),

        current_user: User = Depends(get_current_user)
):
    return await commitment_service.update_commitment(
        commitment_id,commitment_update,current_user.id)

@router.delete("/{commitment_id}")
async def delete_commitment(
        commitment_id: UUID,
        commitment_service: CommitmentService = Depends(get_commitment_service),
        current_user: User = Depends(get_current_user)
):
    return await commitment_service.delete_commitment(
        commitment_id,
        current_user.id
    )