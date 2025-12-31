from app.schemas.habit import HabitCreate, HabitRead

class HabitStore:
    def __init__(self):
        self.habits: list[HabitRead] = []
        self.next_id: int = 1
    
    def reset(self):
        self.habits.clear()
        self.next_id = 1

    def create_habit(self, habit_in: HabitCreate) -> HabitRead:
        habit = HabitRead(id=self.next_id, **habit_in.model_dump())
        self.next_id += 1
        self.habits.append(habit)
        return habit

    def list_habits(self) -> list[HabitRead]:
        return self.habits

    def get_habit(self, habit_id: int) -> HabitRead | None:
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        return None

# A single shared store instance for app runtime
_store = HabitStore()

def get_store() -> HabitStore:
    return _store

def create_habit(habit_in: HabitCreate) -> HabitRead:
    return get_store().create_habit(habit_in)

def list_habits() -> list[HabitRead]:
    return get_store().list_habits()

def get_habit(habit_id: int) -> HabitRead | None:
    return get_store().get_habit(habit_id)