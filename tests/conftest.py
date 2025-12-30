import pytest
import app.services.habits as habits_module

@pytest.fixture(autouse=True)
def reset_habits_store():
    habits_module.HABITS.clear()
    habits_module.NEXT_ID = 1
