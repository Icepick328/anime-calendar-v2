from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from icalendar import Calendar, Event

from anime_calendar.models import EpisodeRelease


def build_calendar(
    releases: list[EpisodeRelease],
    *,
    calendar_name: str,
    event_duration_minutes: int,
) -> Calendar:
    calendar = Calendar()
    calendar.add("prodid", "-//Icepick328//Anime Calendar v2//EN")
    calendar.add("version", "2.0")
    calendar.add("calscale", "GREGORIAN")
    calendar.add("method", "PUBLISH")
    calendar.add("x-wr-calname", calendar_name)

    for release in releases:
        event = Event()
        uid = (
            f"anilist-{release.anime.anilist_id}-ep-{release.episode_number}"
            "@anime-calendar-v2"
        )
        event.add("uid", uid)
        event.add("summary", f"{release.anime.title} — Episode {release.episode_number}")
        event.add("dtstart", release.airing_at)
        event.add("dtend", release.airing_at + timedelta(minutes=event_duration_minutes))
        event.add("url", release.anime.site_url)

        description_lines = [
            f"Episode {release.episode_number}",
            f"AniList: {release.anime.site_url}",
        ]
        if release.anime.genres:
            description_lines.append(f"Genres: {', '.join(release.anime.genres)}")
        if release.anime.cover_image_url:
            description_lines.append(f"Poster: {release.anime.cover_image_url}")

        event.add("description", "\n".join(description_lines))
        calendar.add_component(event)

    return calendar


def write_calendar(calendar: Calendar, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(calendar.to_ical())
    return path
