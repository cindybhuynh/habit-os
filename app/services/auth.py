# app/services/auth.py
from __future__ import annotations

from datetime import date as dt_date
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead



class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class AuthStore:
    def __init__(self, db: Session):
        self.db = db

    def register_user(user_in: UserCreate) -> UserRead:
        user = User(**habit_in.model_dump())
        self.db.add(habit)
        try:
            self.db.flush()
            self.db.refresh(habit)
            return HabitRead.model_validate(habit)
        except IntegrityError as e:
            self.db.rollback()
            raise HabitAlreadyExistsError() from e

    def authenticate_user(email: str, password: str) -> str:



def get_auth_store(db: Session = Depends(get_db)) -> AuthStore:
    return AuthStore(db)

