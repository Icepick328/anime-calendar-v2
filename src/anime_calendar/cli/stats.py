from __future__ import annotations

import argparse
import logging
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from anime_calendar.config import load_settings
from anime_calendar.logging_config import configure_logging
from anime_calendar.models import Release
from anime_calendar.providers.anilist import AniListError
from anime_calendar.release_intelligence.audit import audit_release
from anime_calendar.services.release_loader import load_live_releases

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ReleaseStatistics:
    total_releases: int
    release_types: tuple[tuple[str, int], ...]
    confidence_levels: tuple[tuple[str, int], ...]
    date_statuses: tuple[tuple[str, int], ...]
    precision_levels: tuple[tuple[str, int], ...]
    providers: tuple[tuple[str, int], ...]
    fired_rules: tuple[tuple[str, int], ...]
    releases_with_providers: int
    releases_without_providers: int
    releases_with_evidence: int
    releases_without_evidence: int


def _sorted_counts(
    counter: Counter[str],
    *,
    preferred_order: tuple[str, ...] = (),
) -> tuple[tuple[str, int], ...]:
    preferred_positions = {
        name: position
        for position, name in enumerate(preferred_order)
    }

    return tuple(
        sorted(
            counter.items(),
            key=lambda item: (
                preferred_positions.get(
                    item[0],
                    len(preferred_positions),
                ),
                -item[1],
                item[0],
            ),
        )
    )


def summarize_releases(
    releases: Sequence[Release],
) -> ReleaseStatistics:
    release_type_counts: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    precision_counts: Counter[str] = Counter()
    provider_counts: Counter[str] = Counter()
    rule_counts: Counter[str] = Counter()

    releases_with_providers = 0
    releases_with_evidence = 0

    for release in releases:
        audit = audit_release(release)

        release_type_counts[audit.release_type] += 1
        confidence_counts[audit.confidence] += 1
        status_counts[audit.date_status] += 1
        precision_counts[audit.precision] += 1

        if audit.streaming_providers:
            releases_with_providers += 1
            provider_counts.update(
                set(audit.streaming_providers)
            )

        if release.evidence:
            releases_with_evidence += 1

        rule_counts.update(
            set(audit.fired_rules)
        )

    total_releases = len(releases)

    return ReleaseStatistics(
        total_releases=total_releases,
        release_types=_sorted_counts(
            release_type_counts,
            preferred_order=(
                "episode",
                "movie",
                "ova",
                "ona",
                "special",
                "tv_short",
                "music",
                "other",
            ),
        ),
        confidence_levels=_sorted_counts(
            confidence_counts,
            preferred_order=(
                "verified",
                "high",
                "medium",
                "low",
                "unknown",
            ),
        ),
        date_statuses=_sorted_counts(
            status_counts,
            preferred_order=(
                "confirmed",
                "reported",
                "estimated",
                "unknown",
            ),
        ),
        precision_levels=_sorted_counts(
            precision_counts,
            preferred_order=(
                "exact_time",
                "exact_date",
                "partial_date",
                "unknown",
            ),
        ),
        providers=_sorted_counts(provider_counts),
        fired_rules=_sorted_counts(rule_counts),
        releases_with_providers=releases_with_providers,
        releases_without_providers=(
            total_releases - releases_with_providers
        ),
        releases_with_evidence=releases_with_evidence,
        releases_without_evidence=(
            total_releases - releases_with_evidence
        ),
    )


def _format_label(value: str) -> str:
    return value.replace("_", " ").title()


def _format_count_section(
    heading: str,
    values: tuple[tuple[str, int], ...],
) -> str:
    if not values:
        body = "  None"
    else:
        label_width = max(
            len(_format_label(name))
            for name, _ in values
        )
        body = "\n".join(
            (
                f"  {_format_label(name):<{label_width}}"
                f"  {count:>5}"
            )
            for name, count in values
        )

    return "\n".join(
        (
            heading,
            "-" * len(heading),
            body,
        )
    )


def _percentage(
    value: int,
    total: int,
) -> float:
    if total == 0:
        return 0.0

    return value / total * 100


def format_statistics_report(
    statistics: ReleaseStatistics,
) -> str:
    total = statistics.total_releases

    coverage = "\n".join(
        (
            "Coverage",
            "--------",
            (
                "  Streaming identified"
                f"  {statistics.releases_with_providers:>5}"
                f"  ({_percentage(statistics.releases_with_providers, total):5.1f}%)"
            ),
            (
                "  Streaming unknown"
                f"     {statistics.releases_without_providers:>5}"
                f"  ({_percentage(statistics.releases_without_providers, total):5.1f}%)"
            ),
            (
                "  Evidence available"
                f"    {statistics.releases_with_evidence:>5}"
                f"  ({_percentage(statistics.releases_with_evidence, total):5.1f}%)"
            ),
            (
                "  Evidence missing"
                f"      {statistics.releases_without_evidence:>5}"
                f"  ({_percentage(statistics.releases_without_evidence, total):5.1f}%)"
            ),
        )
    )

    return "\n\n".join(
        (
            "\n".join(
                (
                    "Anime Release Intelligence Statistics",
                    "=" * 37,
                    f"Total releases: {total}",
                )
            ),
            _format_count_section(
                "Release Types",
                statistics.release_types,
            ),
            _format_count_section(
                "Confidence",
                statistics.confidence_levels,
            ),
            _format_count_section(
                "Date Status",
                statistics.date_statuses,
            ),
            _format_count_section(
                "Date Precision",
                statistics.precision_levels,
            ),
            coverage,
            _format_count_section(
                "Streaming Providers",
                statistics.providers,
            ),
            _format_count_section(
                "Rule Usage",
                statistics.fired_rules,
            ),
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate statistics for live anime release "
            "intelligence data."
        )
    )
    parser.add_argument(
        "--provider",
        help=(
            "Include only releases associated with a provider "
            "whose name contains this text."
        ),
    )
    parser.add_argument(
        "--type",
        dest="release_type",
        help=(
            "Include only one release type, such as episode, "
            "movie, ona, ova, or special."
        ),
    )
    return parser


def filter_releases(
    releases: Sequence[Release],
    *,
    provider: str | None = None,
    release_type: str | None = None,
) -> list[Release]:
    provider_filter = (
        provider.casefold()
        if provider
        else None
    )
    type_filter = (
        release_type.casefold()
        if release_type
        else None
    )

    filtered: list[Release] = []

    for release in releases:
        audit = audit_release(release)

        if (
            type_filter is not None
            and audit.release_type.casefold() != type_filter
        ):
            continue

        if provider_filter is not None:
            provider_names = (
                provider_name.casefold()
                for provider_name in audit.streaming_providers
            )
            if not any(
                provider_filter in provider_name
                for provider_name in provider_names
            ):
                continue

        filtered.append(release)

    return filtered


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)

    configure_logging()

    try:
        settings = load_settings()

        LOGGER.info(
            "Fetching live releases for statistics"
        )
        releases = load_live_releases(settings)

        filtered_releases = filter_releases(
            releases,
            provider=arguments.provider,
            release_type=arguments.release_type,
        )

        statistics = summarize_releases(
            filtered_releases
        )
        print(format_statistics_report(statistics))
    except (
        AniListError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        LOGGER.error(
            "Release statistics generation failed: %s",
            exc,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
