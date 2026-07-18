from datetime import UTC, datetime

from anime_calendar.integrations.supabase.serialization import (
    library_entry_from_row,
    library_entry_to_row,
)
from anime_calendar.personalization.library import LibraryEntry, WatchStatus


def test_library_entry_round_trip() -> None:
    now = datetime(2026, 7, 18, 1, 2, tzinfo=UTC)
    entry = LibraryEntry(
        owner_id="user-1",
        anilist_id=42,
        status=WatchStatus.WATCHING,
        progress=3,
        score=90,
        notes="Great show",
        created_at=now,
        updated_at=now,
    )
    row = library_entry_to_row(entry) | {
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }

    restored = library_entry_from_row(row)

    assert restored == entry
