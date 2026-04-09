"""Integration tests for full user workflows."""


def test_full_signup_and_remove_workflow(client):
    """Test complete workflow: get activities, signup, verify, remove, verify."""
    # Arrange: Choose an activity and a test email
    activity_name = "Soccer Club"
    test_email = "integration@test.edu"

    # Act & Assert: Step 1 - Get activities and verify activity exists
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert activity_name in activities
    initial_participants = activities[activity_name]["participants"]
    assert test_email not in initial_participants

    # Act & Assert: Step 2 - Sign up for the activity
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {test_email} for {activity_name}" in data["message"]

    # Act & Assert: Step 3 - Verify participant was added
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    updated_participants = activities[activity_name]["participants"]
    assert test_email in updated_participants

    # Act & Assert: Step 4 - Remove the participant
    response = client.delete(f"/activities/{activity_name}/participants?email={test_email}")
    assert response.status_code == 200

    # Act & Assert: Step 5 - Verify participant was removed
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    final_participants = activities[activity_name]["participants"]
    assert test_email not in final_participants