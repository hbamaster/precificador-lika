# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthcheck():
    res = client.get("/health")
    assert res.status_code == 200