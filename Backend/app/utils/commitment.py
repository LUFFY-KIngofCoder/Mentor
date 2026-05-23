from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Commitment, User


def get_user_commitments(
        commitment_id: UUID,
        current_user: User,
        db: Session
):

    commitment = db.query(Commitment).filter(
        Commitment.id == commitment_id
    ).first()

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