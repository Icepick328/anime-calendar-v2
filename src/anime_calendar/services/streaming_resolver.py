from __future__ import annotations

import re
from collections.abc import Iterable
from urllib.parse import urlparse

from anime_calendar.knowledge.loader import (
    load_anime_streaming_knowledge,
    load_provider_catalog,
)
from anime_calendar.models import (
    ExternalLink,
    ProviderConfidence,
    ProviderEvidence,
    StreamingProvider,
)

_NON_ALNUM = re.compile(r"[^a-z0-9+]+")
_PREFERRED_ORDER = {
    "crunchyroll": 0,
    "hidive": 1,
    "netflix": 2,
    "hulu": 3,
    "disney_plus": 4,
    "prime_video": 5,
    "youtube": 6,
}


def _normalize_name(value: str) -> str:
    return _NON_ALNUM.sub(" ", value.casefold()).strip()


def _provider_id_for_link(link: ExternalLink) -> str | None:
    catalog = load_provider_catalog()
    normalized_site = _normalize_name(link.site)
    hostname = (urlparse(link.url).hostname or "").casefold()

    for provider_id, definition in catalog.items():
        aliases = {_normalize_name(alias) for alias in definition.get("aliases", [])}
        domains = {domain.casefold() for domain in definition.get("domains", [])}
        if normalized_site in aliases:
            return provider_id
        if any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains):
            return provider_id
    return None


def _from_external_link(link: ExternalLink) -> StreamingProvider | None:
    provider_id = _provider_id_for_link(link)
    if provider_id is None:
        return None

    definition = load_provider_catalog()[provider_id]
    official_streaming = (link.link_type or "").casefold() == "streaming"
    return StreamingProvider(
        provider_id=provider_id,
        display_name=str(definition["display_name"]),
        url=link.url,
        confidence=(
            ProviderConfidence.VERIFIED if official_streaming else ProviderConfidence.HIGH
        ),
        evidence=(
            ProviderEvidence.OFFICIAL_STREAMING_LINK
            if official_streaming
            else ProviderEvidence.EXTERNAL_LINK
        ),
    )


def _from_knowledge(anilist_id: int) -> Iterable[StreamingProvider]:
    catalog = load_provider_catalog()
    entries = load_anime_streaming_knowledge().get(str(anilist_id), [])
    for entry in entries:
        provider_id = str(entry.get("provider", ""))
        definition = catalog.get(provider_id)
        if not definition:
            continue
        try:
            confidence = ProviderConfidence(str(entry.get("confidence", "medium")))
        except ValueError:
            confidence = ProviderConfidence.MEDIUM
        yield StreamingProvider(
            provider_id=provider_id,
            display_name=str(definition["display_name"]),
            url=entry.get("url"),
            confidence=confidence,
            evidence=ProviderEvidence.CURATED_KNOWLEDGE,
            regions=tuple(entry.get("regions") or ()),
            sub_languages=tuple(entry.get("sub_languages") or ()),
            dub_languages=tuple(entry.get("dub_languages") or ()),
            simulcast=entry.get("simulcast"),
        )


def _select_better(
    current: StreamingProvider | None,
    candidate: StreamingProvider,
) -> StreamingProvider:
    if current is None:
        return candidate
    if candidate.confidence.rank > current.confidence.rank:
        return candidate
    if candidate.confidence.rank == current.confidence.rank and candidate.url and not current.url:
        return candidate
    return current


def resolve_streaming_providers(
    anilist_id: int,
    external_links: Iterable[ExternalLink],
) -> tuple[StreamingProvider, ...]:
    resolved: dict[str, StreamingProvider] = {}

    for link in external_links:
        candidate = _from_external_link(link)
        if candidate is not None:
            resolved[candidate.provider_id] = _select_better(
                resolved.get(candidate.provider_id), candidate
            )

    for candidate in _from_knowledge(anilist_id):
        resolved[candidate.provider_id] = _select_better(
            resolved.get(candidate.provider_id), candidate
        )

    return tuple(
        sorted(
            resolved.values(),
            key=lambda provider: (
                _PREFERRED_ORDER.get(provider.provider_id, 99),
                -provider.confidence.rank,
                provider.display_name.casefold(),
            ),
        )
    )
