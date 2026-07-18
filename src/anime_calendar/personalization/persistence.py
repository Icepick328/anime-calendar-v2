from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Protocol

from anime_calendar.personalization.models import UserIdentity, UserPreferences, UserProfile


@dataclass(frozen=True, slots=True)
class AccountExport:
    """Portable representation of all private data owned by one account."""

    identity: UserIdentity
    profile: UserProfile | None
    preferences: UserPreferences
    exported_at: datetime

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["exported_at"] = self.exported_at.isoformat()
        data["identity"]["created_at"] = self.identity.created_at.isoformat()  # type: ignore[index]
        return data


class AccountDataRepository(Protocol):
    """Persistence operations needed for private account lifecycle management."""

    def export_account(self, user_id: str) -> AccountExport: ...

    def delete_account_data(self, user_id: str) -> None: ...
