from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from icalendar import Calendar, Event

from anime_calendar.formatting.event_formatter import (
    format_event_description,
    format_event_summary,
)
from anime_calendar.models import (
    Release,
    ReleaseEvidence,
    ReleaseLabel,
    ReleaseType,
    StreamingProvider,
)


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
    prefix = "[Estimated] " if release.is_estimated else ""
    return f"{prefix}{format_event_summary(release)}"


def _provider_lines(provider: StreamingProvider) -> list[str]:
    confidence = provider.confidence.value.title()
    lines = [f"{provider.display_name} â€” {confidence}"]
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


def _evidence_lines(evidence: ReleaseEvidence) -> list[str]:
    lines = [f"- {evidence.source_name}"]
    if evidence.source_url:
        lines.append(f"  {evidence.source_url}")
    if evidence.note:
        lines.append(f"  {evidence.note}")
    return lines


def _description(release: Release) -> str:
    return format_event_description(release)


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
            _humanize(release.date_status.value) or "Unknown",
            _humanize(release.variant.value) or "Unknown",
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



