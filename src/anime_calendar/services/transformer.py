from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from anime_calendar.models import Anime, EpisodeRelease


def transform_airing_schedule(raw_items: Iterable[dict[str, Any]]) -> list[EpisodeRelease]:
    releases: list[EpisodeRelease] = []
    seen: set[tuple[int, int, int]] = set()

    for item in raw_items:
        media = item.get("media") or {}
        title_data = media.get("title") or {}
        romaji_title = title_data.get("romaji") or "Untitled Anime"
        display_title = title_data.get("english") or romaji_title
        cover = media.get("coverImage") or {}

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
            genres=tuple(media.get("genres") or ()),
            site_url=media.get("siteUrl") or f"https://anilist.co/anime/{anime_id}",
            cover_image_url=cover.get("extraLarge") or cover.get("large"),
        )
        releases.append(
            EpisodeRelease(
                anime=anime,
                episode_number=episode_number,
                airing_at=datetime.fromtimestamp(airing_timestamp, tz=UTC),
            )
        )

    return sorted(releases, key=lambda release: release.airing_at)
