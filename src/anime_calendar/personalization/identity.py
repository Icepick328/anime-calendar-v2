from __future__ import annotations

from typing import Protocol

from anime_calendar.personalization.models import UserIdentity, UserProfile


class IdentityRepository(Protocol):
    """Persistence boundary for user identity and profile data."""

    def get_identity(self, user_id: str) -> UserIdentity | None: ...

    def get_profile(self, user_id: str) -> UserProfile | None: ...

    def save_profile(self, profile: UserProfile) -> None: ...
