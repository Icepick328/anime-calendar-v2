from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from icalendar import Calendar, Event

from anime_calendar.models import EpisodeRelease, ReleaseLabel


def _humanize(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("_", " ").title()


def _summary(release: EpisodeRelease) -> str:
    if release.label is ReleaseLabel.PREMIERE:
        marker = "Season Premiere"
    elif release.label is ReleaseLabel.FINALE:
        marker = "Season Finale"
    else:
        marker = f"Episode {release.episode_number}"
    return f"{release.anime.title} — {marker}"


def _description(release: EpisodeRelease) -> str:
    anime = release.anime
    lines = [
        f"Episode: {release.episode_number}",
        f"Release: {_humanize(release.label.value)}",
    ]

    if anime.romaji_title != anime.title:
        lines.append(f"Romaji title: {anime.romaji_title}")
    if anime.native_title:
        lines.append(f"Native title: {anime.native_title}")
    if anime.season_label:
        lines.append(f"Season: {anime.season_label}")
    if anime.media_format:
        lines.append(f"Format: {_humanize(anime.media_format)}")
    if anime.status:
        lines.append(f"Status: {_humanize(anime.status)}")
    if anime.source:
        lines.append(f"Source: {_humanize(anime.source)}")
    if anime.total_episodes:
        lines.append(f"Series episodes: {anime.total_episodes}")
    if anime.duration_minutes:
        lines.append(f"Typical duration: {anime.duration_minutes} minutes")
    if anime.average_score is not None:
        lines.append(f"AniList score: {anime.average_score}/100")
    if anime.genres:
        lines.append(f"Genres: {', '.join(anime.genres)}")
    if anime.studios:
        lines.append(f"Studios: {', '.join(anime.studios)}")

    if anime.synopsis:
        lines.extend(["", "Synopsis", anime.synopsis])

    lines.extend(["", "Links", f"AniList: {anime.site_url}"])
    if anime.cover_image_url:
        lines.append(f"Poster: {anime.cover_image_url}")
    if anime.banner_image_url:
        lines.append(f"Banner: {anime.banner_image_url}")
    if anime.trailer and anime.trailer.url:
        lines.append(f"Trailer: {anime.trailer.url}")

    for link in anime.external_links:
        lines.append(f"{link.site}: {link.url}")

    return "\n".join(lines)


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

    generated_at = datetime.now(UTC)

    for release in releases:
        event = Event()
        uid = (
            f"anilist-{release.anime.anilist_id}-ep-{release.episode_number}"
            "@anime-calendar-v2"
        )
        event.add("uid", uid)
        event.add("summary", _summary(release))
        event.add("dtstamp", generated_at)
        event.add("dtstart", release.airing_at)
        event.add("dtend", release.airing_at + timedelta(minutes=event_duration_minutes))
        event.add("url", release.anime.site_url)
        event.add("description", _description(release))
        event.add("categories", ["Anime", _humanize(release.label.value) or "Episode"])

        if release.anime.cover_image_url:
            event.add("attach", release.anime.cover_image_url, parameters={"FMTTYPE": "image/jpeg"})

        calendar.add_component(event)

    return calendar


def write_calendar(calendar: Calendar, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(calendar.to_ical())
    return path
