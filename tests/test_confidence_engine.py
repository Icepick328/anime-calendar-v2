from anime_calendar.models import (
    ReleaseConfidence,
    ReleaseDateStatus,
    ReleaseEvidence,
    ReleaseEvidenceType,
    ReleasePrecision,
)
from anime_calendar.release_intelligence.confidence import assess_release_evidence


def test_airing_schedule_with_exact_time_is_high_confidence() -> None:
    evidence = (
        ReleaseEvidence(
            evidence_type=ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
            source_name="AniList airing schedule",
        ),
    )

    assessment = assess_release_evidence(
        evidence=evidence,
        precision=ReleasePrecision.EXACT_TIME,
    )

    assert assessment.date_status is ReleaseDateStatus.CONFIRMED
    assert assessment.confidence is ReleaseConfidence.HIGH
    assert assessment.score == 65
    assert assessment.reasons


def test_media_start_date_is_reported_medium_confidence() -> None:
    evidence = (
        ReleaseEvidence(
            evidence_type=ReleaseEvidenceType.ANILIST_MEDIA_START_DATE,
            source_name="AniList media start date",
        ),
    )

    assessment = assess_release_evidence(
        evidence=evidence,
        precision=ReleasePrecision.EXACT_DATE,
    )

    assert assessment.date_status is ReleaseDateStatus.REPORTED
    assert assessment.confidence is ReleaseConfidence.MEDIUM
    assert assessment.score == 40


def test_historical_pattern_is_explicitly_estimated() -> None:
    evidence = (
        ReleaseEvidence(
            evidence_type=ReleaseEvidenceType.HISTORICAL_PATTERN,
            source_name="Historical pattern",
        ),
    )

    assessment = assess_release_evidence(
        evidence=evidence,
        precision=ReleasePrecision.EXACT_DATE,
    )

    assert assessment.date_status is ReleaseDateStatus.ESTIMATED
    assert assessment.confidence is ReleaseConfidence.LOW
    assert assessment.score == 25


def test_missing_evidence_has_unknown_confidence() -> None:
    assessment = assess_release_evidence(
        evidence=(),
        precision=ReleasePrecision.UNKNOWN,
    )

    assert assessment.date_status is ReleaseDateStatus.UNKNOWN
    assert assessment.confidence is ReleaseConfidence.UNKNOWN
    assert assessment.score == 0
    assert assessment.reasons == ()