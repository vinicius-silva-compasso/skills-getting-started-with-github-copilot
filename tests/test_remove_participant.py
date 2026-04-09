"""Tests for DELETE /activities/{activity_name}/participants endpoint."""


def test_remove_participant_successful(client):
    """Test successful removal of a participant from an activity."""
    # Arrange: Choose an activity and an existing participant
    activity_name = "Science Club"
    email_to_remove = "grace@mergington.edu"  # From initial data

    # Verify the participant is initially in the activity
    response = client.get("/activities")
    initial_participants = response.json()[activity_name]["participants"]
    assert email_to_remove in initial_participants

    # Act: Make DELETE request to remove participant
    response = client.delete(f"/activities/{activity_name}/participants?email={email_to_remove}")

    # Assert: Check response status
    assert response.status_code == 200

    # Verify the participant was removed
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert email_to_remove not in updated_participants


def test_remove_participant_activity_not_found(client):
    """Test removal from a non-existent activity."""
    # Arrange: Use a non-existent activity name
    activity_name = "NonExistent Activity"
    email = "test@student.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert: Check response status and error detail
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_remove_participant_not_in_activity(client):
    """Test removal of a participant not in the activity."""
    # Arrange: Choose an activity and an email not signed up
    activity_name = "Science Club"
    email_not_in_activity = "notsignedup@student.edu"

    # Verify the email is not in participants
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    assert email_not_in_activity not in participants

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants?email={email_not_in_activity}")

    # Assert: Check response status and error detail
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found in activity" in data["detail"]