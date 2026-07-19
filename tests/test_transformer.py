from datetime import UTC, date, datetime

from anime_calendar.models import (
    ReleaseConfidence,
    ReleaseDateStatus,
    ReleaseEvidenceType,
    ReleasePrecision,
    ReleaseType,
)
from anime_calendar.services.transformer import (
    merge_releases,
    transform_airing_schedule,
    transform_media_releases,
)


def media_payload(*, media_id: int = 42, media_format: str = "TV") -> dict:
    return {
        "id": media_id,
        "siteUrl": f"https://anilist.co/anime/{media_id}",
        "title": {"romaji": "Romaji Name", "english": "English Name", "native": "日本語名"},
        "description": "A <b>great</b> anime.<br>Second line.",
        "genres": ["Action", "Fantasy"],
        "season": "SUMMER",
        "seasonYear": 2026,
        "format": media_format,
        "status": "RELEASING",
        "source": "LIGHT_NOVEL",
        "episodes": 12,
        "duration": 24,
        "averageScore": 82,
        "coverImage": {"extraLarge": "https://example.com/poster.jpg", "large": None},
        "bannerImage": "https://example.com/banner.jpg",
        "studios": {"nodes": [{"name": "Example Studio", "isAnimationStudio": True}]},
        "trailer": {"site": "youtube", "id": "abc123", "thumbnail": None},
        "externalLinks": [
            {"site": "Official Site", "url": "https://example.com/anime"},
            {
                "site": "Crunchyroll",
                "url": "https://www.crunchyroll.com/series/example",
                "type": "STREAMING",
            },
        ],
    }


def test_transform_airing_schedule_enriches_metadata_and_deduplicates() -> None:
    raw_item = {"airingAt": 1780000000, "episode": 12, "media": media_payload()}
    releases = transform_airing_schedule([raw_item, raw_item])

    assert len(releases) == 1
    release = releases[0]
    assert release.release_type is ReleaseType.EPISODE
    assert release.released_at == datetime.fromtimestamp(1780000000, tz=UTC)
    assert release.anime.synopsis == "A great anime. Second line."
    assert release.anime.studios == ("Example Studio",)
    assert release.anime.streaming_providers[0].provider_id == "crunchyroll"
    assert release.date_status is ReleaseDateStatus.CONFIRMED
    assert release.confidence is ReleaseConfidence.HIGH
    assert release.precision is ReleasePrecision.EXACT_TIME
    assert release.evidence[0].evidence_type is ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE


def test_transform_media_releases_creates_all_day_movie_and_skips_partial_dates() -> None:
    movie = media_payload(media_format="MOVIE") | {
        "startDate": {"year": 2026, "month": 8, "day": 14}
    }
    partial = media_payload(media_id=43, media_format="OVA") | {
        "startDate": {"year": 2026, "month": None, "day": None}
    }

    releases = transform_media_releases([movie, movie, partial])

    assert len(releases) == 1
    assert releases[0].release_type is ReleaseType.MOVIE
    assert releases[0].released_at == datetime(2026, 8, 14, tzinfo=UTC)
    assert releases[0].is_all_day
    assert releases[0].date_status is ReleaseDateStatus.REPORTED
    assert releases[0].confidence is ReleaseConfidence.MEDIUM
    assert releases[0].precision is ReleasePrecision.EXACT_DATE


def test_merge_releases_preserves_distinct_release_types() -> None:
    episode = transform_airing_schedule(
        [{"airingAt": 1780000000, "episode": 1, "media": media_payload()}]
    )[0]
    movie = transform_media_releases(
        [
            media_payload(media_format="MOVIE")
            | {"startDate": {"year": 2026, "month": 8, "day": 14}}
        ]
    )[0]

    assert len(merge_releases([episode], [movie], [movie])) == 2


def test_merge_releases_drops_media_start_duplicate_of_episode_premiere() -> None:
    timestamp = int(datetime(2026, 8, 14, 18, 0, tzinfo=UTC).timestamp())
    episode = transform_airing_schedule(
        [{"airingAt": timestamp, "episode": 1, "media": media_payload(media_format="ONA")}]
    )[0]
    media_release = transform_media_releases(
        [
            media_payload(media_format="ONA")
            | {"startDate": {"year": 2026, "month": 8, "day": 14}}
        ]
    )[0]

    merged = merge_releases([episode], [media_release])

    assert merged == [episode]
