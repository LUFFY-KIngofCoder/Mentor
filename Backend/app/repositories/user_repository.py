from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import User


class UserRepository:
    def __init__(self,db:AsyncSession):
        self.db=db
    
    async def get_by_email(self,email:str) -> User | None:
        result = await self.db.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()
    
    async def get_by_id(self,id:UUID) -> User | None:
        result = await self.db.execute(select(User).filter_by(id=id))
        return result.scalar_one_or_none()
    
    async def create(self,user:User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user