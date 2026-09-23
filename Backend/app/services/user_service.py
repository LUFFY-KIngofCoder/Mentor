from app.core.security import verify_password
from fastapi import HTTPException
from app.core.security import create_access_token
from app.repositories.user_repository import UserRepository
from app.schema.user import UserCreate
from app.models.user import User
from app.core.security import hash_password

class UserService:
    # 1. We inject the repository into the service
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    async def create_user(self, user_in: UserCreate) -> User:
        new_user = User(
            name= user_in.name,
            email= user_in.email,
            password_hash=hash_password(user_in.password)
        )

        result = await self.user_repo.create(new_user)
        
        return result

    async def authenticate_user(self, credentials) -> dict:
        
        user = await self.user_repo.get_by_email(credentials.username)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user does not exist.",
            )

        valid_password = verify_password(
            credentials.password,
            user.password_hash
        )

        if not valid_password:
            raise HTTPException(
                status_code=403,
                detail="Invalid Credentials",
            )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

            
