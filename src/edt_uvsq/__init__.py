"""UVSQ Calendar Sync - Automatic iCalendar generation for UVSQ course schedules."""

__version__ = "1.0.0"

from .ical_generator import clean_html_text, create_ical, parse_description
from .scraper import fetch_calendar_events, fetch_semester

__all__ = [
    "fetch_calendar_events",
    "fetch_semester",
    "create_ical",
    "parse_description",
    "clean_html_text",
]
