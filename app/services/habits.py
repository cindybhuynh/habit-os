from app.schemas.habit import HabitCreate, HabitRead

HABITS: list[HabitRead] = []
NEXT_ID = 1

def create_habit(habit_in: HabitCreate) -> HabitRead: 
    global NEXT_ID
    habit = HabitRead(id = NEXT_ID, **habit_in.model_dump())
    NEXT_ID += 1
    HABITS.append(habit)
    return habit

def list_habits() -> list[HabitRead]:
    return HABITS

def get_habit(habit_id: int) -> HabitRead | None:
    for habit in HABITS:
        if habit.id == habit_id:
            return habit
    return None