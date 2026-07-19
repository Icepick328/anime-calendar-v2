from datetime import UTC, datetime

from anime_calendar.models import ReleaseType
from anime_calendar.services.transformer import (
    merge_releases,
    transform_media_releases,
)


def _media(
    *,
    anime_id: int = 1001,
    title: str = "Timezone Test Movie",
    media_format: str = "MOVIE",
    year: int = 2026,
    month: int = 8,
    day: int = 15,
) -> dict:
    return {
        "id": anime_id,
        "title": {
            "english": title,
            "romaji": title,
            "native": None,
        },
        "description": None,
        "genres": [],
        "studios": {"nodes": []},
        "season": None,
        "seasonYear": year,
        "format": media_format,
        "status": "NOT_YET_RELEASED",
        "source": "ORIGINAL",
        "episodes": None,
        "duration": None,
        "averageScore": None,
        "siteUrl": f"https://anilist.co/anime/{anime_id}",
        "coverImage": {},
        "bannerImage": None,
        "trailer": None,
        "externalLinks": [],
        "startDate": {
            "year": year,
            "month": month,
            "day": day,
        },
    }


def test_media_release_uses_timezone_aware_utc_datetime() -> None:
    releases = transform_media_releases([_media()])

    assert len(releases) == 1

    released_at = releases[0].released_at
    assert isinstance(released_at, datetime)
    assert released_at == datetime(2026, 8, 15, tzinfo=UTC)
    assert released_at.tzinfo is UTC
    assert released_at.utcoffset() is not None


def test_media_release_preserves_exact_date_precision() -> None:
    release = transform_media_releases([_media()])[0]

    assert release.release_type is ReleaseType.MOVIE
    assert release.precision.value == "exact_date"


def test_media_release_deduplication_still_uses_calendar_date() -> None:
    media = _media()

    releases = transform_media_releases([media, media])

    assert len(releases) == 1


def test_merge_removes_media_release_when_episode_exists_same_day() -> None:
    media_release = transform_media_releases(
        [_media(media_format="SPECIAL")]
    )[0]

    episode_release = media_release.__class__(
        anime=media_release.anime,
        release_type=ReleaseType.EPISODE,
        episode_number=1,
        released_at=datetime(2026, 8, 15, 12, tzinfo=UTC),
        date_status=media_release.date_status,
        confidence=media_release.confidence,
        precision=media_release.precision,
        variant=media_release.variant,
        evidence=media_release.evidence,
    )

    merged = merge_releases(
        [media_release],
        [episode_release],
    )

    assert merged == [episode_release]
