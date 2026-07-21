from dataclasses import replace
from datetime import UTC, datetime

from anime_calendar.formatting.event_formatter import (
    format_event_description,
    format_event_summary,
)
from anime_calendar.models import (
    Release,
    ReleaseDateStatus,
    ReleasePrecision,
    ReleaseType,
    ReleaseVariant,
)
from tests.test_models import make_anime


def make_release(
    *,
    release_type: ReleaseType = ReleaseType.EPISODE,
    episode_number: int | None = 3,
    variant: ReleaseVariant = ReleaseVariant.ORIGINAL,
    anime=None,
) -> Release:
    return Release(
        anime=anime or make_anime(),
        release_type=release_type,
        episode_number=episode_number,
        released_at=datetime(2026, 7, 20, 2, tzinfo=UTC),
        date_status=ReleaseDateStatus.CONFIRMED,
        precision=(
            ReleasePrecision.EXACT_TIME
            if release_type is ReleaseType.EPISODE
            else ReleasePrecision.EXACT_DATE
        ),
        variant=variant,
    )


def test_episode_summary_is_compact() -> None:
    release = make_release()

    assert format_event_summary(release) == (
        f"{release.anime.title} • Ep 3"
    )


def test_premiere_summary_and_badge() -> None:
    release = make_release(episode_number=1)

    assert format_event_summary(release) == (
        f"{release.anime.title} • Premiere (Ep 1)"
    )
    assert "🌟 SEASON PREMIERE" in format_event_description(release)


def test_finale_summary_and_badge() -> None:
    anime = replace(make_anime(), total_episodes=12)
    release = make_release(episode_number=12, anime=anime)

    assert format_event_summary(release) == (
        f"{release.anime.title} • Finale (Ep 12)"
    )
    assert "🏁 SEASON FINALE" in format_event_description(release)


def test_movie_has_release_badge_and_no_episode_section() -> None:
    anime = replace(make_anime(), media_format="MOVIE")
    release = make_release(
        release_type=ReleaseType.MOVIE,
        episode_number=None,
        anime=anime,
    )
    description = format_event_description(release)

    assert format_event_summary(release) == (
        f"{release.anime.title} • Movie Release"
    )
    assert "🎬 MOVIE RELEASE" in description
    assert "\nEPISODE\n" not in description


def test_streaming_provider_and_watch_link_are_included() -> None:
    anime = make_anime()
    description = format_event_description(
        make_release(anime=anime)
    )

    provider = anime.preferred_streaming_provider

    assert provider is not None
    assert provider.display_name in description
    assert provider.url is not None
    assert f"WATCH\n{provider.url}" in description


def test_missing_provider_is_explicit() -> None:
    anime = replace(
        make_anime(),
        streaming_providers=(),
    )
    description = format_event_description(
        make_release(anime=anime)
    )

    assert "STREAMING\nProvider not confirmed" in description


def test_dub_variant_is_visible() -> None:
    release = make_release(variant=ReleaseVariant.DUB)

    assert "VERSION\nEnglish Dub" in format_event_description(release)


def test_metadata_links_and_content_are_included() -> None:
    anime = replace(
        make_anime(),
        synopsis="A test synopsis for the formatter.",
        cover_image_url="https://example.com/poster.jpg",
    )
    description = format_event_description(
        make_release(anime=anime)
    )

    assert f"ANILIST\n{anime.site_url}" in description
    assert "GENRES\n" in description
    assert "SYNOPSIS\nA test synopsis for the formatter." in description
    assert "POSTER\nhttps://example.com/poster.jpg" in description
