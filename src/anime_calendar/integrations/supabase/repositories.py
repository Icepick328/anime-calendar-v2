from __future__ import annotations

from datetime import UTC, datetime

from anime_calendar.integrations.supabase.client import SupabaseRestClient
from anime_calendar.integrations.supabase.serialization import (
    identity_from_row,
    preferences_from_row,
    preferences_to_row,
    profile_from_row,
    profile_to_row,
)
from anime_calendar.personalization.models import UserIdentity, UserPreferences, UserProfile
from anime_calendar.personalization.persistence import AccountExport


class _UserScopedRepository:
    def __init__(self, client: SupabaseRestClient, access_token: str) -> None:
        self.client = client
        self.access_token = access_token

    def _get_one(self, table: str, user_id: str) -> dict[str, object] | None:
        rows = self.client.request(
            "GET",
            table,
            access_token=self.access_token,
            params={"user_id": f"eq.{user_id}", "select": "*", "limit": "1"},
        )
        return rows[0] if rows else None


class SupabaseIdentityRepository(_UserScopedRepository):
    def get_identity(self, user_id: str) -> UserIdentity | None:
        row = self._get_one("account_identities", user_id)
        return identity_from_row(row) if row else None

    def get_profile(self, user_id: str) -> UserProfile | None:
        identity = self.get_identity(user_id)
        row = self._get_one("profiles", user_id)
        if not identity or not row:
            return None
        return profile_from_row(row, identity)

    def save_profile(self, profile: UserProfile) -> None:
        self.client.request(
            "POST",
            "profiles",
            access_token=self.access_token,
            json=profile_to_row(profile),
            prefer="resolution=merge-duplicates,return=minimal",
        )


class SupabasePreferenceRepository(_UserScopedRepository):
    def get_preferences(self, user_id: str) -> UserPreferences:
        return preferences_from_row(self._get_one("user_preferences", user_id))

    def save_preferences(self, user_id: str, preferences: UserPreferences) -> None:
        self.client.request(
            "POST",
            "user_preferences",
            access_token=self.access_token,
            json=preferences_to_row(user_id, preferences),
            prefer="resolution=merge-duplicates,return=minimal",
        )


class SupabaseAccountRepository(_UserScopedRepository):
    def export_account(self, user_id: str) -> AccountExport:
        identities = SupabaseIdentityRepository(self.client, self.access_token)
        identity = identities.get_identity(user_id)
        if identity is None:
            raise LookupError(f"account not found: {user_id}")
        profile = identities.get_profile(user_id)
        preferences = SupabasePreferenceRepository(
            self.client, self.access_token
        ).get_preferences(user_id)
        return AccountExport(
            identity=identity,
            profile=profile,
            preferences=preferences,
            exported_at=datetime.now(UTC),
        )

    def delete_account_data(self, user_id: str) -> None:
        self.client.request(
            "POST",
            "rpc/delete_my_account_data",
            access_token=self.access_token,
            json={"requested_user_id": user_id},
            prefer="return=minimal",
        )


class SupabasePersonalCalendarRepository(_UserScopedRepository):
    def get_calendar(self, calendar_id: str):
        from anime_calendar.integrations.supabase.serialization import personal_calendar_from_row

        rows = self.client.request(
            "GET",
            "personal_calendars",
            access_token=self.access_token,
            params={"calendar_id": f"eq.{calendar_id}", "select": "*", "limit": "1"},
        )
        return personal_calendar_from_row(rows[0]) if rows else None

    def list_calendars(self, owner_id: str):
        from anime_calendar.integrations.supabase.serialization import personal_calendar_from_row

        rows = self.client.request(
            "GET",
            "personal_calendars",
            access_token=self.access_token,
            params={"owner_id": f"eq.{owner_id}", "select": "*", "order": "created_at.asc"},
        )
        return tuple(personal_calendar_from_row(row) for row in rows or [])

    def save_calendar(self, calendar) -> None:
        from anime_calendar.integrations.supabase.serialization import personal_calendar_to_row

        self.client.request(
            "POST",
            "personal_calendars",
            access_token=self.access_token,
            json=personal_calendar_to_row(calendar),
            prefer="resolution=merge-duplicates,return=minimal",
        )

    def save_feed_token_hash(self, calendar_id: str, token_hash: str) -> None:
        self.client.request(
            "POST",
            "personal_calendar_tokens",
            access_token=self.access_token,
            json={"calendar_id": calendar_id, "token_hash": token_hash},
            prefer="resolution=merge-duplicates,return=minimal",
        )

    def resolve_calendar_by_token_hash(self, token_hash: str):
        from anime_calendar.integrations.supabase.serialization import personal_calendar_from_row

        rows = self.client.request(
            "POST",
            "rpc/resolve_personal_calendar",
            access_token=self.access_token,
            json={"presented_token_hash": token_hash},
        )
        return personal_calendar_from_row(rows[0]) if rows else None


class SupabaseLibraryRepository(_UserScopedRepository):
    def get_entry(self, owner_id: str, anilist_id: int):
        from anime_calendar.integrations.supabase.serialization import library_entry_from_row

        rows = self.client.request(
            "GET",
            "library_entries",
            access_token=self.access_token,
            params={
                "owner_id": f"eq.{owner_id}",
                "anilist_id": f"eq.{anilist_id}",
                "select": "*",
                "limit": "1",
            },
        )
        return library_entry_from_row(rows[0]) if rows else None

    def list_entries(self, owner_id: str):
        from anime_calendar.integrations.supabase.serialization import library_entry_from_row

        rows = self.client.request(
            "GET",
            "library_entries",
            access_token=self.access_token,
            params={"owner_id": f"eq.{owner_id}", "select": "*", "order": "updated_at.desc"},
        )
        return tuple(library_entry_from_row(row) for row in rows or [])

    def save_entry(self, entry) -> None:
        from anime_calendar.integrations.supabase.serialization import library_entry_to_row

        self.client.request(
            "POST",
            "library_entries",
            access_token=self.access_token,
            json=library_entry_to_row(entry),
            prefer="resolution=merge-duplicates,return=minimal",
        )

    def delete_entry(self, owner_id: str, anilist_id: int) -> None:
        self.client.request(
            "DELETE",
            "library_entries",
            access_token=self.access_token,
            params={"owner_id": f"eq.{owner_id}", "anilist_id": f"eq.{anilist_id}"},
            prefer="return=minimal",
        )
