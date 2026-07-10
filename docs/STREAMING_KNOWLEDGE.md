# Streaming knowledge guide

The resolver prefers structured AniList links. Curated knowledge is only for confirmed information that structured metadata does not expose.

## Provider catalog

`providers.json` defines canonical provider IDs, display names, aliases, and domains. Add a provider here before using it in title records.

## Title records

`anime_streaming.json` is keyed by AniList anime ID.

```json
{
  "151807": [
    {
      "provider": "crunchyroll",
      "url": "https://www.crunchyroll.com/series/example",
      "confidence": "verified",
      "regions": ["US", "CA"],
      "sub_languages": ["English"],
      "dub_languages": ["English"],
      "simulcast": true
    }
  ]
}
```

Allowed confidence values:

- `verified` — confirmed by an official provider or publisher source
- `high` — strong structured evidence
- `medium` — reliable curated evidence that is not first-party
- `low` — weak evidence; avoid unless clearly documented
- `unknown` — should generally not be stored

## Rules

- Do not guess provider availability.
- Prefer direct series URLs over provider homepages.
- Record regions only when known.
- Record languages only when confirmed.
- Do not use a dub language field to imply a release date.
- Keep regional availability separate from future theatrical-release modeling.
