from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ReleaseLabel(StrEnum):
    EPISODE = "episode"
    PREMIERE = "premiere"
    FINALE = "finale"


@dataclass(frozen=True, slots=True)
class ExternalLink:
    site: str
    url: str
    link_type: str | None = None
    language: str | None = None


@dataclass(frozen=True, slots=True)
class Trailer:
    site: str
    trailer_id: str
    thumbnail_url: str | None = None

    @property
    def url(self) -> str | None:
        normalized_site = self.site.casefold()
        if normalized_site == "youtube":
            return f"https://www.youtube.com/watch?v={self.trailer_id}"
        if normalized_site == "dailymotion":
            return f"https://www.dailymotion.com/video/{self.trailer_id}"
        return None


@dataclass(frozen=True, slots=True)
class Anime:
    anilist_id: int
    title: str
    romaji_title: str
    native_title: str | None
    synopsis: str | None
    genres: tuple[str, ...]
    studios: tuple[str, ...]
    season: str | None
    season_year: int | None
    media_format: str | None
    status: str | None
    source: str | None
    total_episodes: int | None
    duration_minutes: int | None
    average_score: int | None
    site_url: str
    cover_image_url: str | None
    banner_image_url: str | None
    trailer: Trailer | None
    external_links: tuple[ExternalLink, ...]

    @property
    def season_label(self) -> str | None:
        if self.season and self.season_year:
            return f"{self.season.title()} {self.season_year}"
        if self.season_year:
            return str(self.season_year)
        return None


@dataclass(frozen=True, slots=True)
class EpisodeRelease:
    anime: Anime
    episode_number: int
    airing_at: datetime

    @property
    def label(self) -> ReleaseLabel:
        if self.episode_number == 1:
            return ReleaseLabel.PREMIERE
        if self.anime.total_episodes and self.episode_number == self.anime.total_episodes:
            return ReleaseLabel.FINALE
        return ReleaseLabel.EPISODE
