import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())


def test_signup_and_unregister():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    # Duplicate signup should fail
    dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup.status_code == 400
    # Unregister
    unregister = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister.status_code == 200
    # Unregister again should fail
    unregister2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister2.status_code == 400


def test_invalid_activity():
    email = "nouser@mergington.edu"
    resp = client.post("/activities/invalid_activity/signup?email=" + email)
    assert resp.status_code == 404
    resp2 = client.post("/activities/invalid_activity/unregister?email=" + email)
    assert resp2.status_code == 404
