from datetime import UTC, datetime

from icalendar import Calendar

from anime_calendar.calendars.ics_builder import build_calendar
from anime_calendar.models import Anime, EpisodeRelease, ExternalLink, ReleaseLabel, Trailer


def make_anime(*, total_episodes: int = 12) -> Anime:
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
        media_format="TV",
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
            ExternalLink(site="Official Site", url="https://example.com/anime"),
        ),
    )


def test_build_calendar_contains_rich_event_metadata() -> None:
    release = EpisodeRelease(
        anime=make_anime(),
        episode_number=7,
        airing_at=datetime(2026, 7, 9, 18, 0, tzinfo=UTC),
    )

    calendar = build_calendar(
        [release],
        calendar_name="Anime Releases",
        event_duration_minutes=30,
    )
    text = calendar.to_ical().decode("utf-8")
    parsed = Calendar.from_ical(calendar.to_ical())
    event = next(component for component in parsed.walk() if component.name == "VEVENT")
    description = str(event.get("description"))

    assert "Example Anime" in text
    assert "Episode 7" in text
    assert "anilist-42-ep-7" in text
    assert "Summer 2026" in description
    assert "Example Studio" in description
    assert "An example synopsis" in description
    assert "https://example.com/poster.jpg" in description
    assert "https://www.youtube.com/watch?v=abc123" in description


def test_release_labels_identify_premiere_and_finale() -> None:
    premiere = EpisodeRelease(
        anime=make_anime(),
        episode_number=1,
        airing_at=datetime(2026, 7, 9, 18, 0, tzinfo=UTC),
    )
    finale = EpisodeRelease(
        anime=make_anime(),
        episode_number=12,
        airing_at=datetime(2026, 9, 24, 18, 0, tzinfo=UTC),
    )

    assert premiere.label is ReleaseLabel.PREMIERE
    assert finale.label is ReleaseLabel.FINALE

    text = build_calendar(
        [premiere, finale],
        calendar_name="Anime Releases",
        event_duration_minutes=30,
    ).to_ical().decode("utf-8")

    assert "Season Premiere" in text
    assert "Season Finale" in text
