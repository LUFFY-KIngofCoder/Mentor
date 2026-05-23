from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.auth.oauth2 import get_current_user

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db:Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/auth/login")
def login_user(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=user_credentials.username).first()

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


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db:Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    return user

@router.get("/auth/me")
def get_me(
        current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/protected")
def protected_route(
        current_user: User = Depends(get_current_user)
):

    return {
        "message": "Authenticated",
        "user": current_user.email
    }