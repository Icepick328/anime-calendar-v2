from datetime import UTC, date, datetime

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
        native_title="日本語名",
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
        external_links=(ExternalLink(site="Official Site", url="https://example.com/anime"),),
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
    calendar = build_calendar([release], calendar_name="Anime Releases", event_duration_minutes=30)
    parsed = Calendar.from_ical(calendar.to_ical())
    event = next(component for component in parsed.walk() if component.name == "VEVENT")

    assert "Episode 7" in str(event.get("summary"))
    assert "anilist-42-ep-7" in str(event.get("uid"))
    assert "Summer 2026" in str(event.get("description"))
    assert "Crunchyroll" in str(event.get("description"))
    assert event.get("url") == "https://www.crunchyroll.com/series/example"
    assert isinstance(event.decoded("dtstart"), datetime)


def test_build_calendar_creates_all_day_movie_release() -> None:
    release = Release(
        anime=make_anime(media_format="MOVIE", total_episodes=1),
        release_type=ReleaseType.MOVIE,
        released_at=date(2026, 8, 14),
    )
    calendar = build_calendar([release], calendar_name="Anime Movies", event_duration_minutes=30)
    parsed = Calendar.from_ical(calendar.to_ical())
    event = next(component for component in parsed.walk() if component.name == "VEVENT")

    assert "Movie Release" in str(event.get("summary"))
    assert event.decoded("dtstart") == date(2026, 8, 14)
    assert event.decoded("dtend") == date(2026, 8, 15)
    assert "Release type: Movie" in str(event.get("description"))
