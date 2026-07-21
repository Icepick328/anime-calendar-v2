from __future__ import annotations

import argparse
import logging
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import IntEnum

from anime_calendar.config import load_settings
from anime_calendar.diagnostics.quality import build_quality_report
from anime_calendar.diagnostics.report import format_quality_report
from anime_calendar.logging_config import configure_logging
from anime_calendar.models import Release
from anime_calendar.providers.anilist import AniListError
from anime_calendar.release_intelligence.audit import audit_release
from anime_calendar.services.release_loader import load_live_releases

LOGGER = logging.getLogger(__name__)


class DiagnosticSeverity(IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3

    @classmethod
    def from_name(cls, value: str) -> "DiagnosticSeverity":
        try:
            return cls[value.strip().upper()]
        except KeyError as exc:
            raise ValueError(
                f"Unknown severity {value!r}; expected info, warning, or error."
            ) from exc


@dataclass(frozen=True, slots=True)
class DiagnosticFinding:
    code: str
    severity: DiagnosticSeverity
    stable_key: str
    title: str
    message: str


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    total_releases: int
    findings: tuple[DiagnosticFinding, ...]

    @property
    def error_count(self) -> int:
        return sum(f.severity is DiagnosticSeverity.ERROR for f in self.findings)

    @property
    def warning_count(self) -> int:
        return sum(f.severity is DiagnosticSeverity.WARNING for f in self.findings)

    @property
    def info_count(self) -> int:
        return sum(f.severity is DiagnosticSeverity.INFO for f in self.findings)

    @property
    def clean_release_count(self) -> int:
        affected = {f.stable_key for f in self.findings}
        return max(self.total_releases - len(affected), 0)


def _title(release: Release) -> str:
    anime = getattr(release, "anime", None)
    for name in ("title", "english_title", "romaji_title", "name"):
        value = getattr(anime, name, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "Untitled release"


def _stable_key(release: Release) -> str:
    value = getattr(release, "stable_key", None)
    if isinstance(value, str) and value.strip():
        return value.strip()

    try:
        value = getattr(audit_release(release), "stable_key", None)
    except (TypeError, ValueError):
        value = None

    return value.strip() if isinstance(value, str) and value.strip() else "unknown-stable-key"


def _finding(
    release: Release,
    code: str,
    severity: DiagnosticSeverity,
    message: str,
) -> DiagnosticFinding:
    return DiagnosticFinding(
        code=code,
        severity=severity,
        stable_key=_stable_key(release),
        title=_title(release),
        message=message,
    )


def diagnose_release(release: Release) -> tuple[DiagnosticFinding, ...]:
    findings: list[DiagnosticFinding] = []

    try:
        audit = audit_release(release)
    except (TypeError, ValueError) as exc:
        return (
            _finding(
                release,
                "audit_failed",
                DiagnosticSeverity.ERROR,
                f"Release intelligence audit failed: {exc}",
            ),
        )

    if _stable_key(release) == "unknown-stable-key":
        findings.append(
            _finding(
                release,
                "missing_stable_key",
                DiagnosticSeverity.ERROR,
                "Release does not expose a usable stable key.",
            )
        )

    if _title(release) == "Untitled release":
        findings.append(
            _finding(
                release,
                "missing_title",
                DiagnosticSeverity.ERROR,
                "Release does not contain a displayable title.",
            )
        )

    released_at = getattr(release, "released_at", None)
    if released_at is None:
        findings.append(
            _finding(
                release,
                "missing_release_datetime",
                DiagnosticSeverity.ERROR,
                "Release does not contain a release datetime.",
            )
        )
    elif getattr(released_at, "tzinfo", None) is None or released_at.utcoffset() is None:
        findings.append(
            _finding(
                release,
                "naive_release_datetime",
                DiagnosticSeverity.ERROR,
                "Release datetime is not timezone-aware.",
            )
        )

    if not getattr(release, "evidence", ()):
        findings.append(
            _finding(
                release,
                "missing_evidence",
                DiagnosticSeverity.WARNING,
                "Release has no supporting evidence records.",
            )
        )

    if audit.date_status == "confirmed" and audit.confidence in {"low", "unknown"}:
        findings.append(
            _finding(
                release,
                "confirmed_low_confidence",
                DiagnosticSeverity.WARNING,
                f"Release is confirmed but confidence is {audit.confidence}.",
            )
        )

    if audit.date_status == "confirmed" and audit.precision in {"partial_date", "unknown"}:
        findings.append(
            _finding(
                release,
                "confirmed_imprecise_date",
                DiagnosticSeverity.WARNING,
                "Confirmed release lacks an exact date or time.",
            )
        )

    if audit.confidence in {"verified", "high"} and not audit.fired_rules:
        findings.append(
            _finding(
                release,
                "confidence_without_rules",
                DiagnosticSeverity.WARNING,
                "Strong confidence exists without recorded scoring rules.",
            )
        )

    if (
        audit.streaming_providers
        and audit.release_type == "episode"
        and audit.lifecycle == "unknown"
    ):
        findings.append(
            _finding(
                release,
                "provider_without_lifecycle",
                DiagnosticSeverity.INFO,
                "Episode has a provider but no known lifecycle state.",
            )
        )

    return tuple(findings)


def diagnose_releases(releases: Sequence[Release]) -> DiagnosticReport:
    findings: list[DiagnosticFinding] = []
    grouped: dict[str, list[Release]] = defaultdict(list)

    for release in releases:
        findings.extend(diagnose_release(release))
        grouped[_stable_key(release)].append(release)

    for stable_key, matches in grouped.items():
        if stable_key == "unknown-stable-key" or len(matches) < 2:
            continue
        for release in matches:
            findings.append(
                _finding(
                    release,
                    "duplicate_stable_key",
                    DiagnosticSeverity.ERROR,
                    f"Stable key {stable_key!r} appears {len(matches)} times.",
                )
            )

    findings.sort(
        key=lambda f: (-int(f.severity), f.code, f.title.casefold(), f.stable_key)
    )
    return DiagnosticReport(len(releases), tuple(findings))


def filter_findings(
    findings: Iterable[DiagnosticFinding],
    *,
    minimum_severity: DiagnosticSeverity,
) -> tuple[DiagnosticFinding, ...]:
    return tuple(f for f in findings if f.severity >= minimum_severity)


def format_diagnostic_report(
    report: DiagnosticReport,
    *,
    minimum_severity: DiagnosticSeverity = DiagnosticSeverity.INFO,
    limit: int | None = None,
) -> str:
    visible = filter_findings(
        report.findings,
        minimum_severity=minimum_severity,
    )
    shown = visible[:limit] if limit is not None else visible
    counts = Counter(f.code for f in visible)

    lines = [
        "Anime Release Intelligence Diagnostics",
        "=" * 38,
        "",
        "Summary",
        "-------",
        f"  Releases scanned   {report.total_releases:>5}",
        f"  Clean releases     {report.clean_release_count:>5}",
        f"  Affected releases  {report.total_releases - report.clean_release_count:>5}",
        f"  Errors             {report.error_count:>5}",
        f"  Warnings           {report.warning_count:>5}",
        f"  Informational      {report.info_count:>5}",
        "",
        "Finding Types",
        "-------------",
    ]

    if counts:
        for code, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"  {code.replace('_', ' ').title():<28} {count:>5}")
    else:
        lines.append("  None")

    lines.extend(["", "Findings", "--------"])
    if not shown:
        lines.append("No findings matched the selected severity.")
    else:
        for finding in shown:
            lines.extend(
                [
                    f"[{finding.severity.name}] {finding.code}",
                    f"  Title: {finding.title}",
                    f"  Stable key: {finding.stable_key}",
                    f"  {finding.message}",
                    "",
                ]
            )

    if limit is not None and len(visible) > limit:
        lines.append(f"Showing {limit} of {len(visible)} findings.")

    return "\n".join(lines).rstrip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan live anime release data for integrity problems."
    )
    parser.add_argument(
        "--minimum-severity",
        choices=("info", "warning", "error"),
        default="info",
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--fail-on-error", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be greater than zero.")

    configure_logging()

    try:
        LOGGER.info("Fetching live releases for diagnostics")
        releases = load_live_releases(load_settings())
        report = diagnose_releases(releases)
        quality_report = build_quality_report(releases, report.findings)
        print(format_quality_report(quality_report))
        print()
        print(
            format_diagnostic_report(
                report,
                minimum_severity=DiagnosticSeverity.from_name(args.minimum_severity),
                limit=args.limit,
            )
        )
    except (AniListError, OSError, TypeError, ValueError) as exc:
        LOGGER.error("Release diagnostics failed: %s", exc)
        return 1

    if args.fail_on_warning and (report.warning_count or report.error_count):
        return 1
    if args.fail_on_error and report.error_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
