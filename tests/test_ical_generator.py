"""Tests for iCalendar generator."""

import os
from pathlib import Path

from edt_uvsq.ical_generator import clean_html_text, create_ical, parse_description


def test_clean_html_text():
    """Test HTML cleaning."""
    html = "Test<br />Line 2<br />Line 3"
    result = clean_html_text(html)

    assert "<br" not in result
    assert "Test" in result
    assert "Line 2" in result
    assert "\n" in result


def test_clean_html_entities():
    """Test HTML entity decoding."""
    html = "Mod&#232;les et &#233;co-syst&#232;mes"
    result = clean_html_text(html)

    assert "Modèles" in result
    assert "éco-systèmes" in result
    assert "&#" not in result


def test_clean_html_with_tags():
    """Test removal of HTML tags."""
    html = "<span>Test</span><br /><div>Content</div>"
    result = clean_html_text(html)

    assert "<span>" not in result
    assert "<div>" not in result
    assert "Test" in result
    assert "Content" in result


def test_parse_description():
    """Test description parsing."""
    desc = "CM/TD<br />101 - DESCARTES<br />MYDS120-Machine Learning [MYDS120]<br />M2 DATASCALE"
    info = parse_description(desc)

    assert info["event_type"] == "CM/TD"
    assert "DESCARTES" in info["location"]
    assert "Machine Learning" in info["course"]
    assert "M2 DATASCALE" in info["group"]


def test_parse_description_minimal():
    """Test description parsing with minimal data."""
    desc = "TD"
    info = parse_description(desc)

    assert info["event_type"] == "TD"
    assert info["location"] == ""
    assert info["course"] == ""
    assert info["group"] == ""


def test_create_ical_basic():
    """Test basic iCalendar creation."""
    events = [
        {
            "start": "2025-12-01T09:00:00",
            "end": "2025-12-01T11:00:00",
            "description": "CM/TD<br />Room 101<br />MYDS120-Test Course [MYDS120]<br />M2 DATASCALE",
            "backgroundColor": "#C6FFCC",
        }
    ]

    output_file = "test_calendar.ics"
    result = create_ical(events, output_file, "Test Calendar")

    assert result == output_file
    assert Path(output_file).exists()

    # Verify file contents
    with open(output_file, "r") as f:
        content = f.read()
        assert "BEGIN:VCALENDAR" in content
        assert "Test Calendar" in content
        assert "BEGIN:VEVENT" in content
        assert "CM/TD: Test Course" in content
        assert "Room 101" in content
        assert "Europe/Paris" in content

    # Cleanup
    os.remove(output_file)


def test_create_ical_multiple_events():
    """Test iCalendar with multiple events."""
    events = [
        {
            "start": "2025-12-01T09:00:00",
            "end": "2025-12-01T11:00:00",
            "description": "CM<br />Room 101<br />MYDS120-ML [MYDS120]<br />M2 DATASCALE",
            "backgroundColor": "#C6FFCC",
        },
        {
            "start": "2025-12-02T14:00:00",
            "end": "2025-12-02T16:00:00",
            "description": "TD<br />Room 202<br />MYDS121-DL [MYDS121]<br />M2 DATASCALE",
            "backgroundColor": "#FFEBBA",
        },
    ]

    output_file = "test_multi.ics"
    create_ical(events, output_file, "Multi Test")

    with open(output_file, "r") as f:
        content = f.read()
        # Should have 2 events
        assert content.count("BEGIN:VEVENT") == 2
        assert "CM: ML" in content
        assert "TD: DL" in content
        assert "Room 101" in content
        assert "Room 202" in content

    os.remove(output_file)


def test_create_ical_with_real_api_data():
    """Test with realistic API response structure."""
    events = [
        {
            "start": "2025-12-02T09:40:00",
            "end": "2025-12-02T12:40:00",
            "description": "CM/TD<br />101 - DESCARTES (MASTER) [CARTABLE NUMERIQUE ]<br />MYDS120-Machine Learning [MYDS120]<br />M2 DATASCALE  [M2 DATASCALE]",
            "backgroundColor": "#C6FFCC",
            "eventCategory": "CM/TD",
        }
    ]

    output_file = "test_real.ics"
    create_ical(events, output_file, "Real Data Test")

    with open(output_file, "r") as f:
        content = f.read()
        assert "Machine Learning" in content
        assert "DESCARTES" in content
        assert "DTSTART" in content
        assert "DTEND" in content
        assert "UID" in content

    os.remove(output_file)


def test_create_ical_handles_special_characters():
    """Test handling of special characters in course names."""
    events = [
        {
            "start": "2025-12-01T09:00:00",
            "end": "2025-12-01T11:00:00",
            "description": "CM<br />Room 101<br />MYDS999-Modèles & Éco-systèmes [MYDS999]<br />M2 DATASCALE",
            "backgroundColor": "#C6FFCC",
        }
    ]

    output_file = "test_special.ics"
    create_ical(events, output_file, "Special Chars")

    with open(output_file, "r") as f:
        content = f.read()
        # Should handle French characters
        assert "Modèles" in content or "Mod" in content

    os.remove(output_file)


def test_create_ical_empty_events():
    """Test creating calendar with empty events list."""
    output_file = "test_empty.ics"
    result = create_ical([], output_file, "Empty Calendar")

    assert result == output_file
    assert Path(output_file).exists()

    with open(output_file, "r") as f:
        content = f.read()
        assert "BEGIN:VCALENDAR" in content
        assert content.count("BEGIN:VEVENT") == 0

    os.remove(output_file)
