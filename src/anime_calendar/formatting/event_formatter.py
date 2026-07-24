from __future__ import annotations

from datetime import datetime
from typing import Any

from anime_calendar.models import Release, ReleaseType, ReleaseVariant


def format_event_summary(release: Release) -> str:
    """Return a compact calendar event title for a release."""
    title = release.anime.title

    if release.release_type is ReleaseType.MOVIE:
        return f"{title} • Movie Release"

    if release.release_type is ReleaseType.OVA:
        return f"{title} • OVA Release"

    if release.release_type is ReleaseType.ONA:
        return f"{title} • ONA Release"

    if release.release_type is ReleaseType.SPECIAL:
        return f"{title} • Special Release"

    if release.release_type is ReleaseType.MUSIC:
        return f"{title} • Music Release"

    if release.release_type is ReleaseType.TV_SHORT:
        return f"{title} • TV Short Release"

    episode_number = release.episode_number

    if episode_number == 1:
        return f"{title} • Premiere (Ep 1)"

    total_episodes = release.anime.total_episodes
    if (
        episode_number is not None
        and total_episodes is not None
        and episode_number == total_episodes
    ):
        return f"{title} • Finale (Ep {episode_number})"

    if episode_number is not None:
        return f"{title} • Ep {episode_number}"

    return title


def format_event_description(release: Release) -> str:
    """Return a readable, metadata-rich calendar event description."""
    sections: list[str] = []

    badge = _release_badge(release)
    if badge is not None:
        sections.append(badge)

    if release.release_type is ReleaseType.EPISODE:
        episode_number = release.episode_number
        episode_value = (
            str(episode_number)
            if episode_number is not None
            else "Not confirmed"
        )
        sections.append(_section("EPISODE", episode_value))

    provider = release.anime.preferred_streaming_provider

    if provider is None:
        sections.append(_section("STREAMING", "Provider not confirmed"))
    else:
        sections.append(_section("STREAMING", provider.display_name))

    sections.append(
        _section(
            "RELEASE",
            _format_release_datetime(release.released_at),
        )
    )

    if release.variant is ReleaseVariant.DUB:
        sections.append(_section("VERSION", "English Dub"))
    elif release.variant is ReleaseVariant.SUB:
        sections.append(_section("VERSION", "English Sub"))
    else:
        sections.append(_section("VERSION", "Original Release"))

    genres = _format_genres(release.anime.genres)
    if genres:
        sections.append(_section("GENRES", genres))

    synopsis = _clean_text(release.anime.synopsis)
    if synopsis:
        sections.append(_section("SYNOPSIS", synopsis))

    if provider is not None and provider.url:
        sections.append(_section("WATCH", provider.url))

    site_url = _clean_text(release.anime.site_url)
    if site_url:
        sections.append(_section("ANILIST", site_url))

    poster_url = _clean_text(release.anime.cover_image_url)
    if poster_url:
        sections.append(_section("POSTER", poster_url))

    return "\n\n".join(sections)


def _release_badge(release: Release) -> str | None:
    if release.release_type is ReleaseType.MOVIE:
        return "🎬 MOVIE RELEASE"

    if release.release_type is ReleaseType.OVA:
        return "💿 OVA RELEASE"

    if release.release_type is ReleaseType.ONA:
        return "🌐 ONA RELEASE"

    if release.release_type is ReleaseType.SPECIAL:
        return "✨ SPECIAL RELEASE"

    if release.release_type is ReleaseType.MUSIC:
        return "🎵 MUSIC RELEASE"

    if release.release_type is ReleaseType.TV_SHORT:
        return "📺 TV SHORT RELEASE"

    if release.release_type is ReleaseType.EPISODE:
        if release.episode_number == 1:
            return "🌟 SEASON PREMIERE"

        total_episodes = release.anime.total_episodes
        if (
            release.episode_number is not None
            and total_episodes is not None
            and release.episode_number == total_episodes
        ):
            return "🏁 SEASON FINALE"

    return None


def _format_release_datetime(value: datetime) -> str:
    return value.strftime("%A, %B %d, %Y\n%I:%M %p %Z").replace(
        " 0",
        " ",
    )


def _format_genres(genres: Any) -> str:
    if not genres:
        return ""

    return " • ".join(str(genre) for genre in genres)


def _clean_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _section(title: str, content: str) -> str:
    return f"{title}\n{content}"
