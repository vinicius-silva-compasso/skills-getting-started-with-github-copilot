"""Tests for GET / root endpoint."""


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html."""
    # Arrange: No specific setup needed

    # Act: Make GET request to / with follow_redirects=False to check redirect
    response = client.get("/", follow_redirects=False)

    # Assert: Check response is a redirect to the static index
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"