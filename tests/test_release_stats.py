from datetime import UTC, datetime, timedelta

from anime_calendar.cli.stats import (
    filter_releases,
    format_statistics_report,
    summarize_releases,
)
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
from tests.test_models import make_anime


def make_release(
    *,
    release_type: ReleaseType = ReleaseType.EPISODE,
    episode_number: int | None = 1,
    evidence: tuple[ReleaseEvidence, ...] | None = None,
) -> Release:
    release_evidence = evidence

    if release_evidence is None:
        release_evidence = (
            ReleaseEvidence(
                evidence_type=(
                    ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE
                ),
                source_name="AniList airing schedule",
            ),
        )

    return Release(
        anime=make_anime(),
        release_type=release_type,
        episode_number=episode_number,
        released_at=datetime.now(UTC) + timedelta(days=1),
        date_status=ReleaseDateStatus.CONFIRMED,
        confidence=ReleaseConfidence.HIGH,
        precision=ReleasePrecision.EXACT_TIME,
        variant=ReleaseVariant.ORIGINAL,
        evidence=release_evidence,
    )


def test_summarize_releases_counts_release_types() -> None:
    releases = [
        make_release(),
        make_release(episode_number=2),
        make_release(
            release_type=ReleaseType.MOVIE,
            episode_number=None,
        ),
    ]

    statistics = summarize_releases(releases)

    assert statistics.total_releases == 3
    assert dict(statistics.release_types) == {
        "episode": 2,
        "movie": 1,
    }


def test_summarize_releases_counts_assessments() -> None:
    releases = [
        make_release(),
        make_release(episode_number=2),
    ]

    statistics = summarize_releases(releases)

    assert dict(statistics.confidence_levels) == {
        "high": 2,
    }
    assert dict(statistics.date_statuses) == {
        "confirmed": 2,
    }
    assert dict(statistics.precision_levels) == {
        "exact_time": 2,
    }


def test_summarize_releases_counts_rules() -> None:
    statistics = summarize_releases(
        [make_release()]
    )

    assert dict(statistics.fired_rules) == {
        "anilist_airing_schedule": 1,
        "exact_time": 1,
    }


def test_summarize_releases_counts_evidence_coverage() -> None:
    releases = [
        make_release(),
        make_release(
            episode_number=2,
            evidence=(),
        ),
    ]

    statistics = summarize_releases(releases)

    assert statistics.releases_with_evidence == 1
    assert statistics.releases_without_evidence == 1


def test_statistics_report_contains_core_sections() -> None:
    statistics = summarize_releases(
        [make_release()]
    )

    report = format_statistics_report(statistics)

    assert "Anime Release Intelligence Statistics" in report
    assert "Total releases: 1" in report
    assert "Release Types" in report
    assert "Confidence" in report
    assert "Date Status" in report
    assert "Date Precision" in report
    assert "Coverage" in report
    assert "Streaming Providers" in report
    assert "Rule Usage" in report


def test_statistics_report_handles_empty_dataset() -> None:
    statistics = summarize_releases([])

    report = format_statistics_report(statistics)

    assert "Total releases: 0" in report
    assert "0.0%" in report


def test_filter_releases_matches_release_type() -> None:
    episode = make_release()
    movie = make_release(
        release_type=ReleaseType.MOVIE,
        episode_number=None,
    )

    results = filter_releases(
        [episode, movie],
        release_type="movie",
    )

    assert results == [movie]


def test_filter_releases_rejects_unknown_provider() -> None:
    release = make_release()

    results = filter_releases(
        [release],
        provider="provider-that-does-not-exist",
    )

    assert results == []
