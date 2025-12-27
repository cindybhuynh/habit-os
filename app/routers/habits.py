from fastapi import APIRouter
from app.schemas.habit import HabitCreate, HabitRead

router = APIRouter(prefix="/habits", tags=["habits"])

HABITS: list[HabitRead] = []
NEXT_ID = 1

@router.post("", response_model=HabitRead, status_code=201)
def create_habit(habit_in: HabitCreate):
    global NEXT_ID
    habit = HabitRead(id = NEXT_ID, **habit_in.model_dump())
    NEXT_ID += 1
    HABITS.append(habit)
    return habit

@router.get("", response_model=list[HabitRead])
def list_habits():
    return HABITS
