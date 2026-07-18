from datetime import UTC, datetime
from unittest.mock import Mock

from anime_calendar.integrations.supabase.repositories import (
    SupabaseIdentityRepository,
    SupabasePreferenceRepository,
)
from anime_calendar.personalization.models import UserIdentity, UserPreferences, UserProfile


def test_save_profile_uses_user_scoped_upsert() -> None:
    client = Mock()
    repo = SupabaseIdentityRepository(client, "jwt")
    profile = UserProfile(
        identity=UserIdentity("user-1", created_at=datetime.now(UTC)),
        display_name="Brad",
        timezone="America/Los_Angeles",
    )

    repo.save_profile(profile)

    client.request.assert_called_once()
    args, kwargs = client.request.call_args
    assert args[:2] == ("POST", "profiles")
    assert kwargs["access_token"] == "jwt"
    assert kwargs["prefer"].startswith("resolution=merge-duplicates")


def test_missing_preferences_return_safe_defaults() -> None:
    client = Mock()
    client.request.return_value = []
    repo = SupabasePreferenceRepository(client, "jwt")

    assert repo.get_preferences("user-1") == UserPreferences()
