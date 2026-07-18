from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from anime_calendar.models import Release
from anime_calendar.personalization.library import LibraryEntry, LibraryFilter, WatchStatus
from anime_calendar.personalization.models import UserPreferences


class DecisionReason(StrEnum):
    FAVORITE_ANIME = "favorite_anime"
    EXCLUDED_GENRE = "excluded_genre"
    GENRE_MATCH = "genre_match"
    PROVIDER_MATCH = "provider_match"
    RELEASE_TYPE_MATCH = "release_type_match"
    STUDIO_MATCH = "studio_match"
    VARIANT_MATCH = "variant_match"
    UNMATCHED_INCLUDED = "unmatched_included"
    UNMATCHED_EXCLUDED = "unmatched_excluded"
    LIBRARY_WATCHING = "library_watching"
    LIBRARY_PLANNED = "library_planned"
    LIBRARY_ON_HOLD = "library_on_hold"
    LIBRARY_COMPLETED = "library_completed"
    LIBRARY_DROPPED = "library_dropped"
    PROGRESS_ALREADY_RELEASED = "progress_already_released"
    LIBRARY_STATUS_EXCLUDED = "library_status_excluded"


@dataclass(frozen=True, slots=True)
class FilterDecision:
    include: bool
    reasons: tuple[DecisionReason, ...]
    score: int = 0


def evaluate_release(
    release: Release,
    preferences: UserPreferences,
    library_entry: LibraryEntry | None = None,
    library_filter: LibraryFilter | None = None,
) -> FilterDecision:
    genres = {value.casefold() for value in release.anime.genres}
    studios = {value.casefold() for value in release.anime.studios}
    providers = {provider.provider_id.casefold() for provider in release.anime.streaming_providers}

    excluded_genres = {value.casefold() for value in preferences.excluded_genres}
    if genres & excluded_genres:
        return FilterDecision(False, (DecisionReason.EXCLUDED_GENRE,), -100)

    reasons: list[DecisionReason] = []
    score = 0

    if library_filter is not None:
        if library_entry is None and not library_filter.include_unlisted_series:
            return FilterDecision(False, (DecisionReason.LIBRARY_STATUS_EXCLUDED,), 0)
        if library_entry is not None:
            if (
                library_filter.included_statuses
                and library_entry.status not in library_filter.included_statuses
            ):
                return FilterDecision(False, (DecisionReason.LIBRARY_STATUS_EXCLUDED,), 0)
            if (
                library_filter.hide_released_progress
                and release.episode_number is not None
                and release.episode_number <= library_entry.progress
            ):
                return FilterDecision(False, (DecisionReason.PROGRESS_ALREADY_RELEASED,), 0)
            library_scores = {
                WatchStatus.WATCHING: (DecisionReason.LIBRARY_WATCHING, 80),
                WatchStatus.PLAN_TO_WATCH: (DecisionReason.LIBRARY_PLANNED, 40),
                WatchStatus.ON_HOLD: (DecisionReason.LIBRARY_ON_HOLD, 15),
                WatchStatus.COMPLETED: (DecisionReason.LIBRARY_COMPLETED, 5),
                WatchStatus.DROPPED: (DecisionReason.LIBRARY_DROPPED, -20),
            }
            reason, adjustment = library_scores[library_entry.status]
            reasons.append(reason)
            score += adjustment

    if release.anime.anilist_id in preferences.favorite_anilist_ids:
        reasons.append(DecisionReason.FAVORITE_ANIME)
        score += 100

    if genres & {value.casefold() for value in preferences.favorite_genres}:
        reasons.append(DecisionReason.GENRE_MATCH)
        score += 20

    if studios & {value.casefold() for value in preferences.favorite_studios}:
        reasons.append(DecisionReason.STUDIO_MATCH)
        score += 20

    if providers & {value.casefold() for value in preferences.preferred_provider_ids}:
        reasons.append(DecisionReason.PROVIDER_MATCH)
        score += 15

    if preferences.preferred_release_types:
        if release.release_type not in preferences.preferred_release_types:
            return FilterDecision(False, (DecisionReason.UNMATCHED_EXCLUDED,), score)
        reasons.append(DecisionReason.RELEASE_TYPE_MATCH)
        score += 10

    if preferences.preferred_variants:
        if release.variant not in preferences.preferred_variants:
            return FilterDecision(False, (DecisionReason.UNMATCHED_EXCLUDED,), score)
        reasons.append(DecisionReason.VARIANT_MATCH)
        score += 10

    if reasons:
        return FilterDecision(True, tuple(reasons), score)

    if preferences.include_unmatched_releases:
        return FilterDecision(True, (DecisionReason.UNMATCHED_INCLUDED,), 0)

    return FilterDecision(False, (DecisionReason.UNMATCHED_EXCLUDED,), 0)
