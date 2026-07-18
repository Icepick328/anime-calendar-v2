from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime

from anime_calendar.models import Release
from anime_calendar.personalization.filters import FilterDecision, evaluate_release
from anime_calendar.personalization.library import LibraryEntry, LibraryFilter
from anime_calendar.personalization.models import UserPreferences


@dataclass(frozen=True, slots=True)
class PersonalizedRelease:
    release: Release
    decision: FilterDecision


class PersonalizationEngine:
    """Creates deterministic user-specific views without mutating public release data."""

    def evaluate(
        self,
        releases: Iterable[Release],
        preferences: UserPreferences,
        *,
        library_entries: Iterable[LibraryEntry] = (),
        library_filter: LibraryFilter | None = None,
    ) -> tuple[PersonalizedRelease, ...]:
        library_by_anilist_id = {entry.anilist_id: entry for entry in library_entries}
        evaluated = (
            PersonalizedRelease(
                release,
                evaluate_release(
                    release,
                    preferences,
                    library_by_anilist_id.get(release.anime.anilist_id),
                    library_filter,
                ),
            )
            for release in releases
        )
        included = (item for item in evaluated if item.decision.include)
        return tuple(sorted(included, key=self._sort_key))

    @staticmethod
    def _sort_key(item: PersonalizedRelease) -> tuple[int, datetime | date, str]:
        return (-item.decision.score, item.release.released_at, item.release.stable_key)
