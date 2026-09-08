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

        
