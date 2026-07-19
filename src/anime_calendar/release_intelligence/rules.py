from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from anime_calendar.models import (
    ReleaseEvidenceType,
    ReleasePrecision,
)


@dataclass(frozen=True, slots=True)
class RuleResult:
    score: int
    reasons: tuple[str, ...]
    fired_rules: tuple[str, ...]


class ScoringRule(Protocol):
    name: str

    def evaluate(
        self,
        evidence_types: set[ReleaseEvidenceType],
        precision: ReleasePrecision,
    ) -> RuleResult:
        ...


@dataclass(frozen=True, slots=True)
class EvidenceScoringRule:
    name: str
    evidence_type: ReleaseEvidenceType
    score: int
    reason: str

    def evaluate(
        self,
        evidence_types: set[ReleaseEvidenceType],
        precision: ReleasePrecision,
    ) -> RuleResult:
        del precision

        if self.evidence_type not in evidence_types:
            return RuleResult(
                score=0,
                reasons=(),
                fired_rules=(),
            )

        return RuleResult(
            score=self.score,
            reasons=(self.reason,),
            fired_rules=(self.name,),
        )


@dataclass(frozen=True, slots=True)
class PrecisionScoringRule:
    name: str
    precision: ReleasePrecision
    score: int
    reason: str

    def evaluate(
        self,
        evidence_types: set[ReleaseEvidenceType],
        precision: ReleasePrecision,
    ) -> RuleResult:
        del evidence_types

        if precision is not self.precision:
            return RuleResult(
                score=0,
                reasons=(),
                fired_rules=(),
            )

        return RuleResult(
            score=self.score,
            reasons=(self.reason,),
            fired_rules=(self.name,),
        )


OFFICIAL_ANNOUNCEMENT_RULE = EvidenceScoringRule(
    name="official_announcement",
    evidence_type=ReleaseEvidenceType.OFFICIAL_ANNOUNCEMENT,
    score=50,
    reason="Supported by an official announcement.",
)

ANILIST_AIRING_SCHEDULE_RULE = EvidenceScoringRule(
    name="anilist_airing_schedule",
    evidence_type=ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
    score=40,
    reason="AniList supplied a precise airing-schedule entry.",
)

CURATED_KNOWLEDGE_RULE = EvidenceScoringRule(
    name="curated_knowledge",
    evidence_type=ReleaseEvidenceType.CURATED_KNOWLEDGE,
    score=30,
    reason="Supported by curated streaming knowledge.",
)

ANILIST_MEDIA_START_DATE_RULE = EvidenceScoringRule(
    name="anilist_media_start_date",
    evidence_type=ReleaseEvidenceType.ANILIST_MEDIA_START_DATE,
    score=25,
    reason="AniList supplied a media start date.",
)

HISTORICAL_PATTERN_RULE = EvidenceScoringRule(
    name="historical_pattern",
    evidence_type=ReleaseEvidenceType.HISTORICAL_PATTERN,
    score=10,
    reason="Date is inferred from a historical release pattern.",
)

EXACT_TIME_RULE = PrecisionScoringRule(
    name="exact_time",
    precision=ReleasePrecision.EXACT_TIME,
    score=25,
    reason="Release includes an exact time.",
)

EXACT_DATE_RULE = PrecisionScoringRule(
    name="exact_date",
    precision=ReleasePrecision.EXACT_DATE,
    score=15,
    reason="Release includes an exact calendar date.",
)

PARTIAL_DATE_RULE = PrecisionScoringRule(
    name="partial_date",
    precision=ReleasePrecision.PARTIAL_DATE,
    score=5,
    reason="Only a partial release date is available.",
)


DEFAULT_SCORING_RULES: tuple[ScoringRule, ...] = (
    OFFICIAL_ANNOUNCEMENT_RULE,
    ANILIST_AIRING_SCHEDULE_RULE,
    CURATED_KNOWLEDGE_RULE,
    ANILIST_MEDIA_START_DATE_RULE,
    HISTORICAL_PATTERN_RULE,
    EXACT_TIME_RULE,
    EXACT_DATE_RULE,
    PARTIAL_DATE_RULE,
)


def evaluate_scoring_rules(
    evidence_types: set[ReleaseEvidenceType],
    precision: ReleasePrecision,
    rules: tuple[ScoringRule, ...] = DEFAULT_SCORING_RULES,
) -> RuleResult:
    score = 0
    reasons: list[str] = []
    fired_rules: list[str] = []

    for rule in rules:
        result = rule.evaluate(
            evidence_types=evidence_types,
            precision=precision,
        )
        score += result.score
        reasons.extend(result.reasons)
        fired_rules.extend(result.fired_rules)

    return RuleResult(
        score=min(score, 100),
        reasons=tuple(reasons),
        fired_rules=tuple(fired_rules),
    )
