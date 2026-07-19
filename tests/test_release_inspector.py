from datetime import UTC, datetime, timedelta

from anime_calendar.cli.inspect import (
    filter_releases,
    format_inspection_report,
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
    episode_number: int = 1,
    release_type: ReleaseType = ReleaseType.EPISODE,
) -> Release:
    return Release(
        anime=make_anime(),
        release_type=release_type,
        episode_number=episode_number,
        released_at=datetime.now(UTC) + timedelta(days=1),
        date_status=ReleaseDateStatus.CONFIRMED,
        confidence=ReleaseConfidence.HIGH,
        precision=ReleasePrecision.EXACT_TIME,
        variant=ReleaseVariant.ORIGINAL,
        evidence=(
            ReleaseEvidence(
                evidence_type=(
                    ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE
                ),
                source_name="AniList airing schedule",
            ),
        ),
    )


def test_filter_releases_matches_title() -> None:
    release = make_release()

    results = filter_releases(
        [release],
        title=release.anime.title.lower(),
    )

    assert results == [release]


def test_filter_releases_matches_assessment_fields() -> None:
    release = make_release()

    results = filter_releases(
        [release],
        release_type="episode",
        confidence="high",
        status="confirmed",
    )

    assert results == [release]


def test_filter_releases_rejects_nonmatching_type() -> None:
    release = make_release()

    results = filter_releases(
        [release],
        release_type="movie",
    )

    assert results == []


def test_inspection_report_includes_rule_diagnostics() -> None:
    release = make_release()

    report = format_inspection_report(
        [release],
        total_available=1,
    )

    assert "Upcoming Anime Release Intelligence Report" in report
    assert release.anime.title in report
    assert "Confidence score: 65/100" in report
    assert "Rules fired:" in report
    assert "anilist_airing_schedule" in report
    assert "exact_time" in report


def test_inspection_report_handles_no_matches() -> None:
    report = format_inspection_report(
        [],
        total_available=0,
    )

    assert "No releases matched" in report
