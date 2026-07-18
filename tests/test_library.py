from datetime import UTC, datetime

import pytest

from anime_calendar.personalization.library import LibraryEntry, WatchStatus


def test_library_entry_validates_progress() -> None:
    with pytest.raises(ValueError, match="progress"):
        LibraryEntry("user-1", 1, WatchStatus.WATCHING, progress=-1)


def test_library_entry_validates_score() -> None:
    with pytest.raises(ValueError, match="score"):
        LibraryEntry("user-1", 1, WatchStatus.COMPLETED, score=101)


def test_with_progress_preserves_identity_and_updates_progress() -> None:
    created = datetime(2026, 7, 18, tzinfo=UTC)
    entry = LibraryEntry(
        "user-1",
        42,
        WatchStatus.WATCHING,
        progress=3,
        created_at=created,
        updated_at=created,
    )

    updated = entry.with_progress(4)

    assert updated.progress == 4
    assert updated.owner_id == entry.owner_id
    assert updated.created_at == created
    assert updated.updated_at >= created
