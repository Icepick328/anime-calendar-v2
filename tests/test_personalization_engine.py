from datetime import UTC, datetime

from anime_calendar.models import (
    Anime,
    ProviderConfidence,
    ProviderEvidence,
    Release,
    ReleaseType,
    ReleaseVariant,
    StreamingProvider,
)
from anime_calendar.personalization import DecisionReason, PersonalizationEngine, UserPreferences


def make_release(
    *,
    anilist_id: int = 1,
    genres: tuple[str, ...] = ("Action",),
    studios: tuple[str, ...] = ("Bones",),
    provider_id: str = "crunchyroll",
    release_type: ReleaseType = ReleaseType.EPISODE,
    variant: ReleaseVariant = ReleaseVariant.SUB,
) -> Release:
    provider = StreamingProvider(
        provider_id=provider_id,
        display_name=provider_id.title(),
        url=f"https://example.com/{provider_id}",
        confidence=ProviderConfidence.HIGH,
        evidence=ProviderEvidence.EXTERNAL_LINK,
    )
    anime = Anime(
        anilist_id=anilist_id,
        title=f"Anime {anilist_id}",
        romaji_title=f"Anime {anilist_id}",
        native_title=None,
        synopsis=None,
        genres=genres,
        studios=studios,
        season="SUMMER",
        season_year=2026,
        media_format="TV",
        status="RELEASING",
        source=None,
        total_episodes=12,
        duration_minutes=24,
        average_score=80,
        site_url=f"https://anilist.co/anime/{anilist_id}",
        cover_image_url=None,
        banner_image_url=None,
        trailer=None,
        external_links=(),
        streaming_providers=(provider,),
    )
    return Release(
        anime=anime,
        release_type=release_type,
        released_at=datetime(2026, 7, 20, 17, 0, tzinfo=UTC),
        episode_number=1 if release_type is ReleaseType.EPISODE else None,
        variant=variant,
    )


def test_excluded_genre_overrides_favorite_anime() -> None:
    release = make_release(anilist_id=10)
    preferences = UserPreferences(
        favorite_anilist_ids=frozenset({10}),
        excluded_genres=frozenset({"action"}),
    )

    result = PersonalizationEngine().evaluate([release], preferences)

    assert result == ()


def test_favorite_anime_receives_highest_priority() -> None:
    favorite = make_release(anilist_id=10)
    genre_match = make_release(anilist_id=20)
    preferences = UserPreferences(
        favorite_anilist_ids=frozenset({10}),
        favorite_genres=frozenset({"Action"}),
    )

    result = PersonalizationEngine().evaluate([genre_match, favorite], preferences)

    assert result[0].release.anime.anilist_id == 10
    assert DecisionReason.FAVORITE_ANIME in result[0].decision.reasons


def test_release_type_filter_excludes_nonmatching_release() -> None:
    movie = make_release(release_type=ReleaseType.MOVIE)
    preferences = UserPreferences(
        preferred_release_types=frozenset({ReleaseType.EPISODE}),
    )

    assert PersonalizationEngine().evaluate([movie], preferences) == ()


def test_variant_filter_includes_matching_dub() -> None:
    dub = make_release(variant=ReleaseVariant.DUB)
    sub = make_release(anilist_id=2, variant=ReleaseVariant.SUB)
    preferences = UserPreferences(
        preferred_variants=frozenset({ReleaseVariant.DUB}),
    )

    result = PersonalizationEngine().evaluate([sub, dub], preferences)

    assert [item.release.variant for item in result] == [ReleaseVariant.DUB]


def test_unmatched_release_can_be_excluded() -> None:
    release = make_release(genres=("Drama",), studios=("Other",), provider_id="netflix")
    preferences = UserPreferences(
        favorite_genres=frozenset({"Action"}),
        include_unmatched_releases=False,
    )

    assert PersonalizationEngine().evaluate([release], preferences) == ()


def test_engine_does_not_mutate_release() -> None:
    release = make_release()
    original_key = release.stable_key

    PersonalizationEngine().evaluate([release], UserPreferences())

    assert release.stable_key == original_key
