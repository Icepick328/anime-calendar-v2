from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import StrEnum


class ReleaseType(StrEnum):
    EPISODE = "episode"
    MOVIE = "movie"
    OVA = "ova"
    ONA = "ona"
    SPECIAL = "special"
    TV_SHORT = "tv_short"
    MUSIC = "music"
    OTHER = "other"


class ReleaseLabel(StrEnum):
    EPISODE = "episode"
    PREMIERE = "premiere"
    FINALE = "finale"
    RELEASE = "release"


class ReleaseDateStatus(StrEnum):
    CONFIRMED = "confirmed"
    REPORTED = "reported"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"


class ReleaseConfidence(StrEnum):
    VERIFIED = "verified"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

    @property
    def rank(self) -> int:
        return {
            ReleaseConfidence.UNKNOWN: 0,
            ReleaseConfidence.LOW: 1,
            ReleaseConfidence.MEDIUM: 2,
            ReleaseConfidence.HIGH: 3,
            ReleaseConfidence.VERIFIED: 4,
        }[self]


class ReleaseEvidenceType(StrEnum):
    ANILIST_AIRING_SCHEDULE = "anilist_airing_schedule"
    ANILIST_MEDIA_START_DATE = "anilist_media_start_date"
    OFFICIAL_ANNOUNCEMENT = "official_announcement"
    CURATED_KNOWLEDGE = "curated_knowledge"
    HISTORICAL_PATTERN = "historical_pattern"


class ReleasePrecision(StrEnum):
    EXACT_TIME = "exact_time"
    EXACT_DATE = "exact_date"
    PARTIAL_DATE = "partial_date"
    UNKNOWN = "unknown"


class ReleaseVariant(StrEnum):
    ORIGINAL = "original"
    SUB = "sub"
    DUB = "dub"
    UNKNOWN = "unknown"


class ReleaseLifecycle(StrEnum):
    SCHEDULED = "scheduled"
    RELEASED = "released"
    DELAYED = "delayed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class ProviderConfidence(StrEnum):
    VERIFIED = "verified"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

    @property
    def rank(self) -> int:
        return {
            ProviderConfidence.UNKNOWN: 0,
            ProviderConfidence.LOW: 1,
            ProviderConfidence.MEDIUM: 2,
            ProviderConfidence.HIGH: 3,
            ProviderConfidence.VERIFIED: 4,
        }[self]


class ProviderEvidence(StrEnum):
    OFFICIAL_STREAMING_LINK = "official_streaming_link"
    EXTERNAL_LINK = "external_link"
    CURATED_KNOWLEDGE = "curated_knowledge"


@dataclass(frozen=True, slots=True)
class ReleaseEvidence:
    evidence_type: ReleaseEvidenceType
    source_name: str
    source_url: str | None = None
    note: str | None = None


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
class StreamingProvider:
    provider_id: str
    display_name: str
    url: str | None
    confidence: ProviderConfidence
    evidence: ProviderEvidence
    regions: tuple[str, ...] = ()
    sub_languages: tuple[str, ...] = ()
    dub_languages: tuple[str, ...] = ()
    simulcast: bool | None = None

    @property
    def verified(self) -> bool:
        return self.confidence is ProviderConfidence.VERIFIED

    @property
    def language_summary(self) -> str | None:
        parts: list[str] = []
        if self.sub_languages:
            parts.append(f"Sub: {', '.join(self.sub_languages)}")
        if self.dub_languages:
            parts.append(f"Dub: {', '.join(self.dub_languages)}")
        return " | ".join(parts) or None


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
    streaming_providers: tuple[StreamingProvider, ...] = ()

    @property
    def season_label(self) -> str | None:
        if self.season and self.season_year:
            return f"{self.season.title()} {self.season_year}"
        if self.season_year:
            return str(self.season_year)
        return None

    @property
    def preferred_streaming_provider(self) -> StreamingProvider | None:
        if not self.streaming_providers:
            return None
        return self.streaming_providers[0]


@dataclass(frozen=True, slots=True)
class Release:
    anime: Anime
    release_type: ReleaseType
    released_at: datetime | date
    episode_number: int | None = None
    date_status: ReleaseDateStatus = ReleaseDateStatus.UNKNOWN
    confidence: ReleaseConfidence = ReleaseConfidence.UNKNOWN
    precision: ReleasePrecision = ReleasePrecision.UNKNOWN
    variant: ReleaseVariant = ReleaseVariant.UNKNOWN
    lifecycle: ReleaseLifecycle = ReleaseLifecycle.SCHEDULED
    evidence: tuple[ReleaseEvidence, ...] = ()

    @property
    def label(self) -> ReleaseLabel:
        if self.release_type is not ReleaseType.EPISODE:
            return ReleaseLabel.RELEASE
        if self.episode_number == 1:
            return ReleaseLabel.PREMIERE
        if (
            self.episode_number is not None
            and self.anime.total_episodes
            and self.episode_number == self.anime.total_episodes
        ):
            return ReleaseLabel.FINALE
        return ReleaseLabel.EPISODE

    @property
    def is_all_day(self) -> bool:
        return (
            self.precision is ReleasePrecision.EXACT_DATE
            or (
                isinstance(self.released_at, date)
                and not isinstance(self.released_at, datetime)
            )
        )

    @property
    def stable_key(self) -> str:
        if self.release_type is ReleaseType.EPISODE:
            return f"anilist-{self.anime.anilist_id}-ep-{self.episode_number}"
        return f"anilist-{self.anime.anilist_id}-{self.release_type.value}"

    @property
    def is_estimated(self) -> bool:
        return self.date_status is ReleaseDateStatus.ESTIMATED

    @property
    def has_confirmed_date(self) -> bool:
        return self.date_status is ReleaseDateStatus.CONFIRMED

    @property
    def effective_lifecycle(self) -> ReleaseLifecycle:
        if self.lifecycle in {ReleaseLifecycle.DELAYED, ReleaseLifecycle.CANCELLED}:
            return self.lifecycle
        now = datetime.now(UTC)
        if isinstance(self.released_at, datetime):
            comparison = self.released_at.astimezone(UTC)
            return ReleaseLifecycle.RELEASED if comparison <= now else ReleaseLifecycle.SCHEDULED
        return (
            ReleaseLifecycle.RELEASED
            if self.released_at < now.date()
            else ReleaseLifecycle.SCHEDULED
        )
