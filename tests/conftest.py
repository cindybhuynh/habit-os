import pytest
from app.main import app
from app.services.habits import HabitStore, get_store

@pytest.fixture(autouse=True)
def override_store_dependency():
    test_store = HabitStore()
    app.dependency_overrides[get_store] = lambda: test_store
    yield
    app.dependency_overrides.clear()
