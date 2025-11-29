"""iCalendar generation utilities."""

import html
import re
from datetime import datetime

import pytz
from icalendar import Calendar, Event


def clean_html_text(text: str) -> str:
    """
    Remove HTML tags and decode entities.

    Args:
        text: HTML text to clean

    Returns:
        Cleaned text

    Example:
        >>> clean_html_text("Test<br />Line 2")
        'Test\\nLine 2'
    """
    text = html.unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def parse_description(desc_html: str) -> dict[str, str]:
    """
    Extract structured info from HTML description.

    Args:
        desc_html: HTML description from API

    Returns:
        Dictionary with event_type, location, course, group

    Example:
        >>> info = parse_description("CM/TD<br />Room 101<br />MYDS120")
        >>> info['event_type']
        'CM/TD'
    """
    desc = clean_html_text(desc_html)
    lines = [line.strip() for line in desc.split("\n") if line.strip()]

    return {
        "event_type": lines[0] if len(lines) > 0 else "",
        "location": lines[1] if len(lines) > 1 else "",
        "course": lines[2] if len(lines) > 2 else "",
        "group": lines[3] if len(lines) > 3 else "",
    }


def create_ical(
    events_data: list[dict],
    output_file: str = "calendar.ics",
    calendar_name: str = "UVSQ Calendar",
) -> str:
    """
    Create iCalendar file from event data.

    Args:
        events_data: List of event dictionaries from API
        output_file: Output filename
        calendar_name: Calendar display name

    Returns:
        Path to created file

    Example:
        >>> events = [{"start": "2025-12-01T09:00:00", "end": "2025-12-01T11:00:00", "description": "Test"}]
        >>> create_ical(events, "test.ics", "Test Calendar")
        'test.ics'
    """
    cal = Calendar()
    cal.add("prodid", f"-//{calendar_name}//uvsq.fr//")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", calendar_name)
    cal.add("x-wr-timezone", "Europe/Paris")

    tz = pytz.timezone("Europe/Paris")

    for event_data in events_data:
        event = Event()

        # Parse datetime
        start = event_data.get("start", "")
        end = event_data.get("end", "")

        start_dt = datetime.fromisoformat(start.replace("Z", ""))
        end_dt = datetime.fromisoformat(end.replace("Z", ""))

        start_dt = tz.localize(start_dt)
        end_dt = tz.localize(end_dt)

        # Parse description
        desc_html = event_data.get("description", "")
        info = parse_description(desc_html)

        # Build summary
        event_type = info["event_type"]
        course = info["course"]

        course_match = re.search(r"([A-Z0-9]+)-([^[]+)", course)
        if course_match:
            course_name = course_match.group(2).strip()
            summary = f"{event_type}: {course_name}"
        else:
            summary = f"{event_type}: {course}" if course else event_type

        # Remove trailing brackets
        summary = re.sub(r"\s*\[.*?\]\s*$", "", summary)

        # Build description
        desc_lines = [info["event_type"]]
        if info["course"]:
            desc_lines.append(info["course"])
        if info["group"]:
            desc_lines.append(info["group"])
        description = "\n".join(desc_lines)

        # Add event
        event.add("summary", summary)
        event.add("dtstart", start_dt)
        event.add("dtend", end_dt)
        event.add("location", info["location"])
        event.add("description", description)

        # Generate UID
        uid_str = f"{start_dt.isoformat()}-{summary}-{info['location']}"
        uid = f"{abs(hash(uid_str))}@uvsq.fr"
        event.add("uid", uid)

        # Add color
        if event_data.get("backgroundColor"):
            event.add("color", event_data["backgroundColor"])

        cal.add_component(event)

    # Write file
    with open(output_file, "wb") as f:
        f.write(cal.to_ical())

    return output_file
