def test_habits_status_no_completions(client):
    # Create habit
    r = client.post("/habits", json={
        "name": "Drink water",
        "schedule_type": "daily",
        "target_count": 8,
        "start_date": "2026-01-06",
        "notes": None,
    })
    assert r.status_code == 201
    habit_id = r.json()["id"]

    r = client.get("/habits/status?for_date=2026-01-07")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == habit_id
    assert data[0]["completed_on_date"] is False
    assert data[0]["completion_count_on_date"] == 0
    assert data[0]["date"] == "2026-01-07"


def test_habits_status_with_completion(client):
    # Create habit
    r = client.post("/habits", json={
        "name": "Stretch",
        "schedule_type": "daily",
        "target_count": 1,
        "start_date": "2026-01-06",
        "notes": None,
    })
    assert r.status_code == 201
    habit_id = r.json()["id"]

    # Create completion for that date
    r = client.post(f"/habits/{habit_id}/completions", json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": None,
    })
    assert r.status_code == 201

    r = client.get("/habits/status?for_date=2026-01-07")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == habit_id
    assert data[0]["completed_on_date"] is True
    assert data[0]["completion_count_on_date"] == 1