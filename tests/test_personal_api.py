from datetime import UTC, datetime

import pytest

from anime_calendar.application.personal_api import PersonalApiContext, PersonalApiService
from anime_calendar.personalization.library import LibraryEntry, WatchStatus
from anime_calendar.personalization.models import (
    PersonalCalendar,
    UserIdentity,
    UserPreferences,
    UserProfile,
)
from anime_calendar.personalization.persistence import AccountExport


class MemoryProfiles:
    def __init__(self):
        self.value = None

    def get_profile(self, user_id):
        return self.value

    def save_profile(self, profile):
        self.value = profile


class MemoryPreferences:
    def __init__(self):
        self.value = UserPreferences()

    def get_preferences(self, user_id):
        return self.value

    def save_preferences(self, user_id, preferences):
        self.value = preferences


class MemoryCalendars:
    def __init__(self):
        self.values = {}
        self.tokens = {}

    def get_calendar(self, calendar_id):
        return self.values.get(calendar_id)

    def list_calendars(self, owner_id):
        return tuple(v for v in self.values.values() if v.owner_id == owner_id)

    def save_calendar(self, calendar):
        self.values[calendar.calendar_id] = calendar

    def save_feed_token_hash(self, calendar_id, token_hash):
        self.tokens[calendar_id] = token_hash

    def resolve_calendar_by_token_hash(self, token_hash):
        return None


class MemoryLibrary:
    def __init__(self):
        self.values = {}

    def get_entry(self, owner_id, anilist_id):
        return self.values.get((owner_id, anilist_id))

    def list_entries(self, owner_id):
        return tuple(v for (o, _), v in self.values.items() if o == owner_id)

    def save_entry(self, entry):
        self.values[(entry.owner_id, entry.anilist_id)] = entry

    def delete_entry(self, owner_id, anilist_id):
        self.values.pop((owner_id, anilist_id), None)


class MemoryAccounts:
    def __init__(self, identity):
        self.identity = identity
        self.deleted = False

    def export_account(self, user_id):
        return AccountExport(self.identity, None, UserPreferences(), datetime.now(UTC))

    def delete_account_data(self, user_id):
        self.deleted = True


def make_service():
    identity = UserIdentity("user-1")
    profiles, preferences, calendars, library = (
        MemoryProfiles(),
        MemoryPreferences(),
        MemoryCalendars(),
        MemoryLibrary(),
    )
    accounts = MemoryAccounts(identity)
    service = PersonalApiService(
        profiles=profiles,
        preferences=preferences,
        calendars=calendars,
        library=library,
        accounts=accounts,
    )
    return service, profiles, preferences, calendars, library, accounts, identity


def test_context_rejects_empty_user_id():
    with pytest.raises(ValueError):
        PersonalApiContext(" ")


def test_profile_save_requires_owner():
    service, profiles, *_rest, identity = make_service()
    profile = UserProfile(identity, "Brad")
    service.save_profile(PersonalApiContext("user-1"), profile)
    assert profiles.value == profile
    with pytest.raises(PermissionError):
        service.save_profile(PersonalApiContext("other"), profile)


def test_preferences_round_trip():
    service, _, preferences, *_ = make_service()
    value = UserPreferences(favorite_genres=frozenset({"Action"}))
    context = PersonalApiContext("user-1")
    service.save_preferences(context, value)
    assert service.get_preferences(context) == value


def test_calendar_save_list_and_feed_token():
    service, _, _, calendars, *_ = make_service()
    context = PersonalApiContext("user-1")
    calendar = PersonalCalendar("cal-1", "user-1", "My Anime")
    service.save_calendar(context, calendar)
    assert service.list_calendars(context) == (calendar,)
    token = service.issue_feed_token(context, "cal-1")
    assert calendars.tokens["cal-1"] == token.token_hash
    assert token.plaintext


def test_feed_token_rejects_foreign_calendar():
    service, _, _, calendars, *_ = make_service()
    calendars.save_calendar(PersonalCalendar("cal-1", "user-1", "Mine"))
    with pytest.raises(PermissionError):
        service.issue_feed_token(PersonalApiContext("other"), "cal-1")


def test_library_crud_is_owner_scoped():
    service, *_, library, _accounts, _identity = make_service()
    context = PersonalApiContext("user-1")
    entry = LibraryEntry("user-1", 7, WatchStatus.WATCHING)
    service.save_library_entry(context, entry)
    assert service.list_library(context) == (entry,)
    service.delete_library_entry(context, 7)
    assert service.list_library(context) == ()


def test_foreign_library_entry_is_rejected():
    service, *_ = make_service()
    with pytest.raises(PermissionError):
        service.save_library_entry(
            PersonalApiContext("user-1"), LibraryEntry("other", 7, WatchStatus.WATCHING)
        )


def test_export_and_delete_use_authenticated_user():
    service, *_, accounts, identity = make_service()
    context = PersonalApiContext("user-1")
    assert service.export_account(context).identity == identity
    service.delete_application_data(context)
    assert accounts.deleted is True


def test_health_is_framework_neutral():
    result = PersonalApiService.health()
    assert result["status"] == "ok"
    assert "checked_at" in result
