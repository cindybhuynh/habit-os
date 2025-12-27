from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_habit():
    create_resp = client.post("/habits", json={"name": "yoga", "schedule_type": "daily", "target_count": 1, "start_date": "2025-12-26", "notes": "This is a test",})
    assert create_resp.status_code == 201
    assert create_resp.json() == {
        "id": 1,
        "name": "yoga", 
        "schedule_type": "daily", 
        "target_count": 1, 
        "start_date": "2025-12-26", 
        "notes": "This is a test",
    }
    

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
