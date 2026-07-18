from datetime import UTC, datetime

from anime_calendar.integrations.supabase.serialization import (
    identity_from_row,
    preferences_from_row,
    preferences_to_row,
    profile_from_row,
)
from anime_calendar.models import ReleaseType, ReleaseVariant
from anime_calendar.personalization.models import UserPreferences


def test_identity_and_profile_deserialize() -> None:
    identity = identity_from_row(
        {
            "user_id": "user-1",
            "email": "brad@example.com",
            "status": "active",
            "created_at": "2026-07-18T01:00:00+00:00",
        }
    )
    profile = profile_from_row(
        {"display_name": "Brad", "timezone": "America/Los_Angeles", "locale": "en-US"},
        identity,
    )

    assert identity.created_at == datetime(2026, 7, 18, 1, tzinfo=UTC)
    assert profile.timezone == "America/Los_Angeles"


def test_preferences_round_trip() -> None:
    preferences = UserPreferences(
        favorite_genres=frozenset({"Action"}),
        preferred_release_types=frozenset({ReleaseType.EPISODE}),
        preferred_variants=frozenset({ReleaseVariant.DUB}),
        favorite_anilist_ids=frozenset({10, 20}),
        include_unmatched_releases=False,
    )

    row = preferences_to_row("user-1", preferences)
    restored = preferences_from_row(row)

    assert restored == preferences
    assert row["user_id"] == "user-1"
