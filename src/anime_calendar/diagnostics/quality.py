from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from anime_calendar.models import Release, ReleaseDateStatus, ReleaseType


@dataclass(frozen=True, slots=True)
class QualityReport:
    overall_score: int
    release_count: int
    duplicate_keys: int
    metadata: dict[str, float]
    confidence: dict[str, float]
    coverage: dict[str, int]
    integrity: dict[str, bool]


def _percentage(part: int, total: int) -> float:
    if total == 0:
        return 100.0
    return round(part / total * 100, 1)


def _has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _metadata_scores(releases: Sequence[Release]) -> dict[str, float]:
    total = len(releases)

    return {
        "streaming": _percentage(
            sum(bool(release.anime.streaming_providers) for release in releases),
            total,
        ),
        "synopsis": _percentage(
            sum(_has_text(release.anime.synopsis) for release in releases),
            total,
        ),
        "genres": _percentage(
            sum(bool(release.anime.genres) for release in releases),
            total,
        ),
        "studios": _percentage(
            sum(bool(release.anime.studios) for release in releases),
            total,
        ),
        "artwork": _percentage(
            sum(_has_text(release.anime.cover_image_url) for release in releases),
            total,
        ),
    }


def _confidence_scores(releases: Sequence[Release]) -> dict[str, float]:
    counts = Counter(release.date_status.value for release in releases)
    total = len(releases)

    if total == 0:
        return {
            status.value: 0.0
            for status in ReleaseDateStatus
        }

    return {
        status.value: _percentage(counts[status.value], total)
        for status in ReleaseDateStatus
    }


def _coverage_counts(releases: Sequence[Release]) -> dict[str, int]:
    counts = Counter(release.release_type.value for release in releases)

    return {
        release_type.value: counts[release_type.value]
        for release_type in ReleaseType
    }


def _finding_codes(findings: Iterable[object]) -> set[str]:
    codes: set[str] = set()

    for finding in findings:
        code = getattr(finding, "code", None)
        if isinstance(code, str):
            codes.add(code)

    return codes


def _calculate_score(
    *,
    metadata: dict[str, float],
    confidence: dict[str, float],
    integrity: dict[str, bool],
) -> int:
    score = 100.0

    # Integrity failures are the strongest signal.
    score -= 10 * sum(not passed for passed in integrity.values())

    # Metadata can subtract no more than 30 points.
    metadata_weights = {
        "streaming": 0.10,
        "synopsis": 0.05,
        "genres": 0.05,
        "studios": 0.05,
        "artwork": 0.05,
    }
    score -= sum(
        (100.0 - metadata[name]) * weight
        for name, weight in metadata_weights.items()
    )

    # Uncertain release dates can subtract no more than 20 points.
    score -= confidence["estimated"] * 0.10
    score -= confidence["unknown"] * 0.10

    return max(0, min(100, round(score)))


def build_quality_report(
    releases: Sequence[Release],
    findings: Iterable[object] = (),
) -> QualityReport:
    codes = _finding_codes(findings)

    stable_key_counts = Counter(release.stable_key for release in releases)
    duplicate_keys = sum(
        count - 1
        for count in stable_key_counts.values()
        if count > 1
    )

    metadata = _metadata_scores(releases)
    confidence = _confidence_scores(releases)
    coverage = _coverage_counts(releases)

    integrity = {
        "duplicate_events": (
            duplicate_keys == 0
            and "duplicate_stable_key" not in codes
        ),
        "stable_keys": "missing_stable_key" not in codes,
        "timezone_normalization": "naive_release_datetime" not in codes,
        "release_datetimes": "missing_release_datetime" not in codes,
        "display_titles": "missing_title" not in codes,
    }

    return QualityReport(
        overall_score=_calculate_score(
            metadata=metadata,
            confidence=confidence,
            integrity=integrity,
        ),
        release_count=len(releases),
        duplicate_keys=duplicate_keys,
        metadata=metadata,
        confidence=confidence,
        coverage=coverage,
        integrity=integrity,
    )
