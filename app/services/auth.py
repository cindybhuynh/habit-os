# app/services/auth.py
from __future__ import annotations

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password, verify_password, create_access_token


class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class AuthStore:
    
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_in: UserCreate) -> UserRead:
        hashed = hash_password(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed)

        self.db.add(user)
        try:
            self.db.flush()
            self.db.refresh(user)
            return UserRead.model_validate(user)
        except IntegrityError as e:
            self.db.rollback()
            raise UserAlreadyExistsError() from e

    def authenticate_user(self, email: str, password: str) -> str:
        user = (
            self.db.execute(
                select(User)
                .where(User.email == email)
            )
            .scalar_one_or_none()
        )
        
        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        
        return create_access_token(user.id)


def get_auth_store(db: Session = Depends(get_db)) -> AuthStore:
    return AuthStore(db)

