from datetime import UTC, datetime

from anime_calendar.integrations.supabase.serialization import (
    personal_calendar_from_row,
    personal_calendar_to_row,
)
from anime_calendar.personalization.models import CalendarVisibility, PersonalCalendar


def test_personal_calendar_round_trip():
    now = datetime(2026, 7, 18, tzinfo=UTC)
    calendar = PersonalCalendar(
        "calendar-1",
        "user-1",
        "Dub Calendar",
        visibility=CalendarVisibility.UNLISTED,
        created_at=now,
        updated_at=now,
    )
    row = personal_calendar_to_row(calendar)
    row.update({"created_at": now.isoformat(), "updated_at": now.isoformat()})
    assert personal_calendar_from_row(row) == calendar
