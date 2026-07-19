from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence

from anime_calendar.config import load_settings
from anime_calendar.logging_config import configure_logging
from anime_calendar.models import Release
from anime_calendar.providers.anilist import AniListError
from anime_calendar.release_intelligence.audit import (
    audit_release,
    format_release_audit,
)
from anime_calendar.services.release_loader import load_live_releases

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect live anime releases and explain their "
            "confidence assessments."
        )
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of releases to display. Default: 10.",
    )
    parser.add_argument(
        "--title",
        help="Display only releases whose title contains this text.",
    )
    parser.add_argument(
        "--type",
        dest="release_type",
        help="Display only one release type, such as episode or movie.",
    )
    parser.add_argument(
        "--provider",
        help="Display only releases available from this provider.",
    )
    parser.add_argument(
        "--confidence",
        help="Display only releases with this confidence level.",
    )
    parser.add_argument(
        "--status",
        help="Display only releases with this date status.",
    )
    return parser


def filter_releases(
    releases: Sequence[Release],
    *,
    title: str | None = None,
    release_type: str | None = None,
    provider: str | None = None,
    confidence: str | None = None,
    status: str | None = None,
) -> list[Release]:
    title_filter = title.casefold() if title else None
    type_filter = release_type.casefold() if release_type else None
    provider_filter = provider.casefold() if provider else None
    confidence_filter = confidence.casefold() if confidence else None
    status_filter = status.casefold() if status else None

    filtered: list[Release] = []

    for release in releases:
        audit = audit_release(release)

        if (
            title_filter is not None
            and title_filter not in audit.title.casefold()
        ):
            continue

        if (
            type_filter is not None
            and audit.release_type.casefold() != type_filter
        ):
            continue

        if (
            confidence_filter is not None
            and audit.confidence.casefold() != confidence_filter
        ):
            continue

        if (
            status_filter is not None
            and audit.date_status.casefold() != status_filter
        ):
            continue

        if provider_filter is not None:
            provider_names = {
                provider_name.casefold()
                for provider_name in audit.streaming_providers
            }
            if not any(
                provider_filter in provider_name
                for provider_name in provider_names
            ):
                continue

        filtered.append(release)

    return sorted(
        filtered,
        key=lambda item: item.released_at.isoformat(),
    )


def format_inspection_report(
    releases: Sequence[Release],
    *,
    total_available: int,
) -> str:
    heading = "Upcoming Anime Release Intelligence Report"
    separator = "-" * 72

    if not releases:
        return "\n".join(
            (
                heading,
                separator,
                "No releases matched the selected filters.",
            )
        )

    sections = [
        heading,
        separator,
        (
            f"Showing {len(releases)} of "
            f"{total_available} matching releases."
        ),
    ]

    for release in releases:
        sections.extend(
            (
                "",
                format_release_audit(audit_release(release)),
                "",
                separator,
            )
        )

    return "\n".join(sections)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)

    if arguments.limit < 1:
        parser.error("--limit must be at least 1")

    configure_logging()

    try:
        settings = load_settings()

        LOGGER.info("Fetching live releases for inspection")
        releases = load_live_releases(settings)

        matching_releases = filter_releases(
            releases,
            title=arguments.title,
            release_type=arguments.release_type,
            provider=arguments.provider,
            confidence=arguments.confidence,
            status=arguments.status,
        )

        visible_releases = matching_releases[: arguments.limit]

        print(
            format_inspection_report(
                visible_releases,
                total_available=len(matching_releases),
            )
        )
    except (AniListError, OSError, TypeError, ValueError) as exc:
        LOGGER.error("Release inspection failed: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
