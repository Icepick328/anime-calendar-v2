from datetime import UTC, datetime, timedelta

from anime_calendar.cli.diagnostics import (
    DiagnosticFinding,
    DiagnosticReport,
    DiagnosticSeverity,
    diagnose_releases,
    filter_findings,
    format_diagnostic_report,
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
    evidence: tuple[ReleaseEvidence, ...] | None = None,
    released_at: datetime | None = None,
) -> Release:
    resolved_evidence = evidence
    if resolved_evidence is None:
        resolved_evidence = (
            ReleaseEvidence(
                evidence_type=ReleaseEvidenceType.ANILIST_AIRING_SCHEDULE,
                source_name="AniList airing schedule",
            ),
        )

    return Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=episode_number,
        released_at=released_at or datetime.now(UTC) + timedelta(days=1),
        date_status=ReleaseDateStatus.CONFIRMED,
        confidence=ReleaseConfidence.HIGH,
        precision=ReleasePrecision.EXACT_TIME,
        variant=ReleaseVariant.ORIGINAL,
        evidence=resolved_evidence,
    )


def test_clean_release_has_no_diagnostic_findings() -> None:
    report = diagnose_releases([make_release()])
    assert report.findings == ()
    assert report.clean_release_count == 1


def test_missing_evidence_creates_warning() -> None:
    report = diagnose_releases([make_release(evidence=())])
    assert any(
        f.code == "missing_evidence"
        and f.severity is DiagnosticSeverity.WARNING
        for f in report.findings
    )


def test_naive_datetime_creates_error() -> None:
    report = diagnose_releases(
        [make_release(released_at=datetime.now() + timedelta(days=1))]
    )
    assert any(
        f.code == "naive_release_datetime"
        and f.severity is DiagnosticSeverity.ERROR
        for f in report.findings
    )


def test_duplicate_stable_keys_create_errors() -> None:
    release = make_release()
    report = diagnose_releases([release, release])
    duplicates = [f for f in report.findings if f.code == "duplicate_stable_key"]
    assert len(duplicates) == 2
    assert report.error_count == 2


def test_filter_findings_respects_minimum_severity() -> None:
    findings = (
        DiagnosticFinding("info", DiagnosticSeverity.INFO, "1", "One", "Info"),
        DiagnosticFinding("warning", DiagnosticSeverity.WARNING, "2", "Two", "Warning"),
        DiagnosticFinding("error", DiagnosticSeverity.ERROR, "3", "Three", "Error"),
    )
    filtered = filter_findings(
        findings,
        minimum_severity=DiagnosticSeverity.WARNING,
    )
    assert [f.code for f in filtered] == ["warning", "error"]


def test_report_counts_severities() -> None:
    report = DiagnosticReport(
        total_releases=3,
        findings=(
            DiagnosticFinding("warning", DiagnosticSeverity.WARNING, "1", "One", "Warning"),
            DiagnosticFinding("error", DiagnosticSeverity.ERROR, "2", "Two", "Error"),
            DiagnosticFinding("info", DiagnosticSeverity.INFO, "3", "Three", "Info"),
        ),
    )
    assert report.error_count == 1
    assert report.warning_count == 1
    assert report.info_count == 1
    assert report.clean_release_count == 0


def test_format_report_contains_summary_and_findings() -> None:
    output = format_diagnostic_report(
        diagnose_releases([make_release(evidence=())])
    )
    assert "Anime Release Intelligence Diagnostics" in output
    assert "Summary" in output
    assert "Finding Types" in output
    assert "missing_evidence" in output
    assert "[WARNING]" in output


def test_format_report_handles_clean_dataset() -> None:
    output = format_diagnostic_report(diagnose_releases([make_release()]))
    assert "Clean releases         1" in output
    assert "No findings matched" in output
