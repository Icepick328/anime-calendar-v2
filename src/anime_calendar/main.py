from __future__ import annotations

import logging

from anime_calendar.calendars.ics_builder import build_calendar, write_calendar
from anime_calendar.config import load_settings
from anime_calendar.logging_config import configure_logging
from anime_calendar.providers.anilist import AniListError, fetch_airing_schedule
from anime_calendar.services.transformer import transform_airing_schedule

LOGGER = logging.getLogger(__name__)


def main() -> int:
    configure_logging()

    try:
        settings = load_settings()
        LOGGER.info("Fetching anime releases from AniList")
        raw_schedule = fetch_airing_schedule(settings)
        releases = transform_airing_schedule(raw_schedule)

        calendar = build_calendar(
            releases,
            calendar_name=settings.calendar_name,
            event_duration_minutes=settings.event_duration_minutes,
        )
        output_path = write_calendar(calendar, settings.output_path)
    except (AniListError, OSError, TypeError, ValueError) as exc:
        LOGGER.error("Calendar generation failed: %s", exc)
        return 1

    LOGGER.info("Generated %s events", len(releases))
    LOGGER.info("Calendar written to %s", output_path.resolve())
    return 0
