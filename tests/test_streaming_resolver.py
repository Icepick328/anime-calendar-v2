from anime_calendar.models import (
    ExternalLink,
    ProviderConfidence,
    ProviderEvidence,
)
from anime_calendar.services import streaming_resolver
from anime_calendar.services.streaming_resolver import resolve_streaming_providers


def test_resolves_official_crunchyroll_streaming_link() -> None:
    providers = resolve_streaming_providers(
        42,
        (
            ExternalLink(
                site="Crunchyroll",
                url="https://www.crunchyroll.com/series/example",
                link_type="STREAMING",
            ),
        ),
    )

    assert len(providers) == 1
    provider = providers[0]
    assert provider.provider_id == "crunchyroll"
    assert provider.display_name == "Crunchyroll"
    assert provider.confidence is ProviderConfidence.VERIFIED
    assert provider.evidence is ProviderEvidence.OFFICIAL_STREAMING_LINK


def test_resolver_uses_curated_knowledge_and_prioritizes_crunchyroll(monkeypatch) -> None:
    monkeypatch.setattr(
        streaming_resolver,
        "load_anime_streaming_knowledge",
        lambda: {
            "7": [
                {
                    "provider": "netflix",
                    "url": "https://www.netflix.com/title/example",
                    "confidence": "medium",
                },
                {
                    "provider": "crunchyroll",
                    "url": "https://www.crunchyroll.com/series/example",
                    "confidence": "high",
                    "regions": ["US"],
                    "sub_languages": ["English"],
                },
            ]
        },
    )

    providers = resolve_streaming_providers(7, ())

    assert [provider.provider_id for provider in providers] == ["crunchyroll", "netflix"]
    assert providers[0].regions == ("US",)
    assert providers[0].language_summary == "Sub: English"
