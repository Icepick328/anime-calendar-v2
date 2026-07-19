from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from anime_calendar.models import Release
from anime_calendar.release_intelligence.confidence import (
    assess_release_evidence,
)


@dataclass(frozen=True, slots=True)
class ReleaseAudit:
    stable_key: str
    title: str
    release_type: str
    episode_number: int | None
    released_at: datetime | date
    date_status: str
    confidence: str
    precision: str
    lifecycle: str
    variant: str
    score: int
    reasons: tuple[str, ...]
    evidence_sources: tuple[str, ...]
    evidence_types: tuple[str, ...]
    streaming_providers: tuple[str, ...]


def audit_release(release: Release) -> ReleaseAudit:
    assessment = assess_release_evidence(
        evidence=release.evidence,
        precision=release.precision,
    )

    return ReleaseAudit(
        stable_key=release.stable_key,
        title=release.anime.title,
        release_type=release.release_type.value,
        episode_number=release.episode_number,
        released_at=release.released_at,
        date_status=assessment.date_status.value,
        confidence=assessment.confidence.value,
        precision=assessment.precision.value,
        lifecycle=release.effective_lifecycle.value,
        variant=release.variant.value,
        score=assessment.score,
        reasons=assessment.reasons,
        evidence_sources=tuple(
            item.source_name
            for item in release.evidence
        ),
        evidence_types=tuple(
            item.evidence_type.value
            for item in release.evidence
        ),
        streaming_providers=tuple(
            provider.display_name
            for provider in release.anime.streaming_providers
        ),
    )


def format_release_audit(audit: ReleaseAudit) -> str:
    release_name = audit.title
    if audit.episode_number is not None:
        release_name = f"{release_name} - Episode {audit.episode_number}"

    released_at = audit.released_at.isoformat()

    reasons = (
        "\n".join(f"  - {reason}" for reason in audit.reasons)
        if audit.reasons
        else "  - No assessment reasons available."
    )

    evidence = (
        "\n".join(
            f"  - {source} ({evidence_type})"
            for source, evidence_type in zip(
                audit.evidence_sources,
                audit.evidence_types,
                strict=True,
            )
        )
        if audit.evidence_sources
        else "  - No evidence available."
    )

    providers = (
        ", ".join(audit.streaming_providers)
        if audit.streaming_providers
        else "None identified"
    )

    return "\n".join(
        (
            release_name,
            "=" * len(release_name),
            f"Stable key: {audit.stable_key}",
            f"Release type: {audit.release_type}",
            f"Release date: {released_at}",
            f"Date status: {audit.date_status}",
            f"Confidence: {audit.confidence}",
            f"Confidence score: {audit.score}/100",
            f"Precision: {audit.precision}",
            f"Lifecycle: {audit.lifecycle}",
            f"Variant: {audit.variant}",
            f"Streaming providers: {providers}",
            "",
            "Reasons:",
            reasons,
            "",
            "Evidence:",
            evidence,
        )
    )
