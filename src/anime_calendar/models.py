from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Anime:
    anilist_id: int
    title: str
    romaji_title: str
    genres: tuple[str, ...]
    site_url: str
    cover_image_url: str | None


@dataclass(frozen=True, slots=True)
class EpisodeRelease:
    anime: Anime
    episode_number: int
    airing_at: datetime
