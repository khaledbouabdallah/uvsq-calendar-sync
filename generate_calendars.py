#!/usr/bin/env python3
"""Generate calendar files for configured groups."""

from pathlib import Path
from datetime import datetime
from src.edt_uvsq import fetch_semester, create_ical


# Configuration: Add your groups here
GROUPS = [
    {
        "id": "M2 DATASCALE",
        "name": "M2 DATASCALE - Data Science",
        "filename": "M2_DATASCALE.ics",
    },
    # Add more groups here:
    # {
    #     "id": "M1 INFO",
    #     "name": "M1 Informatique",
    #     "filename": "M1_INFO.ics"
    # },
]

# Academic year configuration
CURRENT_YEAR = 2025
NEXT_YEAR = 2026


def main():
    """Generate all calendar files."""
    output_dir = Path("calendars")
    output_dir.mkdir(exist_ok=True)

    print(f"🗓️  Generating calendars - {datetime.now()}")
    print("=" * 60)

    for group in GROUPS:
        print(f"\n📚 Processing: {group['name']}")

        # Fetch semester 1 (Sep-Dec)
        events_s1 = fetch_semester(
            group_id=group["id"], start_month=9, end_month=12, year=CURRENT_YEAR
        )

        # Fetch semester 2 (Jan-Aug)
        events_s2 = fetch_semester(
            group_id=group["id"], start_month=1, end_month=8, year=NEXT_YEAR
        )

        # Combine
        all_events = events_s1 + events_s2

        if all_events:
            # Generate calendar
            output_path = output_dir / group["filename"]
            create_ical(all_events, str(output_path), group["name"])
            print(f"✅ Generated: {output_path} ({len(all_events)} events)")
        else:
            print(f"⚠️  No events found for {group['name']}")

    print("\n" + "=" * 60)
    print("✨ Done!")


if __name__ == "__main__":
    main()
