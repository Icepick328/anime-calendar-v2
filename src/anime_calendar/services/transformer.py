from __future__ import annotations

import html
import re
from collections.abc import Iterable
from datetime import UTC, date, datetime
from typing import Any

from anime_calendar.models import (
    Anime,
    ExternalLink,
    Release,
    ReleaseEvidence,
    ReleaseEvidenceType,
    ReleasePrecision,
    ReleaseType,
    ReleaseVariant,
    Trailer,
)
from anime_calendar.release_intelligence.confidence import assess_release_evidence
from anime_calendar.services.streaming_resolver import resolve_streaming_providers

_WHITESPACE = re.compile(r"\s+")
_FORMAT_TO_RELEASE_TYPE = {
    "MOVIE": ReleaseType.MOVIE,
    "OVA": ReleaseType.OVA,
    "ONA": ReleaseType.ONA,
    "SPECIAL": ReleaseType.SPECIAL,
    "TV_SHORT": ReleaseType.TV_SHORT,
    "MUSIC": ReleaseType.MUSIC,
}


def _clean_text(value: str | None) -> str | None:
    if not value:
        return None

    cleaned = html.unescape(value).replace("<br>", "\n").replace("<br />", "\n")
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = _WHITESPACE.sub(" ", cleaned).strip()
    return cleaned or None


def _transform_external_links(
    raw_links: list[dict[str, Any]] | None,
) -> tuple[ExternalLink, ...]:
    links: list[ExternalLink] = []

    for raw in raw_links or []:
        site = raw.get("site")
        url = raw.get("url")

        if site and url:
            links.append(
                ExternalLink(
                    site=str(site),
                    url=str(url),
                    link_type=raw.get("type"),
                    language=raw.get("language"),
                )
            )

    return tuple(links)


def _transform_trailer(raw: dict[str, Any] | None) -> Trailer | None:
    if not raw or not raw.get("site") or not raw.get("id"):
        return None

    return Trailer(
        site=str(raw["site"]),
        trailer_id=str(raw["id"]),
        thumbnail_url=raw.get("thumbnail"),
    )


def _transform_anime(media: dict[str, Any]) -> Anime:
    title_data = media.get("title") or {}
    romaji_title = title_data.get("romaji") or "Untitled Anime"
    cover = media.get("coverImage") or {}
    studio_nodes = (media.get("studios") or {}).get("nodes") or []
    anime_id = int(media["id"])

    external_links = _transform_external_links(media.get("externalLinks"))

    return Anime(
        anilist_id=anime_id,
        title=title_data.get("english") or romaji_title,
        romaji_title=romaji_title,
        native_title=title_data.get("native"),
        synopsis=_clean_text(media.get("description")),
        genres=tuple(media.get("genres") or ()),
        studios=tuple(
            str(studio["name"])
            for studio in studio_nodes
            if studio.get("name") and studio.get("isAnimationStudio", True)
        ),
        season=media.get("season"),
        season_year=media.get("seasonYear"),
        media_format=media.get("format"),
        status=media.get("status"),
        source=media.get("source"),
        total_episodes=media.get("episodes"),
        duration_minutes=media.get("duration"),
        average_score=media.get("averageScore"),
        site_url=media.get("siteUrl") or f"https://anilist.co/anime/{anime_id}",
        cover_image_url=cover.get("extraLarge") or cover.get("large"),
        banner_image_url=media.get("bannerImage"),
        trailer=_transform_trailer(media.get("trailer")),
        external_links=external_links,
        streaming_providers=resolve_streaming_providers(anime_id, external_links),
    )


def transform_airing_schedule(
    raw_items: Iterable[dict[str, Any]],
) -> list[Release]:
    releases: list[Release] = []
    seen: set[tuple[int, int, int]] = set()

    for item in raw_items:
        media = item.get("media") or {}
        anime_id = int(media["id"])
        episode_number = int(item["episode"])
        airing_timestamp = int(item["airingAt"])

        dedupe_key = (anime_id, episode_number, airing_timestamp)
        if dedupe_key in seen:
            continue

        seen.add(dedupe_key)
        anime = _transform_anime(media)

        evidence = (
            ReleaseEvidence(
                evidence_type=ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
                source_name="AniList airing schedule",
                source_url=anime.site_url,
                note="Precise upstream airing timestamp.",
            ),
        )

        assessment = assess_release_evidence(
            evidence=evidence,
            precision=ReleasePrecision.EXACT_TIME,
        )

        releases.append(
            Release(
                anime=anime,
                release_type=ReleaseType.EPISODE,
                episode_number=episode_number,
                released_at=datetime.fromtimestamp(airing_timestamp, tz=UTC),
                date_status=assessment.date_status,
                confidence=assessment.confidence,
                precision=assessment.precision,
                variant=ReleaseVariant.ORIGINAL,
                evidence=evidence,
            )
        )

    return sorted(releases, key=lambda release: release.released_at)


def transform_media_releases(
    raw_items: Iterable[dict[str, Any]],
) -> list[Release]:
    releases: list[Release] = []
    seen: set[tuple[int, ReleaseType, date]] = set()

    for media in raw_items:
        start = media.get("startDate") or {}
        year = start.get("year")
        month = start.get("month")
        day = start.get("day")

        if not all((year, month, day)):
            continue

        media_format = media.get("format")
        release_type = _FORMAT_TO_RELEASE_TYPE.get(
            media_format,
            ReleaseType.OTHER,
        )
        release_date = date(int(year), int(month), int(day))
        release_datetime = datetime.combine(
            release_date,
            datetime.min.time(),
            tzinfo=UTC,
        )
        anime_id = int(media["id"])

        dedupe_key = (anime_id, release_type, release_date)
        if dedupe_key in seen:
            continue

        seen.add(dedupe_key)
        anime = _transform_anime(media)

        evidence = (
            ReleaseEvidence(
                evidence_type=ReleaseEvidenceType.ANILIST_MEDIA_START_DATE,
                source_name="AniList media start date",
                source_url=anime.site_url,
                note=(
                    "Date-only upstream metadata; region and theatrical/"
                    "streaming context may be unspecified."
                ),
            ),
        )

        assessment = assess_release_evidence(
            evidence=evidence,
            precision=ReleasePrecision.EXACT_DATE,
        )

        releases.append(
            Release(
                anime=anime,
                release_type=release_type,
                released_at=release_datetime,
                date_status=assessment.date_status,
                confidence=assessment.confidence,
                precision=assessment.precision,
                variant=ReleaseVariant.ORIGINAL,
                evidence=evidence,
            )
        )

    return sorted(releases, key=lambda release: release.released_at)


def _sort_value(release: Release) -> datetime:
    if isinstance(release.released_at, datetime):
        if (
            release.released_at.tzinfo is None
            or release.released_at.utcoffset() is None
        ):
            return release.released_at.replace(tzinfo=UTC)

        return release.released_at

    return datetime.combine(
        release.released_at,
        datetime.min.time(),
        tzinfo=UTC,
    )


def merge_releases(
    *release_groups: Iterable[Release],
) -> list[Release]:
    candidates = [
        release
        for group in release_groups
        for release in group
    ]

    episode_dates = {
        (release.anime.anilist_id, release.released_at.date())
        for release in candidates
        if release.release_type is ReleaseType.EPISODE
        and isinstance(release.released_at, datetime)
    }

    merged: dict[str, Release] = {}

    for release in candidates:
        release_date = (
            release.released_at.date()
            if isinstance(release.released_at, datetime)
            else release.released_at
        )

        if (
            release.release_type is not ReleaseType.EPISODE
            and (release.anime.anilist_id, release_date) in episode_dates
        ):
            continue

        existing = merged.get(release.stable_key)

        if existing is None or release.confidence.rank > existing.confidence.rank:
            merged[release.stable_key] = release

    return sorted(merged.values(), key=_sort_value)
