"""Tests for GET /activities endpoint."""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure."""
    # Arrange: No specific setup needed as activities are in-memory

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check response status and content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Based on the 9 activities defined

    # Check that expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Soccer Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
    ]
    for activity in expected_activities:
        assert activity in data
        assert "description" in data[activity]
        assert "schedule" in data[activity]
        assert "max_participants" in data[activity]
        assert "participants" in data[activity]
        assert isinstance(data[activity]["participants"], list)