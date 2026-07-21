from dataclasses import replace
from datetime import UTC, datetime

from anime_calendar.diagnostics.quality import build_quality_report
from anime_calendar.diagnostics.report import format_quality_report
from anime_calendar.models import (
    Release,
    ReleaseDateStatus,
    ReleasePrecision,
    ReleaseType,
)
from tests.test_models import make_anime


def make_release(
    *,
    anime=None,
    release_type: ReleaseType = ReleaseType.EPISODE,
    episode_number: int | None = 1,
    date_status: ReleaseDateStatus = ReleaseDateStatus.CONFIRMED,
) -> Release:
    return Release(
        anime=anime or make_anime(),
        release_type=release_type,
        episode_number=episode_number,
        released_at=datetime(2026, 7, 20, 2, tzinfo=UTC),
        date_status=date_status,
        precision=ReleasePrecision.EXACT_TIME,
    )


def test_empty_report_is_healthy() -> None:
    report = build_quality_report([])

    assert report.overall_score == 100
    assert report.release_count == 0
    assert report.duplicate_keys == 0
    assert all(report.integrity.values())


def test_metadata_completeness_uses_release_anime() -> None:
    complete_anime = replace(
        make_anime(),
        synopsis="A complete synopsis.",
        cover_image_url="https://example.com/cover.jpg",
    )
    complete = make_release(anime=complete_anime)
    incomplete_anime = replace(
        make_anime(),
        synopsis=None,
        genres=(),
        studios=(),
        cover_image_url=None,
        streaming_providers=(),
    )
    incomplete = make_release(
        anime=incomplete_anime,
        episode_number=2,
    )

    report = build_quality_report([complete, incomplete])

    assert report.metadata == {
        "streaming": 50.0,
        "synopsis": 50.0,
        "genres": 50.0,
        "studios": 50.0,
        "artwork": 50.0,
    }


def test_confidence_and_coverage_are_counted() -> None:
    releases = [
        make_release(
            episode_number=1,
            date_status=ReleaseDateStatus.CONFIRMED,
        ),
        make_release(
            episode_number=2,
            date_status=ReleaseDateStatus.ESTIMATED,
        ),
        make_release(
            release_type=ReleaseType.MOVIE,
            episode_number=None,
            date_status=ReleaseDateStatus.REPORTED,
        ),
    ]

    report = build_quality_report(releases)

    assert report.coverage["episode"] == 2
    assert report.coverage["movie"] == 1
    assert report.confidence["confirmed"] == 33.3
    assert report.confidence["reported"] == 33.3
    assert report.confidence["estimated"] == 33.3
    assert report.confidence["unknown"] == 0.0


def test_duplicate_stable_keys_fail_integrity() -> None:
    release = make_release()

    report = build_quality_report([release, release])

    assert report.duplicate_keys == 1
    assert report.integrity["duplicate_events"] is False
    assert report.overall_score < 100


def test_existing_diagnostic_codes_drive_integrity() -> None:
    class Finding:
        code = "naive_release_datetime"

    report = build_quality_report(
        [make_release()],
        [Finding()],
    )

    assert report.integrity["timezone_normalization"] is False


def test_renderer_contains_major_sections() -> None:
    report = build_quality_report([make_release()])
    output = format_quality_report(report)

    assert "Anime Calendar Quality Report" in output
    assert "Overall Health" in output
    assert "Calendar Integrity" in output
    assert "Metadata Completeness" in output
    assert "Release Confidence" in output
    assert "Release Coverage" in output
    assert "Total Releases" in output
