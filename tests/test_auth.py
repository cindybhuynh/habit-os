# tests/test_auth.py

def test_register_success(client):
    email = "test@example.com"
    password = "stringst"

    r = client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert r.status_code == 201

    data = r.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data # ensure password information is not in data
    assert "hashed_password" not in data
    assert isinstance(data["id"], int)

    
def test_register_duplicate_email_returns_409(client):
    email = "test@example.com"
    password = "stringst"

    r = client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert r.status_code == 201

    r = client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert r.status_code == 409

def test_login_success(client):
    email = "test@example.com"
    password = "stringst"

    r = client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert r.status_code == 201

    r = client.post("/auth/login", data={
        "username": email,
        "password": password,
    })

    assert r.status_code == 200

    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_incorrect_password_returns_401(client):
    email = "test@example.com"
    correct_password = "stringst"
    incorrect_password = "wrongpassword"
    
    r = client.post("/auth/register", json={
        "email": email,
        "password": correct_password,
    })

    assert r.status_code == 201

    r = client.post("/auth/login", data={
        "username": email,
        "password": incorrect_password,
    })

    assert r.status_code == 401