from __future__ import annotations

from typing import Protocol

from anime_calendar.personalization.models import UserPreferences


class PreferenceRepository(Protocol):
    """Persistence boundary for private user preferences."""

    def get_preferences(self, user_id: str) -> UserPreferences: ...

    def save_preferences(self, user_id: str, preferences: UserPreferences) -> None: ...
