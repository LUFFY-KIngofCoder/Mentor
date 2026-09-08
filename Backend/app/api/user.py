from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import hash_password
from app.db.database import get_db
from app.models.user import User
from app.schema.user import UserCreate, UserResponse
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.auth.oauth2 import get_current_user
from app.core.dependencies import get_user_service
from app.services.user_service import UserService



router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, user_service : UserService = Depends(get_user_service)):


    new_user =  await user_service.create_user(User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    ))
    
    return new_user

@router.post("/auth/login")
async def login_user(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        user_service : UserService = Depends(get_user_service)
):

    user = await user_service.user_repo.get_by_email(user_credentials.username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist.",
        )

    valid_password = verify_password(
        user_credentials.password,
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


@router.get("/users/{user_id}", response_model=UserResponse | None)
async def get_user(user_id: UUID, user_service : UserService = Depends(get_user_service)):

    user = await user_service.user_repo.get_by_id(user_id)
    return user

@router.get("/auth/me")
async def get_me(
        current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/protected")
async def protected_route(
        current_user: User = Depends(get_current_user)
):

    return {
        "message": "Authenticated",
        "user": current_user.email
    }