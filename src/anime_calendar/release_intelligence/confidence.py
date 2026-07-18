from __future__ import annotations

from dataclasses import dataclass

from anime_calendar.models import (
    ReleaseConfidence,
    ReleaseDateStatus,
    ReleaseEvidence,
    ReleaseEvidenceType,
    ReleasePrecision,
)


@dataclass(frozen=True, slots=True)
class ReleaseAssessment:
    date_status: ReleaseDateStatus
    confidence: ReleaseConfidence
    precision: ReleasePrecision
    score: int
    reasons: tuple[str, ...]


def assess_release_evidence(
    evidence: tuple[ReleaseEvidence, ...],
    precision: ReleasePrecision,
) -> ReleaseAssessment:
    evidence_types = {item.evidence_type for item in evidence}
    reasons: list[str] = []
    score = 0

    if ReleaseEvidenceType.OFFICIAL_ANNOUNCEMENT in evidence_types:
        score += 50
        reasons.append("Supported by an official announcement.")

    if ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE in evidence_types:
        score += 40
        reasons.append("AniList supplied a precise airing-schedule entry.")

    if ReleaseEvidenceType.CURATED_KNOWLEDGE in evidence_types:
        score += 30
        reasons.append("Supported by curated streaming knowledge.")

    if ReleaseEvidenceType.ANILIST_MEDIA_START_DATE in evidence_types:
        score += 25
        reasons.append("AniList supplied a media start date.")

    if ReleaseEvidenceType.HISTORICAL_PATTERN in evidence_types:
        score += 10
        reasons.append("Date is inferred from a historical release pattern.")

    if precision is ReleasePrecision.EXACT_TIME:
        score += 25
        reasons.append("Release includes an exact time.")
    elif precision is ReleasePrecision.EXACT_DATE:
        score += 15
        reasons.append("Release includes an exact calendar date.")
    elif precision is ReleasePrecision.PARTIAL_DATE:
        score += 5
        reasons.append("Only a partial release date is available.")

    score = min(score, 100)

    if score >= 90:
        confidence = ReleaseConfidence.VERIFIED
    elif score >= 65:
        confidence = ReleaseConfidence.HIGH
    elif score >= 40:
        confidence = ReleaseConfidence.MEDIUM
    elif score > 0:
        confidence = ReleaseConfidence.LOW
    else:
        confidence = ReleaseConfidence.UNKNOWN

    if (
        ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE in evidence_types
        and precision is ReleasePrecision.EXACT_TIME
    ):
        date_status = ReleaseDateStatus.CONFIRMED
    elif (
        ReleaseEvidenceType.OFFICIAL_ANNOUNCEMENT in evidence_types
        and precision in {ReleasePrecision.EXACT_TIME, ReleasePrecision.EXACT_DATE}
    ):
        date_status = ReleaseDateStatus.CONFIRMED
    elif ReleaseEvidenceType.HISTORICAL_PATTERN in evidence_types:
        date_status = ReleaseDateStatus.ESTIMATED
    elif evidence:
        date_status = ReleaseDateStatus.REPORTED
    else:
        date_status = ReleaseDateStatus.UNKNOWN

    return ReleaseAssessment(
        date_status=date_status,
        confidence=confidence,
        precision=precision,
        score=score,
        reasons=tuple(reasons),
    )