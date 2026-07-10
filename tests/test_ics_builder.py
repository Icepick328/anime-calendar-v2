from datetime import UTC, datetime

from anime_calendar.calendars.ics_builder import build_calendar
from anime_calendar.models import Anime, EpisodeRelease


def test_build_calendar_contains_event_metadata() -> None:
    anime = Anime(
        anilist_id=42,
        title="Example Anime",
        romaji_title="Example Anime",
        genres=("Action", "Fantasy"),
        site_url="https://anilist.co/anime/42",
        cover_image_url="https://example.com/poster.jpg",
    )
    release = EpisodeRelease(
        anime=anime,
        episode_number=7,
        airing_at=datetime(2026, 7, 9, 18, 0, tzinfo=UTC),
    )

    calendar = build_calendar(
        [release],
        calendar_name="Anime Releases",
        event_duration_minutes=30,
    )
    text = calendar.to_ical().decode("utf-8")

    assert "Example Anime" in text
    assert "Episode 7" in text
    assert "anilist-42-ep-7" in text
    assert "https://example.com/poster.jpg" in text
