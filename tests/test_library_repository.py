from unittest.mock import Mock

from anime_calendar.integrations.supabase.repositories import SupabaseLibraryRepository
from anime_calendar.personalization.library import LibraryEntry, WatchStatus


def test_save_library_entry_uses_owner_scoped_upsert() -> None:
    client = Mock()
    repo = SupabaseLibraryRepository(client, "jwt")
    entry = LibraryEntry("user-1", 42, WatchStatus.WATCHING, progress=2)

    repo.save_entry(entry)

    args, kwargs = client.request.call_args
    assert args[:2] == ("POST", "library_entries")
    assert kwargs["access_token"] == "jwt"
    assert kwargs["json"]["owner_id"] == "user-1"


def test_delete_library_entry_is_scoped_to_owner_and_series() -> None:
    client = Mock()
    repo = SupabaseLibraryRepository(client, "jwt")

    repo.delete_entry("user-1", 42)

    _, kwargs = client.request.call_args
    assert kwargs["params"] == {"owner_id": "eq.user-1", "anilist_id": "eq.42"}
