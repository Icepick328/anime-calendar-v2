from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol


class WatchStatus(StrEnum):
    WATCHING = "watching"
    PLAN_TO_WATCH = "plan_to_watch"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"


@dataclass(frozen=True, slots=True)
class LibraryEntry:
    owner_id: str
    anilist_id: int
    status: WatchStatus
    progress: int = 0
    score: int | None = None
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.owner_id.strip():
            raise ValueError("owner_id must not be empty")
        if self.anilist_id <= 0:
            raise ValueError("anilist_id must be positive")
        if self.progress < 0:
            raise ValueError("progress must not be negative")
        if self.score is not None and not 0 <= self.score <= 100:
            raise ValueError("score must be between 0 and 100")
        if self.created_at.tzinfo is None or self.updated_at.tzinfo is None:
            raise ValueError("library timestamps must be timezone-aware")

    def with_progress(self, progress: int) -> LibraryEntry:
        return LibraryEntry(
            owner_id=self.owner_id,
            anilist_id=self.anilist_id,
            status=self.status,
            progress=progress,
            score=self.score,
            notes=self.notes,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
        )


@dataclass(frozen=True, slots=True)
class LibraryFilter:
    included_statuses: frozenset[WatchStatus] = frozenset()
    hide_released_progress: bool = True
    include_unlisted_series: bool = True


class LibraryRepository(Protocol):
    def get_entry(self, owner_id: str, anilist_id: int) -> LibraryEntry | None: ...

    def list_entries(self, owner_id: str) -> tuple[LibraryEntry, ...]: ...

    def save_entry(self, entry: LibraryEntry) -> None: ...

    def delete_entry(self, owner_id: str, anilist_id: int) -> None: ...
