from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_returns_healthy():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}