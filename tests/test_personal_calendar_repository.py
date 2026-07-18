from datetime import UTC, datetime

from anime_calendar.integrations.supabase.repositories import SupabasePersonalCalendarRepository
from anime_calendar.personalization.models import CalendarVisibility, PersonalCalendar


class FakeClient:
    def __init__(self):
        self.calls = []
        self.responses = []

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return self.responses.pop(0) if self.responses else None


def row():
    return {
        "calendar_id": "cal-1",
        "owner_id": "user-1",
        "name": "My Anime",
        "visibility": "unlisted",
        "enabled": True,
        "created_at": datetime(2026, 7, 18, tzinfo=UTC).isoformat(),
        "updated_at": datetime(2026, 7, 18, tzinfo=UTC).isoformat(),
    }


def test_repository_lists_and_saves_calendars():
    client = FakeClient()
    client.responses = [[row()]]
    repository = SupabasePersonalCalendarRepository(client, "jwt")
    calendars = repository.list_calendars("user-1")
    assert calendars[0].visibility is CalendarVisibility.UNLISTED

    repository.save_calendar(PersonalCalendar("cal-2", "user-1", "Movies"))
    assert client.calls[-1][1] == "personal_calendars"


def test_repository_saves_hash_and_resolves_feed():
    client = FakeClient()
    repository = SupabasePersonalCalendarRepository(client, "jwt")
    repository.save_feed_token_hash("cal-1", "a" * 64)
    assert client.calls[-1][2]["json"]["token_hash"] == "a" * 64

    client.responses = [[row()]]
    resolved = repository.resolve_calendar_by_token_hash("a" * 64)
    assert resolved and resolved.calendar_id == "cal-1"
    assert client.calls[-1][1] == "rpc/resolve_personal_calendar"
