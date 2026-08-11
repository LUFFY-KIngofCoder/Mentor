from fastapi import APIRouter , Depends
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.auth.oauth2 import get_current_user

from app.models import Commitment , User
from app.schema.commitment import (
    CommitmentCreate,
    CommitmentResponse, CommitmentUpdate
)
from app.utils.commitment import get_user_commitments

router = APIRouter(
    prefix = "/commitments",
    tags = ["Commitments"]
)

@router.post("/", response_model=CommitmentResponse)
async def create_commitment(
        commitment: CommitmentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
                      ):
    end_date = (
        commitment.start_date + timedelta(days=commitment.duration_days)
    )

    new_commitment = Commitment(
        user_id=current_user.id,
        title=commitment.title,
        description=commitment.description,
        duration_days=commitment.duration_days,
        start_date=commitment.start_date,
        end_date=end_date
    )

    db.add(new_commitment)
    await db.commit()
    await db.refresh(new_commitment)

    return new_commitment

@router.get("/", response_model=List[CommitmentResponse])
async def get_commitments(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Commitment).filter(Commitment.user_id == current_user.id))
    commitments = result.scalars().all()
    return commitments


@router.get("/{commitment_id}", response_model=CommitmentResponse)
async def get_commitment(
        commitment_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    commitment = await get_user_commitments(
        commitment_id,
        current_user,
        db
    )

    return commitment

@router.patch("/{commitment_id}", response_model=CommitmentResponse)
async def update_commitment(
        commitment_id: UUID,
        commitment_update: CommitmentUpdate,

        db: AsyncSession = Depends(get_db),

        current_user: User = Depends(get_current_user)
):

    commitment = await get_user_commitments(
        commitment_id,
        current_user,
        db
    )

    update_data = commitment_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(commitment, key, value)

    if (
        "start_date" in update_data
        or "duration_days" in update_data
    ):
        commitment.end_date = commitment.start_date + timedelta(days=commitment.duration_days)

    await db.commit()
    await db.refresh(commitment)

    return commitment

@router.delete("/{commitment_id}")
async def delete_commitment(
        commitment_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    commitment = await get_user_commitments(
        commitment_id,
        current_user,
        db
    )
    await db.delete(commitment)
    await db.commit()

    return {
        "message": "Commitment deleted successfully"
    }