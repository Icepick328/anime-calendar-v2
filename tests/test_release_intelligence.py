from datetime import UTC, date, datetime, timedelta

from anime_calendar.models import (
    Release,
    ReleaseConfidence,
    ReleaseDateStatus,
    ReleaseEvidence,
    ReleaseEvidenceType,
    ReleaseLifecycle,
    ReleasePrecision,
    ReleaseType,
    ReleaseVariant,
)
from tests.test_models import make_anime


def test_confirmed_episode_intelligence_helpers() -> None:
    release = Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=3,
        released_at=datetime.now(UTC) + timedelta(days=1),
        date_status=ReleaseDateStatus.CONFIRMED,
        confidence=ReleaseConfidence.HIGH,
        precision=ReleasePrecision.EXACT_TIME,
        variant=ReleaseVariant.ORIGINAL,
        evidence=(
            ReleaseEvidence(
                evidence_type=ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
                source_name="AniList airing schedule",
            ),
        ),
    )

    assert release.has_confirmed_date
    assert not release.is_estimated
    assert release.effective_lifecycle is ReleaseLifecycle.SCHEDULED
    assert release.evidence[0].evidence_type is ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE


def test_estimated_release_is_explicitly_marked() -> None:
    release = Release(
        anime=make_anime(media_format="MOVIE"),
        release_type=ReleaseType.MOVIE,
        released_at=date.today() + timedelta(days=30),
        date_status=ReleaseDateStatus.ESTIMATED,
        confidence=ReleaseConfidence.LOW,
        precision=ReleasePrecision.EXACT_DATE,
        variant=ReleaseVariant.UNKNOWN,
        evidence=(
            ReleaseEvidence(
                evidence_type=ReleaseEvidenceType.HISTORICAL_PATTERN,
                source_name="Historical pattern",
            ),
        ),
    )

    assert release.is_estimated
    assert not release.has_confirmed_date


def test_past_release_reports_released_lifecycle() -> None:
    release = Release(
        anime=make_anime(media_format="OVA"),
        release_type=ReleaseType.OVA,
        released_at=date.today() - timedelta(days=1),
        date_status=ReleaseDateStatus.REPORTED,
        confidence=ReleaseConfidence.MEDIUM,
        precision=ReleasePrecision.EXACT_DATE,
        variant=ReleaseVariant.ORIGINAL,
    )

    assert release.effective_lifecycle is ReleaseLifecycle.RELEASED
