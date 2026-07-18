from datetime import UTC, datetime

import pytest

from anime_calendar.models import ReleaseType, ReleaseVariant
from anime_calendar.personalization.models import (
    PersonalCalendar,
    UserIdentity,
    UserPreferences,
    UserProfile,
)


def test_identity_requires_nonempty_id() -> None:
    with pytest.raises(ValueError, match="user_id"):
        UserIdentity(user_id="")


def test_identity_requires_timezone_aware_creation_time() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        UserIdentity(user_id="user-1", created_at=datetime(2026, 7, 17))


def test_profile_validates_timezone() -> None:
    identity = UserIdentity(user_id="user-1", created_at=datetime.now(UTC))

    with pytest.raises(ValueError, match="unknown timezone"):
        UserProfile(identity=identity, display_name="Brad", timezone="Mars/Olympus")


def test_preferences_reject_conflicting_genres() -> None:
    with pytest.raises(ValueError, match="both favorite and excluded"):
        UserPreferences(
            favorite_genres=frozenset({"Action"}),
            excluded_genres=frozenset({"action"}),
        )


def test_preferences_accept_typed_release_filters() -> None:
    preferences = UserPreferences(
        preferred_release_types=frozenset({ReleaseType.EPISODE}),
        preferred_variants=frozenset({ReleaseVariant.DUB}),
    )

    assert ReleaseType.EPISODE in preferences.preferred_release_types
    assert ReleaseVariant.DUB in preferences.preferred_variants


def test_personal_calendar_requires_owner() -> None:
    with pytest.raises(ValueError, match="owner_id"):
        PersonalCalendar(calendar_id="calendar-1", owner_id="", name="Dub Calendar")
