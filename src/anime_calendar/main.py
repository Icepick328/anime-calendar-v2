from __future__ import annotations

import logging
from pathlib import Path

from anime_calendar.calendars.ics_builder import build_calendar, write_calendar
from anime_calendar.config import load_settings
from anime_calendar.logging_config import configure_logging
from anime_calendar.models import Release, ReleaseType
from anime_calendar.providers.anilist import (
    AniListError,
    fetch_airing_schedule,
    fetch_media_releases,
)
from anime_calendar.services.transformer import (
    merge_releases,
    transform_airing_schedule,
    transform_media_releases,
)

LOGGER = logging.getLogger(__name__)


def _write_feed(
    releases: list[Release],
    *,
    name: str,
    filename: str,
    output_directory: Path,
    duration: int,
) -> Path:
    calendar = build_calendar(
        releases,
        calendar_name=name,
        event_duration_minutes=duration,
    )
    return write_calendar(calendar, output_directory / filename)


def main() -> int:
    configure_logging()

    try:
        settings = load_settings()
        LOGGER.info("Fetching episode schedules from AniList")
        episode_releases = transform_airing_schedule(fetch_airing_schedule(settings))

        LOGGER.info("Fetching movie and special releases from AniList")
        media_releases = transform_media_releases(fetch_media_releases(settings))
        all_releases = merge_releases(episode_releases, media_releases)

        movies = [item for item in all_releases if item.release_type is ReleaseType.MOVIE]
        specials = [
            item
            for item in all_releases
            if item.release_type
            in {
                ReleaseType.OVA,
                ReleaseType.ONA,
                ReleaseType.SPECIAL,
                ReleaseType.TV_SHORT,
                ReleaseType.MUSIC,
                ReleaseType.OTHER,
            }
        ]

        output_directory = Path(settings.output_directory)
        feeds = (
            (all_releases, settings.calendar_name, "anime_calendar.ics"),
            (all_releases, settings.calendar_name, "all_releases.ics"),
            (episode_releases, "Anime Episodes", "episodes.ics"),
            (movies, "Anime Movies", "movies.ics"),
            (specials, "Anime OVAs, ONAs & Specials", "specials.ics"),
        )
        for releases, name, filename in feeds:
            path = _write_feed(
                releases,
                name=name,
                filename=filename,
                output_directory=output_directory,
                duration=settings.event_duration_minutes,
            )
            LOGGER.info("Generated %s events in %s", len(releases), path.resolve())
    except (AniListError, OSError, TypeError, ValueError) as exc:
        LOGGER.error("Calendar generation failed: %s", exc)
        return 1

    return 0
