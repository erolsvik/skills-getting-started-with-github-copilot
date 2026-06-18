from urllib.parse import quote

from src.app import activities


def test_get_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in data
    assert data[expected_activity]["description"] == "Learn strategies and compete in chess tournaments"
    assert "participants" in data[expected_activity]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={encoded_email}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_returns_error(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(existing_email, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={encoded_email}")
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student is already signed up for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = activities[activity_name]["participants"][0]
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(participant_email, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants?email={encoded_email}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Removed {participant_email} from {activity_name}"
    assert participant_email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing@mergington.edu"
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(missing_email, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants?email={encoded_email}")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"
