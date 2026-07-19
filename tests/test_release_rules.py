import pytest

from anime_calendar.models import (
    ReleaseEvidenceType,
    ReleasePrecision,
)
from anime_calendar.release_intelligence.rules import (
    ANILIST_AIRING_SCHEDULE_RULE,
    DEFAULT_SCORING_RULES,
    EXACT_TIME_RULE,
    EvidenceScoringRule,
    PrecisionScoringRule,
    evaluate_scoring_rules,
)


@pytest.mark.parametrize(
    ("evidence_type", "expected_score", "expected_reason"),
    (
        (
            ReleaseEvidenceType.OFFICIAL_ANNOUNCEMENT,
            50,
            "Supported by an official announcement.",
        ),
        (
            ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
            40,
            "AniList supplied a precise airing-schedule entry.",
        ),
        (
            ReleaseEvidenceType.CURATED_KNOWLEDGE,
            30,
            "Supported by curated streaming knowledge.",
        ),
        (
            ReleaseEvidenceType.ANILIST_MEDIA_START_DATE,
            25,
            "AniList supplied a media start date.",
        ),
        (
            ReleaseEvidenceType.HISTORICAL_PATTERN,
            10,
            "Date is inferred from a historical release pattern.",
        ),
    ),
)
def test_evidence_rules_contribute_expected_scores(
    evidence_type: ReleaseEvidenceType,
    expected_score: int,
    expected_reason: str,
) -> None:
    rule = next(
        candidate
        for candidate in DEFAULT_SCORING_RULES
        if (
            isinstance(candidate, EvidenceScoringRule)
            and candidate.evidence_type is evidence_type
        )
    )

    result = rule.evaluate(
        evidence_types={evidence_type},
        precision=ReleasePrecision.UNKNOWN,
    )

    assert result.score == expected_score
    assert result.reasons == (expected_reason,)


@pytest.mark.parametrize(
    ("precision", "expected_score", "expected_reason"),
    (
        (
            ReleasePrecision.EXACT_TIME,
            25,
            "Release includes an exact time.",
        ),
        (
            ReleasePrecision.EXACT_DATE,
            15,
            "Release includes an exact calendar date.",
        ),
        (
            ReleasePrecision.PARTIAL_DATE,
            5,
            "Only a partial release date is available.",
        ),
    ),
)
def test_precision_rules_contribute_expected_scores(
    precision: ReleasePrecision,
    expected_score: int,
    expected_reason: str,
) -> None:
    rule = next(
        candidate
        for candidate in DEFAULT_SCORING_RULES
        if (
            isinstance(candidate, PrecisionScoringRule)
            and candidate.precision is precision
        )
    )

    result = rule.evaluate(
        evidence_types=set(),
        precision=precision,
    )

    assert result.score == expected_score
    assert result.reasons == (expected_reason,)


def test_nonmatching_rule_does_not_contribute() -> None:
    result = ANILIST_AIRING_SCHEDULE_RULE.evaluate(
        evidence_types=set(),
        precision=ReleasePrecision.EXACT_TIME,
    )

    assert result.score == 0
    assert result.reasons == ()


def test_rule_engine_combines_evidence_and_precision() -> None:
    result = evaluate_scoring_rules(
        evidence_types={
            ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
        },
        precision=ReleasePrecision.EXACT_TIME,
    )

    assert result.score == 65
    assert result.reasons == (
        "AniList supplied a precise airing-schedule entry.",
        "Release includes an exact time.",
    )


def test_rule_engine_caps_score_at_one_hundred() -> None:
    result = evaluate_scoring_rules(
        evidence_types={
            ReleaseEvidenceType.OFFICIAL_ANNOUNCEMENT,
            ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
            ReleaseEvidenceType.CURATED_KNOWLEDGE,
            ReleaseEvidenceType.ANILIST_MEDIA_START_DATE,
            ReleaseEvidenceType.HISTORICAL_PATTERN,
        },
        precision=ReleasePrecision.EXACT_TIME,
    )

    assert result.score == 100


def test_default_rule_names_are_unique() -> None:
    rule_names = tuple(rule.name for rule in DEFAULT_SCORING_RULES)

    assert len(rule_names) == len(set(rule_names))


def test_exact_time_rule_is_independently_evaluable() -> None:
    result = EXACT_TIME_RULE.evaluate(
        evidence_types=set(),
        precision=ReleasePrecision.EXACT_TIME,
    )

    assert result.score == 25
    assert result.reasons == ("Release includes an exact time.",)
