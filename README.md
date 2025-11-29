# 🗓️ UVSQ Calendar Sync

Automatic synchronization of UVSQ course schedules to iCalendar format. Subscribe once, stay updated automatically.

[![Update Calendars](https://github.com/khaledbouabdallah/uvsq-calendar-sync/actions/workflows/update_calendar.yml/badge.svg)](https://github.com/khaledbouabdallah/uvsq-calendar-sync/actions/workflows/update_calendar.yml)

## 📥 Subscribe to Your Calendar

### Available Calendars

- **M2 DATASCALE**: [Subscribe](webcal://raw.githubusercontent.com/khaledbouabdallah/uvsq-calendar-sync/main/calendars/M2_DATASCALE.ics) | [View](https://raw.githubusercontent.com/khaledbouabdallah/uvsq-calendar-sync/main/calendars/M2_DATASCALE.ics)

### How to Subscribe

#### 📱 Apple Calendar (iPhone/Mac)
1. Click the "Subscribe" link above
2. Confirm subscription
3. Calendar updates automatically

#### 📧 Google Calendar
1. Copy the "View" link above
2. Open Google Calendar → Settings → Add calendar → From URL
3. Paste the link
4. Calendar syncs periodically

#### 💼 Outlook
1. Copy the "View" link
2. Open Outlook → Calendar → Add Calendar → Subscribe from web
3. Paste the link

## 🔧 For Developers

### Setup
```bash
# Clone repository
git clone https://github.com/khaledbouabdallah/uvsq-calendar-sync.git
cd uvsq-calendar-sync

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Generate calendars
uv run python generate_calendars.py
```

### Add Your Group

Edit `generate_calendars.py`:
```python
GROUPS = [
    {
        "id": "M2 DATASCALE",  # Your group ID from UVSQ EDT
        "name": "M2 DATASCALE - Data Science",
        "filename": "M2_DATASCALE.ics"
    },
    # Add your group here:
    {
        "id": "YOUR_GROUP_ID",
        "name": "Your Group Name",
        "filename": "YOUR_FILE.ics"
    },
]
```

### Run Tests
```bash
uv run pytest
```

### Manual Update
```bash
uv run python generate_calendars.py
```

## 🤖 Automatic Updates

Calendars update automatically every day at 6 AM UTC via GitHub Actions.

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Contributing

1. Fork the repository
2. Add your group to `generate_calendars.py`
3. Submit a pull request

## ⚠️ Disclaimer

This is an unofficial tool. Not affiliated with UVSQ.

---

Made with ❤️ for UVSQ students