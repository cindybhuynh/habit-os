# app/tests/test_habits.py

def _create_habit(client, name, number) -> int:
    r = client.post("/habits", json={
        "name": name,
        "schedule_type": "daily",
        "target_count": number,
        "start_date": "2026-06-22",
        "notes": None
    })
    assert r.status_code == 201
    return r.json()["id"]

def test_create_habit(client):
    r = client.post("/habits", json={
        "name": "Drink water",
        "schedule_type": "daily",
        "target_count": 8,
        "start_date": "2026-06-22",
        "notes": "Drink 8 cups of water daily"
    })
    assert r.status_code == 201
    data = r.json()
    assert isinstance(data["id"], int)
    assert data["name"] == "Drink water"

def test_list_habits(client):
    _create_habit(client, "Walking", 1)
    r = client.get("/habits")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == "Walking"

def test_get_habit_404(client):
    r = client.get("/habits/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Habit not found"

def test_create_habit_validation_error(client):
    r = client.post("/habits", json={
        "name": "",
        "schedule_type": "daily",
        "target_count": 1,
        "start_date": "2026-01-06",
        "notes": None,
    })
    assert r.status_code == 422

def test_create_habit_duplicate_name_returns_409(client):
    payload = {
        "name": "Meditate",
        "schedule_type": "daily",
        "target_count": 1,
        "start_date": "2026-01-06",
        "notes": None,
    }
    r1 = client.post("/habits", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/habits", json=payload)
    assert r2.status_code == 409
    assert r2.json()["detail"] == "Habit already exists"

def test_delete_habit_success(client):
    habit_id = _create_habit(client, "Yoga", 1)
    r1 = client.delete(f"/habits/{habit_id}")
    assert r1.status_code == 204

    r2 = client.get(f"/habits/{habit_id}")
    assert r2.status_code == 404