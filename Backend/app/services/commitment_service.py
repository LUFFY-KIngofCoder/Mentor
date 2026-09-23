from datetime import timedelta, datetime
from uuid import UUID

from app.repositories.commitment_repository import CommitmentRepository
from app.models.commitment import Commitment
from app.core.exceptions import NotFoundException
from app.core.exceptions import UnauthorizedException
from app.schema.commitment import CommitmentUpdate


class CommitmentService:

    def __init__(self, commitment_repo: CommitmentRepository):
        self.commitment_repo = commitment_repo

    async def create_commitment(self, commitment: Commitment) -> Commitment:
        end_date = (
        commitment.start_date + timedelta(days=commitment.duration_days)
        )

        commitment.end_date = end_date

        return await self.commitment_repo.create(commitment)
    
    async def get_user_commitments(self, user_id: UUID,limit: int = 10, cursor: datetime | None = None, status: str | None = None) -> tuple[list[Commitment],datetime | None]:
        return await self.commitment_repo.get_all_for_user(user_id=user_id,limit=limit,cursor=cursor,status=status)
    
    async def get_user_commitment(self, commitment_id: UUID,user_id: UUID):
        commitment = await self.commitment_repo.get_by_id(commitment_id)

        if not commitment:
            raise NotFoundException("Commitment not found")

        if commitment.user_id != user_id:
            raise UnauthorizedException("Not authorized to access this commitment")

        return commitment
    
    async def update_commitment(self,commitment_id:UUID,commitment_update:CommitmentUpdate, user_id:UUID) -> Commitment:
        commitment = await self.get_user_commitment(commitment_id,user_id)

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

        return await self.commitment_repo.update(commitment)

    async def delete_commitment(self,commitment_id:UUID,user_id:UUID):
        commitment = await self.get_user_commitment(commitment_id,user_id)
        return await self.commitment_repo.delete(commitment)