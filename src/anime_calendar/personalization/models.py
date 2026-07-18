from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from anime_calendar.models import ReleaseType, ReleaseVariant


class AccountStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"
    PENDING = "pending"


class CalendarVisibility(StrEnum):
    PRIVATE = "private"
    UNLISTED = "unlisted"


@dataclass(frozen=True, slots=True)
class UserIdentity:
    user_id: str
    email: str | None = None
    status: AccountStatus = AccountStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class UserProfile:
    identity: UserIdentity
    display_name: str
    timezone: str = "UTC"
    locale: str = "en-US"

    def __post_init__(self) -> None:
        if not self.display_name.strip():
            raise ValueError("display_name must not be empty")
        try:
            ZoneInfo(self.timezone)
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"unknown timezone: {self.timezone}") from error


@dataclass(frozen=True, slots=True)
class UserPreferences:
    favorite_genres: frozenset[str] = frozenset()
    excluded_genres: frozenset[str] = frozenset()
    favorite_studios: frozenset[str] = frozenset()
    preferred_provider_ids: frozenset[str] = frozenset()
    preferred_release_types: frozenset[ReleaseType] = frozenset()
    preferred_variants: frozenset[ReleaseVariant] = frozenset()
    favorite_anilist_ids: frozenset[int] = frozenset()
    include_unmatched_releases: bool = True

    def __post_init__(self) -> None:
        overlap = self._normalized(self.favorite_genres) & self._normalized(self.excluded_genres)
        if overlap:
            names = ", ".join(sorted(overlap))
            raise ValueError(f"genres cannot be both favorite and excluded: {names}")

    @staticmethod
    def _normalized(values: frozenset[str]) -> frozenset[str]:
        return frozenset(value.strip().casefold() for value in values if value.strip())


@dataclass(frozen=True, slots=True)
class PersonalCalendar:
    calendar_id: str
    owner_id: str
    name: str
    visibility: CalendarVisibility = CalendarVisibility.PRIVATE
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.calendar_id.strip():
            raise ValueError("calendar_id must not be empty")
        if not self.owner_id.strip():
            raise ValueError("owner_id must not be empty")
        if not self.name.strip():
            raise ValueError("name must not be empty")
