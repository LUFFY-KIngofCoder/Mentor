from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Mentor Backend Running"}

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"healthy"}

def test_login_missing_credentials():
    resposne = client.post("/auth/login", data={})
    assert resposne.status_code == 422
