from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from anime_calendar.personalization.calendars import FeedToken, PersonalCalendarRepository
from anime_calendar.personalization.library import LibraryEntry, LibraryRepository
from anime_calendar.personalization.models import PersonalCalendar, UserPreferences, UserProfile
from anime_calendar.personalization.persistence import AccountDataRepository, AccountExport


class ProfileRepository(Protocol):
    def get_profile(self, user_id: str) -> UserProfile | None: ...
    def save_profile(self, profile: UserProfile) -> None: ...


class PreferenceRepository(Protocol):
    def get_preferences(self, user_id: str) -> UserPreferences: ...
    def save_preferences(self, user_id: str, preferences: UserPreferences) -> None: ...


@dataclass(frozen=True, slots=True)
class PersonalApiContext:
    user_id: str

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty")


class PersonalApiService:
    """Authenticated, framework-neutral operations for the private user platform."""

    def __init__(
        self,
        *,
        profiles: ProfileRepository,
        preferences: PreferenceRepository,
        calendars: PersonalCalendarRepository,
        library: LibraryRepository,
        accounts: AccountDataRepository,
    ) -> None:
        self.profiles = profiles
        self.preferences = preferences
        self.calendars = calendars
        self.library = library
        self.accounts = accounts

    def get_profile(self, context: PersonalApiContext) -> UserProfile | None:
        return self.profiles.get_profile(context.user_id)

    def save_profile(self, context: PersonalApiContext, profile: UserProfile) -> None:
        self._require_owner(context, profile.identity.user_id)
        self.profiles.save_profile(profile)

    def get_preferences(self, context: PersonalApiContext) -> UserPreferences:
        return self.preferences.get_preferences(context.user_id)

    def save_preferences(self, context: PersonalApiContext, preferences: UserPreferences) -> None:
        self.preferences.save_preferences(context.user_id, preferences)

    def list_calendars(self, context: PersonalApiContext) -> tuple[PersonalCalendar, ...]:
        return self.calendars.list_calendars(context.user_id)

    def save_calendar(self, context: PersonalApiContext, calendar: PersonalCalendar) -> None:
        self._require_owner(context, calendar.owner_id)
        self.calendars.save_calendar(calendar)

    def issue_feed_token(self, context: PersonalApiContext, calendar_id: str) -> FeedToken:
        calendar = self.calendars.get_calendar(calendar_id)
        if calendar is None:
            raise LookupError(f"calendar not found: {calendar_id}")
        self._require_owner(context, calendar.owner_id)
        token = FeedToken.issue(calendar_id)
        self.calendars.save_feed_token_hash(calendar_id, token.token_hash)
        return token

    def list_library(self, context: PersonalApiContext) -> tuple[LibraryEntry, ...]:
        return self.library.list_entries(context.user_id)

    def save_library_entry(self, context: PersonalApiContext, entry: LibraryEntry) -> None:
        self._require_owner(context, entry.owner_id)
        self.library.save_entry(entry)

    def delete_library_entry(self, context: PersonalApiContext, anilist_id: int) -> None:
        self.library.delete_entry(context.user_id, anilist_id)

    def export_account(self, context: PersonalApiContext) -> AccountExport:
        return self.accounts.export_account(context.user_id)

    def delete_application_data(self, context: PersonalApiContext) -> None:
        self.accounts.delete_account_data(context.user_id)

    @staticmethod
    def health() -> dict[str, object]:
        return {"status": "ok", "checked_at": datetime.now(UTC).isoformat()}

    @staticmethod
    def _require_owner(context: PersonalApiContext, owner_id: str) -> None:
        if context.user_id != owner_id:
            raise PermissionError("resource does not belong to authenticated user")
