from fastapi import APIRouter
from app.schemas.habit import HabitCreate, HabitRead
from app.services import habits as habits_service

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("", response_model=HabitRead, status_code=201)
def create_habit(habit_in: HabitCreate):
    return habits_service.create_habit(habit_in)

@router.get("", response_model=list[HabitRead])
def list_habits():
    return habits_service.list_habits()

@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int):
    habit = habits_service.get_habit(habit_id)
    if habit is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit