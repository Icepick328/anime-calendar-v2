from __future__ import annotations

from datetime import datetime

from anime_calendar.models import ReleaseType, ReleaseVariant
from anime_calendar.personalization.models import (
    AccountStatus,
    UserIdentity,
    UserPreferences,
    UserProfile,
)


def identity_from_row(row: dict[str, object]) -> UserIdentity:
    return UserIdentity(
        user_id=str(row["user_id"]),
        email=str(row["email"]) if row.get("email") else None,
        status=AccountStatus(str(row.get("status", AccountStatus.ACTIVE.value))),
        created_at=datetime.fromisoformat(str(row["created_at"]).replace("Z", "+00:00")),
    )


def profile_from_row(row: dict[str, object], identity: UserIdentity) -> UserProfile:
    return UserProfile(
        identity=identity,
        display_name=str(row["display_name"]),
        timezone=str(row.get("timezone", "UTC")),
        locale=str(row.get("locale", "en-US")),
    )


def profile_to_row(profile: UserProfile) -> dict[str, object]:
    return {
        "user_id": profile.identity.user_id,
        "display_name": profile.display_name,
        "timezone": profile.timezone,
        "locale": profile.locale,
    }


def preferences_from_row(row: dict[str, object] | None) -> UserPreferences:
    if not row:
        return UserPreferences()
    return UserPreferences(
        favorite_genres=frozenset(row.get("favorite_genres", [])),
        excluded_genres=frozenset(row.get("excluded_genres", [])),
        favorite_studios=frozenset(row.get("favorite_studios", [])),
        preferred_provider_ids=frozenset(row.get("preferred_provider_ids", [])),
        preferred_release_types=frozenset(
            ReleaseType(value) for value in row.get("preferred_release_types", [])
        ),
        preferred_variants=frozenset(
            ReleaseVariant(value) for value in row.get("preferred_variants", [])
        ),
        favorite_anilist_ids=frozenset(int(value) for value in row.get("favorite_anilist_ids", [])),
        include_unmatched_releases=bool(row.get("include_unmatched_releases", True)),
    )


def preferences_to_row(user_id: str, preferences: UserPreferences) -> dict[str, object]:
    return {
        "user_id": user_id,
        "favorite_genres": sorted(preferences.favorite_genres),
        "excluded_genres": sorted(preferences.excluded_genres),
        "favorite_studios": sorted(preferences.favorite_studios),
        "preferred_provider_ids": sorted(preferences.preferred_provider_ids),
        "preferred_release_types": sorted(
            value.value for value in preferences.preferred_release_types
        ),
        "preferred_variants": sorted(value.value for value in preferences.preferred_variants),
        "favorite_anilist_ids": sorted(preferences.favorite_anilist_ids),
        "include_unmatched_releases": preferences.include_unmatched_releases,
    }


def personal_calendar_from_row(row: dict[str, object]):
    from anime_calendar.personalization.models import CalendarVisibility, PersonalCalendar

    return PersonalCalendar(
        calendar_id=str(row["calendar_id"]),
        owner_id=str(row["owner_id"]),
        name=str(row["name"]),
        visibility=CalendarVisibility(str(row.get("visibility", "private"))),
        enabled=bool(row.get("enabled", True)),
        created_at=datetime.fromisoformat(str(row["created_at"]).replace("Z", "+00:00")),
        updated_at=datetime.fromisoformat(str(row["updated_at"]).replace("Z", "+00:00")),
    )


def personal_calendar_to_row(calendar) -> dict[str, object]:
    return {
        "calendar_id": calendar.calendar_id,
        "owner_id": calendar.owner_id,
        "name": calendar.name,
        "visibility": calendar.visibility.value,
        "enabled": calendar.enabled,
    }
