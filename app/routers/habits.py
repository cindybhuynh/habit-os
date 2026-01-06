from fastapi import APIRouter, Depends, HTTPException
from app.schemas.habit import HabitCreate, HabitRead
from app.services.habits import HabitStore, get_store, HabitAlreadyExistsError

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("", response_model=HabitRead, status_code=201)
def create_habit(habit_in: HabitCreate, store: HabitStore = Depends(get_store)):
    try:
        return store.create_habit(habit_in)
    except HabitAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Habit already exists")

@router.get("", response_model=list[HabitRead], response_model_exclude_none=True)
def list_habits(store: HabitStore = Depends(get_store)):
    return store.list_habits()

@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, store: HabitStore = Depends(get_store)):
    habit = store.get_habit(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit
