from datetime import UTC, date, datetime, timedelta

from icalendar import Calendar

from anime_calendar.calendars.ics_builder import build_calendar
from anime_calendar.models import (
    Anime,
    ExternalLink,
    ProviderConfidence,
    ProviderEvidence,
    Release,
    ReleaseType,
    StreamingProvider,
    Trailer,
)


def make_anime(*, media_format: str = "TV", total_episodes: int | None = 12) -> Anime:
    return Anime(
        anilist_id=42,
        title="Example Anime",
        romaji_title="Example Anime Romaji",
        native_title="\u65e5\u672c\u8a9e",
        synopsis="An example synopsis.",
        genres=("Action", "Fantasy"),
        studios=("Example Studio",),
        season="SUMMER",
        season_year=2026,
        media_format=media_format,
        status="RELEASING",
        source="LIGHT_NOVEL",
        total_episodes=total_episodes,
        duration_minutes=24,
        average_score=82,
        site_url="https://anilist.co/anime/42",
        cover_image_url="https://example.com/poster.jpg",
        banner_image_url="https://example.com/banner.jpg",
        trailer=Trailer(site="youtube", trailer_id="abc123"),
        external_links=(
            ExternalLink(
                site="Official Site",
                url="https://example.com/anime",
            ),
        ),
        streaming_providers=(
            StreamingProvider(
                provider_id="crunchyroll",
                display_name="Crunchyroll",
                url="https://www.crunchyroll.com/series/example",
                confidence=ProviderConfidence.VERIFIED,
                evidence=ProviderEvidence.OFFICIAL_STREAMING_LINK,
                dub_languages=("English",),
            ),
        ),
    )


def test_build_calendar_contains_timed_episode_metadata() -> None:
    release = Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=7,
        released_at=datetime(2026, 7, 9, 18, 0, tzinfo=UTC),
    )

    calendar = build_calendar(
        [release],
        calendar_name="Anime Releases",
        event_duration_minutes=30,
    )

    parsed = Calendar.from_ical(calendar.to_ical())
    event = next(
        component
        for component in parsed.walk()
        if component.name == "VEVENT"
    )

    summary = str(event.get("summary"))
    description = str(event.get("description"))

    assert summary == f"{release.anime.title} \u2022 Ep 7"
    assert "anilist-42-ep-7" in str(event.get("uid"))

    assert "EPISODE\n7" in description
    assert "STREAMING\nCrunchyroll" in description
    assert "RELEASE\nThursday, July 9, 2026" in description
    assert "06:00 PM UTC" in description
    assert "VERSION\nOriginal Release" in description
    assert "GENRES\nAction \u2022 Fantasy" in description
    assert "SYNOPSIS\nAn example synopsis." in description
    assert "WATCH\nhttps://www.crunchyroll.com/series/example" in description
    assert "ANILIST\nhttps://anilist.co/anime/42" in description
    assert "POSTER\nhttps://example.com/poster.jpg" in description

    assert event.get("url") == "https://www.crunchyroll.com/series/example"
    assert isinstance(event.decoded("dtstart"), datetime)
    assert isinstance(event.decoded("dtend"), datetime)

    assert event.decoded("dtend") - event.decoded("dtstart") == timedelta(
        minutes=30
    )


def test_build_calendar_creates_all_day_movie_release() -> None:
    release = Release(
        anime=make_anime(media_format="MOVIE", total_episodes=1),
        release_type=ReleaseType.MOVIE,
        released_at=date(2026, 8, 14),
    )

    calendar = build_calendar(
        [release],
        calendar_name="Anime Movies",
        event_duration_minutes=30,
    )

    parsed = Calendar.from_ical(calendar.to_ical())
    event = next(
        component
        for component in parsed.walk()
        if component.name == "VEVENT"
    )

    summary = str(event.get("summary"))
    description = str(event.get("description"))

    assert summary == "Example Anime \u2022 Movie Release"
    assert "\U0001F3AC MOVIE RELEASE" in description
    assert "STREAMING\nCrunchyroll" in description
    assert "RELEASE\nFriday, August 14, 2026" in description
    assert "VERSION\nOriginal Release" in description
    assert "GENRES\nAction \u2022 Fantasy" in description
    assert "SYNOPSIS\nAn example synopsis." in description
    assert "WATCH\nhttps://www.crunchyroll.com/series/example" in description
    assert "ANILIST\nhttps://anilist.co/anime/42" in description
    assert "POSTER\nhttps://example.com/poster.jpg" in description

    assert event.decoded("dtstart") == date(2026, 8, 14)
    assert event.decoded("dtend") == date(2026, 8, 15)