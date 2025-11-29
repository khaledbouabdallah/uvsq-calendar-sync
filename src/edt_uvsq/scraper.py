"""Scraper for UVSQ calendar API."""

from datetime import datetime, timedelta
from typing import Optional

import requests


def fetch_calendar_events(
    group_id: str = "M2 DATASCALE", year: int = 2025, month: int = 12
) -> Optional[list[dict]]:
    """
    Fetch calendar events from UVSQ API for a specific month.

    Args:
        group_id: Group identifier (e.g., "M2 DATASCALE")
        year: Year (e.g., 2025)
        month: Month (1-12)

    Returns:
        List of event dictionaries, or None if request fails

    Example:
        >>> events = fetch_calendar_events("M2 DATASCALE", 2025, 12)
        >>> len(events) > 0
        True
    """
    session = requests.Session()
    session.get(
        f"https://edt.uvsq.fr/cal?vt=month&dt={year}-{month:02d}-01&et=group&fid0={group_id}",
        headers={"User-Agent": "Mozilla/5.0"},
    )

    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=34)

    url = "https://edt.uvsq.fr/Home/GetCalendarData"

    data = {
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"),
        "resType": "103",
        "calView": "month",
        "federationIds[]": group_id,
        "colourScheme": "3",
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://edt.uvsq.fr/cal?vt=month&dt={year}-{month:02d}-01&et=group&fid0={group_id.replace(' ', '%20')}",
    }

    try:
        response = session.post(url, data=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
        return None


def fetch_semester(
    group_id: str = "M2 DATASCALE",
    start_month: int = 9,
    end_month: int = 12,
    year: int = 2025,
) -> list[dict]:
    """
    Fetch calendar events for multiple months.

    Args:
        group_id: Group identifier
        start_month: Starting month (1-12)
        end_month: Ending month (1-12)
        year: Year

    Returns:
        List of unique event dictionaries

    Example:
        >>> events = fetch_semester("M2 DATASCALE", 9, 12, 2025)
        >>> len(events) > 0
        True
    """
    all_events = []

    for month in range(start_month, end_month + 1):
        print(f"Fetching {year}-{month:02d}...")
        events = fetch_calendar_events(group_id, year, month)
        if events:
            all_events.extend(events)

    # Remove duplicates based on start time, end time, and description
    seen = set()
    unique_events = []
    for event in all_events:
        # Use more fields for deduplication
        key = (
            event.get("start"),
            event.get("end"),
            event.get("description"),
            event.get("eventCategory"),  # Add this for better uniqueness
        )
        if key not in seen:
            seen.add(key)
            unique_events.append(event)

    duplicates_removed = len(all_events) - len(unique_events)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate events")

    return unique_events
