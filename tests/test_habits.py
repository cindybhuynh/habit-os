from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_habits_list_starts_empty():
    resp = client.get("/habits")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_habit_returns_expected_fields():
    resp = client.post("/habits", json={
        "name": "yoga", 
        "schedule_type": "daily", 
        "target_count": 1, 
        "start_date": "2025-12-26", 
        "notes": "This is a test",
    })
    assert resp.status_code == 201
    data = resp.json()

    assert "id" in data
    assert isinstance(data["id"], int)

    assert data["name"] == "yoga"
    assert data["schedule_type"] == "daily"
    assert data["target_count"] == 1
    assert data["start_date"] == "2025-12-26"
    assert data["notes"] == "This is a test"
    

def test_habit_included_in_list():
    create_resp = client.post("/habits", json={
        "name": "reading", 
        "schedule_type": "daily", 
        "target_count": 1, 
        "start_date": "2025-12-26", 
        "notes": "Read 15 minutes daily",
    })
    assert create_resp.status_code == 201
    created = create_resp.json()

    list_resp = client.get("/habits")
    assert list_resp.status_code == 200
    habits = list_resp.json()
    
    assert len(habits) == 1
    assert habits[0]["id"] == created["id"]
    assert habits[0]["name"] == "reading"


def test_invalid_target_count():
    resp = client.post("/habits", json={
        "name": "yoga", 
        "schedule_type": "daily", 
        "target_count": 0, 
        "start_date": "2025-12-26",
    })
    assert resp.status_code == 422
    assert "detail" in resp.json()


def test_create_habit_ids_increment():
    r1 = client.post("/habits", json={
        "name": "habit1", 
        "schedule_type": "daily", 
        "target_count": 1, 
        "start_date": "2025-12-28", 
    })
    r2 = client.post("/habits", json={
        "name": "habit2", 
        "schedule_type": "daily", 
        "target_count": 1, 
        "start_date": "2025-12-28", 
    })
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.json()["id"] == 1
    assert r2.json()["id"] == 2

def test_invalid_schedule_type():
    resp = client.post("/habits", json={
        "name": "habit1", 
        "schedule_type": "regularly", 
        "target_count": 1, 
        "start_date": "2025-12-28", 
    })
    assert resp.status_code == 422
    assert "detail" in resp.json()

def test_empty_name():
    resp = client.post("/habits", json={
        "name": "", 
        "schedule_type": "daily", 
        "target_count": 1, 
        "start_date": "2025-12-28", 
    })
    assert resp.status_code == 422
    assert "detail" in resp.json()