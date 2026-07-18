from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from anime_calendar.models import Release
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


@dataclass(frozen=True, slots=True)
class FilterDecision:
    include: bool
    reasons: tuple[DecisionReason, ...]
    score: int = 0


def evaluate_release(release: Release, preferences: UserPreferences) -> FilterDecision:
    genres = {value.casefold() for value in release.anime.genres}
    studios = {value.casefold() for value in release.anime.studios}
    providers = {provider.provider_id.casefold() for provider in release.anime.streaming_providers}

    excluded_genres = {value.casefold() for value in preferences.excluded_genres}
    if genres & excluded_genres:
        return FilterDecision(False, (DecisionReason.EXCLUDED_GENRE,), -100)

    reasons: list[DecisionReason] = []
    score = 0

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
