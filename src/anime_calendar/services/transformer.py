from __future__ import annotations

import html
import re
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from anime_calendar.models import Anime, EpisodeRelease, ExternalLink, Trailer

_WHITESPACE = re.compile(r"\s+")


def _clean_text(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = html.unescape(value).replace("<br>", "\n").replace("<br />", "\n")
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = _WHITESPACE.sub(" ", cleaned).strip()
    return cleaned or None


def _transform_external_links(raw_links: list[dict[str, Any]] | None) -> tuple[ExternalLink, ...]:
    links: list[ExternalLink] = []
    for raw in raw_links or []:
        site = raw.get("site")
        url = raw.get("url")
        if not site or not url:
            continue
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


def transform_airing_schedule(raw_items: Iterable[dict[str, Any]]) -> list[EpisodeRelease]:
    releases: list[EpisodeRelease] = []
    seen: set[tuple[int, int, int]] = set()

    for item in raw_items:
        media = item.get("media") or {}
        title_data = media.get("title") or {}
        romaji_title = title_data.get("romaji") or "Untitled Anime"
        display_title = title_data.get("english") or romaji_title
        cover = media.get("coverImage") or {}
        studio_nodes = (media.get("studios") or {}).get("nodes") or []

        anime_id = int(media["id"])
        episode_number = int(item["episode"])
        airing_timestamp = int(item["airingAt"])
        dedupe_key = (anime_id, episode_number, airing_timestamp)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        anime = Anime(
            anilist_id=anime_id,
            title=display_title,
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
            external_links=_transform_external_links(media.get("externalLinks")),
        )
        releases.append(
            EpisodeRelease(
                anime=anime,
                episode_number=episode_number,
                airing_at=datetime.fromtimestamp(airing_timestamp, tz=UTC),
            )
        )

    return sorted(releases, key=lambda release: release.airing_at)
