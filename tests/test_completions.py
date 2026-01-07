# tests/test_completions.py

def _create_habit(client) -> int:
    r = client.post("/habits", json={
        "name": "Meditate",
        "schedule_type": "daily",
        "target_count": 1,
        "start_date": "2026-01-06",
        "notes": None,
    })
    assert r.status_code == 201
    return r.json()["id"]


def test_create_completion_success(client):
    habit_id = _create_habit(client)

    r = client.post(f"/habits/{habit_id}/completions", json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": "Felt great!",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["habit_id"] == habit_id
    assert data["done_on"] == "2026-01-07"


def test_create_completion_missing_habit(client):
    r = client.post("/habits/999/completions", json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": "Felt great!",
    })
    assert r.status_code == 404
    assert r.json()["detail"] == "Habit not found"


def test_list_completions_success(client):
    habit_id = _create_habit(client)

    r1 = client.post(f"/habits/{habit_id}/completions", json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": "Felt great!",
    })
    assert r1.status_code == 201

    r = client.get(f"/habits/{habit_id}/completions")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["habit_id"] == habit_id


def test_validation_count_zero(client):
    habit_id = _create_habit(client)

    r = client.post(f"/habits/{habit_id}/completions", json={
        "done_on": "2026-01-07",
        "count": 0,
        "notes": "Felt great!",
    })
    assert r.status_code == 422
