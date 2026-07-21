from __future__ import annotations

from anime_calendar.diagnostics.quality import QualityReport


def _rating(score: int) -> str:
    if score >= 95:
        return "Excellent"
    if score >= 85:
        return "Very Good"
    if score >= 70:
        return "Good"
    if score >= 50:
        return "Needs Attention"
    return "Poor"


def _stars(score: int) -> str:
    filled = min(5, max(0, (score + 9) // 20))
    return f"{'★' * filled}{'☆' * (5 - filled)}"


def _label(value: str) -> str:
    return value.replace("_", " ").title()


def format_quality_report(report: QualityReport) -> str:
    lines = [
        "Anime Calendar Quality Report",
        "=" * 29,
        "",
        "Overall Health",
        "--------------",
        f"  {_stars(report.overall_score)}  "
        f"{report.overall_score}/100",
        f"  {_rating(report.overall_score)}",
        "",
        "Calendar Integrity",
        "------------------",
    ]

    for name, passed in report.integrity.items():
        marker = "✓" if passed else "✗"
        lines.append(f"  {marker} {_label(name)}")

    lines.extend(
        [
            "",
            "Metadata Completeness",
            "---------------------",
        ]
    )
    for name, percentage in report.metadata.items():
        lines.append(f"  {_label(name):<18} {percentage:>6.1f}%")

    lines.extend(
        [
            "",
            "Release Confidence",
            "------------------",
        ]
    )
    for name, percentage in report.confidence.items():
        lines.append(f"  {_label(name):<18} {percentage:>6.1f}%")

    lines.extend(
        [
            "",
            "Release Coverage",
            "----------------",
        ]
    )
    for name, count in report.coverage.items():
        lines.append(f"  {_label(name):<18} {count:>6}")

    lines.extend(
        [
            "",
            f"  Total Releases     {report.release_count:>6}",
            f"  Duplicate Keys     {report.duplicate_keys:>6}",
        ]
    )

    return "\n".join(lines)
