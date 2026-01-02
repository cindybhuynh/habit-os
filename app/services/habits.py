# app/services/habits.py
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.habit import HabitCreate, HabitRead

class HabitStore:
    def __init__(self, db: Session):
        self.db = db

    # For now, these are placeholders until you add a SQLAlchemy Habit model.
    # Once you have app/models/habit.py, you'll implement real CRUD here.
    def create_habit(self, habit_in: HabitCreate) -> HabitRead:
        raise NotImplementedError("Implement DB-backed create_habit after adding Habit SQLAlchemy model")

    def list_habits(self) -> list[HabitRead]:
        raise NotImplementedError("Implement DB-backed list_habits after adding Habit SQLAlchemy model")

    def get_habit(self, habit_id: int) -> HabitRead | None:
        raise NotImplementedError("Implement DB-backed get_habit after adding Habit SQLAlchemy model")

def get_store(db: Session = Depends(get_db)) -> HabitStore:
    return HabitStore(db)
