import copy
import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original_activities


@pytest.fixture
def client():
    return TestClient(app_module.app)


def quote_activity_name(name: str) -> str:
    return urllib.parse.quote(name, safe="")


def test_root_redirects_to_static_index(client: TestClient):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client: TestClient):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_succeeds_for_new_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{quote_activity_name(activity_name)}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"
    url = f"/activities/{quote_activity_name(activity_name)}/signup"

    # Act
    response = client.post(url, params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_missing_activity_returns_404(client: TestClient):
    # Arrange
    activity_name = "Nonexistent Club"
    url = f"/activities/{quote_activity_name(activity_name)}/signup"

    # Act
    response = client.post(url, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_succeeds_for_existing_participant(client: TestClient):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    url = f"/activities/{quote_activity_name(activity_name)}/signup"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_from_activity_rejects_missing_participant(client: TestClient):
    # Arrange
    activity_name = "Programming Class"
    missing_email = "notregistered@mergington.edu"
    url = f"/activities/{quote_activity_name(activity_name)}/signup"

    # Act
    response = client.delete(url, params={"email": missing_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_from_missing_activity_returns_404(client: TestClient):
    # Arrange
    activity_name = "Nonexistent Club"
    url = f"/activities/{quote_activity_name(activity_name)}/signup"

    # Act
    response = client.delete(url, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
