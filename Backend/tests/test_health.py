from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("api/")
    assert response.status_code == 200
    assert response.json() == {"message":"Mentor API v1.0"}

def test_health_endpoint():
    response = client.get("api/health")
    assert response.status_code == 200
    assert response.json() == {"status":"healthy"}

def test_login_missing_credentials():
    response = client.post("api/auth/login", data={})
    assert response.status_code == 422
