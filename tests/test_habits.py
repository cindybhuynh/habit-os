def test_create_habit(client):
    payload = {
        "name": "Drink water",
        "schedule_type": "daily",
        "target_count": 8,
        "start_date": "2026-01-06",
        "notes": "8 cups",
    }
    r = client.post("/habits", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 1
    assert data["name"] == "Drink water"

def test_list_habits(client):
    client.post("/habits", json={
        "name": "Walk",
        "schedule_type": "daily",
        "target_count": 1,
        "start_date": "2026-01-06",
        "notes": None,
    })
    r = client.get("/habits")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == "Walk"

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