from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_habits_empty():
    resp = client.get("/habits")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_habit():
    resp = client.post("/habits", json={"name": "yoga", "schedule_type": "daily", "target_count": 1, "start_date": "2025-12-26", "notes": "This is a test",})
    assert resp.status_code == 201
    data = resp.json()

    assert "id" in data
    assert isinstance(data["id"], int)

    assert data["name"] == "yoga"
    assert data["schedule_type"] == "daily"
    assert data["target_count"] == 1
    assert data["start_date"] == "2025-12-26"
    assert data["notes"] == "This is a test"
    

def test_habit_in_list():
    create_resp = client.post("/habits", json={"name": "reading", "schedule_type": "daily", "target_count": 1, "start_date": "2025-12-26", "notes": "Read 15 minutes daily",})
    assert create_resp.status_code == 201
    created = create_resp.json()

    list_resp = client.get("/habits")
    assert list_resp.status_code == 200
    habits = list_resp.json()
    assert isinstance(habits, list)

    assert any(h["id"] == created["id"] for h in habits)

    found = next(h for h in habits if h["id"] == created["id"])
    assert found["name"] == "reading"
    assert found["schedule_type"] == "daily"
    assert found["target_count"] == 1
    assert found["start_date"] == "2025-12-26"
    assert found["notes"] == "Read 15 minutes daily"



def test_invalid_target_count():
    resp = client.post("/habits", json={"name": "yoga", "schedule_type": "daily", "target_count": 0, "start_date": "2025-12-26",})
    assert resp.status_code == 422
