from datetime import UTC, date, datetime

from anime_calendar.models import (
    Anime,
    ExternalLink,
    ProviderConfidence,
    ProviderEvidence,
    Release,
    ReleaseLabel,
    ReleaseType,
    StreamingProvider,
    Trailer,
)


def make_anime(*, total_episodes: int | None = 12, media_format: str = "TV") -> Anime:
    return Anime(
        anilist_id=1,
        title="Example",
        romaji_title="Example",
        native_title=None,
        synopsis=None,
        genres=("Action",),
        studios=("Example Studio",),
        season="WINTER",
        season_year=2026,
        media_format=media_format,
        status="RELEASING",
        source="ORIGINAL",
        total_episodes=total_episodes,
        duration_minutes=24,
        average_score=80,
        site_url="https://anilist.co/anime/1",
        cover_image_url=None,
        banner_image_url=None,
        trailer=Trailer(site="youtube", trailer_id="xyz"),
        external_links=(ExternalLink(site="Official Site", url="https://example.com"),),
        streaming_providers=(
            StreamingProvider(
                provider_id="crunchyroll",
                display_name="Crunchyroll",
                url="https://www.crunchyroll.com/series/example",
                confidence=ProviderConfidence.VERIFIED,
                evidence=ProviderEvidence.OFFICIAL_STREAMING_LINK,
                sub_languages=("English",),
            ),
        ),
    )


def test_anime_season_label_and_trailer_url() -> None:
    anime = make_anime()
    assert anime.season_label == "Winter 2026"
    assert anime.trailer is not None
    assert anime.trailer.url == "https://www.youtube.com/watch?v=xyz"


def test_episode_and_movie_release_behavior() -> None:
    premiere = Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=1,
        released_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
    )
    movie = Release(
        anime=make_anime(total_episodes=1, media_format="MOVIE"),
        release_type=ReleaseType.MOVIE,
        released_at=date(2026, 7, 10),
    )

    assert premiere.label is ReleaseLabel.PREMIERE
    assert not premiere.is_all_day
    assert premiere.stable_key == "anilist-1-ep-1"
    assert movie.label is ReleaseLabel.RELEASE
    assert movie.is_all_day
    assert movie.stable_key == "anilist-1-movie"


def test_streaming_provider_helpers_and_preference() -> None:
    anime = make_anime()
    provider = anime.preferred_streaming_provider

    assert provider is not None
    assert provider.verified
    assert provider.language_summary == "Sub: English"
