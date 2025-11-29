"""Tests for scraper module."""

from edt_uvsq.scraper import fetch_calendar_events, fetch_semester


def test_fetch_calendar_events():
    """Test fetching events for a single month."""
    events = fetch_calendar_events("M2 DATASCALE", 2025, 12)

    assert events is not None
    assert isinstance(events, list)
    if events:
        assert "start" in events[0]
        assert "end" in events[0]
        assert "description" in events[0]


def test_fetch_semester(capsys):
    """Test fetching events for multiple months."""
    events = fetch_semester("M2 DATASCALE", 12, 12, 2025)

    assert isinstance(events, list)
    assert len(events) > 0

    # Check for duplicates - all events should be unique
    event_keys = [(e.get("start"), e.get("description")) for e in events]
    unique_keys = set(event_keys)

    assert len(event_keys) == len(unique_keys), (
        f"Found {len(event_keys) - len(unique_keys)} duplicates"
    )

    # Verify print output
    captured = capsys.readouterr()
    assert "Fetching 2025-12" in captured.out


def test_invalid_group():
    """Test handling of invalid group ID."""
    events = fetch_calendar_events("INVALID_GROUP_XYZ", 2025, 12)

    # Should return empty list or None
    assert events is None or len(events) == 0


def test_fetch_calendar_events_network_error(monkeypatch):
    """Test handling of network errors."""
    import requests

    def mock_post(*args, **kwargs):
        raise requests.RequestException("Network error")

    monkeypatch.setattr("requests.Session.post", mock_post)

    result = fetch_calendar_events("M2 DATASCALE", 2025, 12)
    assert result is None


def test_fetch_calendar_events_http_error(monkeypatch):
    """Test handling of HTTP errors."""
    import requests

    class MockResponse:
        def raise_for_status(self):
            raise requests.HTTPError("404 Not Found")

        def json(self):
            return []

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.Session.post", mock_post)

    result = fetch_calendar_events("M2 DATASCALE", 2025, 12)
    assert result is None


def test_fetch_semester_handles_none_response():
    """Test that fetch_semester handles None responses gracefully."""
    # This will naturally occur if network fails
    # Just verify it doesn't crash and returns empty list
    events = fetch_semester("INVALID_GROUP_XYZ_999", 12, 12, 2025)
    assert isinstance(events, list)
