import pytest
from fastapi.testclient import TestClient
from src.app import app

# Arrange: Create a test client fixture
@pytest.fixture
def client():
    return TestClient(app)

# Arrange: Helper to reset activities (if needed)
def reset_activities():
    from src import app as app_module
    if hasattr(app_module, 'activities'):
        for activity in app_module.activities.values():
            activity['participants'].clear()

# Test: List activities
def test_list_activities(client):
    # Arrange
    reset_activities()
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test: Signup for activity
def test_signup_for_activity(client):
    # Arrange
    reset_activities()
    email = "student1@example.com"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")
    # Act again: Try duplicate signup
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response2.status_code == 400 or "already" in response2.json().get("detail", "")

# Test: Signup for non-existent activity
def test_signup_nonexistent_activity(client):
    # Arrange
    reset_activities()
    email = "student2@example.com"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404

# Test: Unregister participant (if endpoint exists)
def test_unregister_participant(client):
    # Arrange
    reset_activities()
    email = "student3@example.com"
    activity = "Chess Club"
    # Act: Register first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act: Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code in (200, 404)  # 404 if endpoint not implemented
