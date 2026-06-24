# app/tests/test_health.py

def test_health_returns_healthy(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}