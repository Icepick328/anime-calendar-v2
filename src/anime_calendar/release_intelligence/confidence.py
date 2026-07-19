from __future__ import annotations

from dataclasses import dataclass

from anime_calendar.models import (
    ReleaseConfidence,
    ReleaseDateStatus,
    ReleaseEvidence,
    ReleaseEvidenceType,
    ReleasePrecision,
)
from anime_calendar.release_intelligence.rules import (
    evaluate_scoring_rules,
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

    scoring_result = evaluate_scoring_rules(
        evidence_types=evidence_types,
        precision=precision,
    )

    score = scoring_result.score
    reasons = scoring_result.reasons

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
        and precision in {
            ReleasePrecision.EXACT_TIME,
            ReleasePrecision.EXACT_DATE,
        }
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
        reasons=reasons,
    )
