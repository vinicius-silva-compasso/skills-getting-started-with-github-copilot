"""Tests for POST /activities/{activity_name}/signup endpoint."""


def test_signup_successful(client):
    """Test successful signup for an activity."""
    # Arrange: Choose an activity and a new email not already signed up
    activity_name = "Art Studio"
    new_email = "test@student.edu"

    # Ensure the email is not already in participants
    response = client.get("/activities")
    initial_participants = response.json()[activity_name]["participants"]
    assert new_email not in initial_participants

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert: Check response status and message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {new_email} for {activity_name}" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert new_email in updated_participants


def test_signup_activity_not_found(client):
    """Test signup for a non-existent activity."""
    # Arrange: Use a non-existent activity name
    activity_name = "NonExistent Activity"
    email = "test@student.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check response status and error detail
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up(client):
    """Test signup when student is already signed up."""
    # Arrange: Use an activity and an email already signed up
    activity_name = "Drama Club"
    existing_email = "aiden@mergington.edu"  # From initial data

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")

    # Assert: Check response status and error detail
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is already signed up for this activity" in data["detail"]