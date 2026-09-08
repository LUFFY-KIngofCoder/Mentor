from app.core.dependencies import get_user_service
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from sqlalchemy import select

from app.db.database import get_db
from app.models.user import User
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY 
ALGORITHM = settings.ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service : UserService = Depends(get_user_service)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await user_service.user_repo.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user