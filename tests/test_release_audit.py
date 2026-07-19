from datetime import UTC, datetime, timedelta

from anime_calendar.models import (
    Release,
    ReleaseConfidence,
    ReleaseDateStatus,
    ReleaseEvidence,
    ReleaseEvidenceType,
    ReleasePrecision,
    ReleaseType,
    ReleaseVariant,
)
from anime_calendar.release_intelligence.audit import (
    audit_release,
    format_release_audit,
)
from tests.test_models import make_anime


def test_audit_release_explains_episode_assessment() -> None:
    release = Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=4,
        released_at=datetime.now(UTC) + timedelta(days=1),
        date_status=ReleaseDateStatus.CONFIRMED,
        confidence=ReleaseConfidence.HIGH,
        precision=ReleasePrecision.EXACT_TIME,
        variant=ReleaseVariant.ORIGINAL,
        evidence=(
            ReleaseEvidence(
                evidence_type=ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
                source_name="AniList airing schedule",
                source_url="https://anilist.co/anime/1",
                note="Precise upstream airing timestamp.",
            ),
        ),
    )

    audit = audit_release(release)

    assert audit.title == release.anime.title
    assert audit.episode_number == 4
    assert audit.date_status == "confirmed"
    assert audit.confidence == "high"
    assert audit.precision == "exact_time"
    assert audit.score == 65
    assert audit.evidence_sources == ("AniList airing schedule",)
    assert audit.evidence_types == ("anilist_airing_schedule",)
    assert audit.reasons


def test_format_release_audit_produces_readable_report() -> None:
    release = Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=1,
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

    report = format_release_audit(audit_release(release))

    assert f"{release.anime.title} - Episode 1" in report
    assert "Confidence: high" in report
    assert "Confidence score: 65/100" in report
    assert "Date status: confirmed" in report
    assert "AniList airing schedule" in report
    assert "Reasons:" in report
    assert "Evidence:" in report
