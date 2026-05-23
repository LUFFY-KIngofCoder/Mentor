from fastapi import APIRouter , Depends
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.auth.oauth2 import get_current_user

from app.models import Commitment , User
from app.schema.commitment import (
CommitmentCreate,
CommitmentResponse
)

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