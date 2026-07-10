from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from icalendar import Calendar, Event

from anime_calendar.models import Release, ReleaseLabel, ReleaseType, StreamingProvider


def _humanize(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("_", " ").title()


def _release_name(release: Release) -> str:
    if release.release_type is ReleaseType.EPISODE:
        if release.label is ReleaseLabel.PREMIERE:
            return "Season Premiere"
        if release.label is ReleaseLabel.FINALE:
            return "Season Finale"
        return f"Episode {release.episode_number}"
    return f"{_humanize(release.release_type.value)} Release"


def _summary(release: Release) -> str:
    return f"{release.anime.title} — {_release_name(release)}"


def _provider_lines(provider: StreamingProvider) -> list[str]:
    confidence = provider.confidence.value.title()
    lines = [f"{provider.display_name} — {confidence}"]
    if provider.url:
        lines.append(provider.url)
    if provider.regions:
        lines.append(f"Regions: {', '.join(provider.regions)}")
    if provider.language_summary:
        lines.append(provider.language_summary)
    if provider.simulcast is not None:
        lines.append(f"Simulcast: {'Yes' if provider.simulcast else 'No'}")
    lines.append(f"Evidence: {_humanize(provider.evidence.value)}")
    return lines


def _description(release: Release) -> str:
    anime = release.anime
    lines = [
        f"Release type: {_humanize(release.release_type.value)}",
        f"Release: {_release_name(release)}",
    ]
    if release.episode_number is not None:
        lines.insert(0, f"Episode: {release.episode_number}")
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
        unit = "movie" if release.release_type is ReleaseType.MOVIE else "episode"
        lines.append(f"Typical {unit} duration: {anime.duration_minutes} minutes")
    if anime.average_score:
        lines.append(f"AniList score: {anime.average_score}/100")
    if anime.genres:
        lines.append(f"Genres: {', '.join(anime.genres)}")
    if anime.studios:
        lines.append(f"Studios: {', '.join(anime.studios)}")

    if anime.streaming_providers:
        lines.extend(["", "Streaming"])
        for index, provider in enumerate(anime.streaming_providers):
            if index:
                lines.append("")
            lines.extend(_provider_lines(provider))
    else:
        lines.extend(["", "Streaming", "No confirmed streaming provider found."])

    if anime.synopsis:
        lines.extend(["", "Synopsis", anime.synopsis])

    lines.extend(["", "Links", f"AniList: {anime.site_url}"])
    if anime.cover_image_url:
        lines.append(f"Poster: {anime.cover_image_url}")
    if anime.banner_image_url:
        lines.append(f"Banner: {anime.banner_image_url}")
    if anime.trailer and anime.trailer.url:
        lines.append(f"Trailer: {anime.trailer.url}")

    provider_urls = {provider.url for provider in anime.streaming_providers if provider.url}
    for link in anime.external_links:
        if link.url not in provider_urls:
            lines.append(f"{link.site}: {link.url}")
    return "\n".join(lines)


def build_calendar(
    releases: list[Release],
    *,
    calendar_name: str,
    event_duration_minutes: int,
) -> Calendar:
    calendar = Calendar()
    calendar.add("prodid", "-//Anime Calendar v2//EN")
    calendar.add("version", "2.0")
    calendar.add("calscale", "GREGORIAN")
    calendar.add("x-wr-calname", calendar_name)

    generated_at = datetime.now().astimezone()
    for release in releases:
        event = Event()
        event.add("uid", f"{release.stable_key}@anime-calendar-v2")
        event.add("summary", _summary(release))
        event.add("dtstamp", generated_at)

        if release.is_all_day:
            assert isinstance(release.released_at, date)
            event.add("dtstart", release.released_at)
            event.add("dtend", release.released_at + timedelta(days=1))
        else:
            assert isinstance(release.released_at, datetime)
            event.add("dtstart", release.released_at)
            event.add("dtend", release.released_at + timedelta(minutes=event_duration_minutes))

        preferred_provider = release.anime.preferred_streaming_provider
        event_url = (
            preferred_provider.url
            if preferred_provider and preferred_provider.url
            else release.anime.site_url
        )
        event.add("url", event_url)
        event.add("description", _description(release))

        categories = [
            "Anime",
            _humanize(release.release_type.value) or "Release",
            _humanize(release.label.value) or "Release",
        ]
        categories.extend(provider.display_name for provider in release.anime.streaming_providers)
        event.add("categories", categories)

        if release.anime.cover_image_url:
            event.add(
                "attach",
                release.anime.cover_image_url,
                parameters={"FMTTYPE": "image/jpeg"},
            )
        calendar.add_component(event)

    return calendar


def write_calendar(calendar: Calendar, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(calendar.to_ical())
    return path
