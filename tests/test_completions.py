# tests/test_completions.py

from tests.conftest import _register_and_login, _auth

def _create_habit(client, token, name, number) -> int:

    r = client.post("/habits", headers=_auth(token), json={
        "name": name,
        "schedule_type": "daily",
        "target_count": number,
        "start_date": "2026-06-22",
        "notes": None
    })
    assert r.status_code == 201
    return r.json()["id"]


def test_create_completion_success(client):
    token = _register_and_login(client)
    habit_id = _create_habit(client, token, "Walking", 1)

    r = client.post(f"/habits/{habit_id}/completions", headers=_auth(token), json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": "Felt great!",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["habit_id"] == habit_id
    assert data["done_on"] == "2026-01-07"


def test_create_completion_missing_habit(client):
    token = _register_and_login(client)

    r = client.post("/habits/999/completions", headers=_auth(token), json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": "Felt great!",
    })
    assert r.status_code == 404
    assert r.json()["detail"] == "Habit not found"


def test_list_completions_success(client):
    token = _register_and_login(client)
    habit_id = _create_habit(client, token, "Dance", 1)

    r1 = client.post(f"/habits/{habit_id}/completions", headers=_auth(token), json={
        "done_on": "2026-01-07",
        "count": 1,
        "notes": "Felt great!",
    })
    assert r1.status_code == 201

    r = client.get(f"/habits/{habit_id}/completions", headers=_auth(token))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["habit_id"] == habit_id


def test_validation_count_zero(client):
    token = _register_and_login(client)
    habit_id = _create_habit(client, token, "Yoga", 1)

    r = client.post(f"/habits/{habit_id}/completions", headers=_auth(token), json={
        "done_on": "2026-01-07",
        "count": 0,
        "notes": "Felt great!",
    })
    assert r.status_code == 422

def test_duplicate_completion_same_day_returns_409(client):
    token = _register_and_login(client)
    habit_id = _create_habit(client, token, "Study Spanish", 1)

    payload = {"done_on": "2026-01-07", "count": 1, "notes": None}

    r1 = client.post(f"/habits/{habit_id}/completions", headers=_auth(token), json=payload)
    assert r1.status_code == 201

    r2 = client.post(f"/habits/{habit_id}/completions", headers=_auth(token), json=payload)
    assert r2.status_code == 409
    assert r2.json()["detail"] == "Completion already exists"

def test_toggle_completion(client):
    token = _register_and_login(client)
    habit_id = _create_habit(client, token, "Meditation", 1)

    r = client.post(f"/habits/{habit_id}/completions/toggle/2026-01-06", headers=_auth(token))
    data = r.json()
    assert data["completed"] is True

    r = client.post(f"/habits/{habit_id}/completions/toggle/2026-01-06", headers=_auth(token))
    data = r.json()
    assert data["completed"] is False

    r = client.post(f"/habits/{habit_id}/completions/toggle/2026-01-06", headers=_auth(token))
    data = r.json()
    assert data["completed"] is True

def test_user_cannot_access_other_users_completion(client):
    token1 = _register_and_login(client, email="user1@example.com")
    habit_id = _create_habit(client, token1, "Reading", 2)

    token2 = _register_and_login(client, email="user2@example.com")

    r = client.post(f"/habits/{habit_id}/completions/toggle/2026-07-03", headers=_auth(token2))
    assert r.status_code == 404