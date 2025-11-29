#!/usr/bin/env python3
"""Generate calendar files for configured groups."""

from pathlib import Path
from datetime import datetime
import sys
from edt_uvsq import fetch_semester, create_ical


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

    failed_groups = []
    success_count = 0

    for group in GROUPS:
        print(f"\n📚 Processing: {group['name']}")

        try:
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

            if not all_events:
                print(f"⚠️  No events found for {group['name']}")
                failed_groups.append(group["name"])
                continue

            # Write to temporary file first
            output_path = output_dir / group["filename"]
            temp_path = output_dir / f"{group['filename']}.tmp"

            create_ical(all_events, str(temp_path), group["name"])

            # Only replace if successful
            temp_path.replace(output_path)
            print(f"✅ Generated: {output_path} ({len(all_events)} events)")
            success_count += 1

        except Exception as e:
            print(f"❌ Error processing {group['name']}: {e}")
            failed_groups.append(group["name"])
            continue

    print("\n" + "=" * 60)
    print(f"✨ Complete: {success_count}/{len(GROUPS)} calendars updated")

    if failed_groups:
        print(f"⚠️  Failed: {', '.join(failed_groups)}")
        sys.exit(1)  # Exit with error code for CI/CD

    print("✨ All calendars updated successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
