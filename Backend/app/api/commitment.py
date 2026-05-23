from fastapi import APIRouter , Depends
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
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
def create_commitment(
        commitment: CommitmentCreate,
        db: Session = Depends(get_db),
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
    db.commit()
    db.refresh(new_commitment)

    return new_commitment

@router.get("/", response_model=List[CommitmentResponse])
def get_commitments(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    commitments = db.query(Commitment).filter(Commitment.user_id == current_user.id).all()
    return commitments


@router.get("/{commitment_id}", response_model=CommitmentResponse)
def get_commitment(
        commitment_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    commitment = get_user_commitments(
        commitment_id,
        current_user,
        db
    )

    return commitment

@router.patch("/{commitment_id}", response_model=CommitmentResponse)
def update_commitment(
        commitment_id: UUID,
        commitment_update: CommitmentUpdate,

        db: Session = Depends(get_db),

        current_user: User = Depends(get_current_user)
):

    commitment = get_user_commitments(
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

    db.commit()
    db.refresh(commitment)

    return commitment

@router.delete("/{commitment_id}")
def delete_commitment(
        commitment_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    commitment = get_user_commitments(
        commitment_id,
        current_user,
        db
    )
    db.delete(commitment)
    db.commit()

    return {
        "message": "Commitment deleted successfully"
    }