from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Commitment, User


async def get_user_commitments(
        commitment_id: UUID,
        current_user: User,
        db: AsyncSession
):

    result = await db.execute(select(Commitment).filter(
        Commitment.id == commitment_id
    ))
    commitment = result.scalar_one_or_none()

    if not commitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commitment not found"
        )

    if commitment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to access this commitment"
        )

    return commitment