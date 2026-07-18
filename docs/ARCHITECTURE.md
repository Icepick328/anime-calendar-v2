# Architecture

> **Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

## Architectural philosophy

The project builds reusable engines around canonical models. Calendars are an output—not the core business model. Public release intelligence remains separate from private account data. Uncertainty, confidence, and evidence are preserved through every layer.

```text
Data Sources
    ↓
Metadata and Release Ingestion
    ↓
Canonical Anime and Release Models
    ↓
Streaming Intelligence + Release Intelligence
    ↓
Filtering and Personalization
    ↓
Output Plugins: ICS, dashboard, API, notifications
```

Major architectural choices are documented in `docs/adr/`. Governance and quality gates are defined in `PROJECT_CHARTER.md` and `RELEASE_PROCESS.md`.

## Pipeline

```text
AniList episode schedule ─┐
                         ├─> Metadata transformers ─> Streaming resolver ─> Release objects
AniList media start dates ┘                                  │                    │
                                                            │                    ├─ ICS feeds
Curated provider knowledge ──────────────────────────────────┘                    ├─ dashboard (future)
                                                                                 └─ API (future)
```

## Canonical release model

`Release` represents both timed episode airings and date-only media releases.

- Episodes use timezone-aware datetimes from AniList `AiringSchedule`.
- Movies and one-off formats use AniList `Media.startDate`.
- Incomplete dates are omitted rather than invented.
- Date-only releases become all-day iCalendar events.
- Stable keys prevent duplicates and support subscribed-calendar updates.

## Streaming domain

`StreamingProvider` is provider-neutral and contains:

- Canonical provider ID
- Display name
- Watch URL
- Confidence
- Evidence source
- Regions
- Subtitle languages
- Dub languages
- Simulcast state

The calendar layer does not infer providers. It only renders provider objects attached by the resolver.

## Resolver order

1. Normalize structured AniList external links.
2. Match exact provider aliases or URL domains.
3. Mark official `STREAMING` links as verified.
4. Mark other recognized external links as high confidence.
5. Merge curated knowledge records.
6. Keep the strongest record for each provider.
7. Order Crunchyroll first, then other canonical providers.

Unknown providers remain absent. The resolver never assigns a provider merely because a title is popular or likely to stream there.

## Knowledge package

```text
src/anime_calendar/knowledge/
├── providers.json
├── anime_streaming.json
└── loader.py
```

`providers.json` defines canonical providers, aliases, and domains. `anime_streaming.json` supplements titles whose structured links are missing or incomplete.

## Output feeds

- Combined releases
- Episodes
- Movies
- OVAs/ONAs/specials
- Confirmed streaming availability
- Crunchyroll
- HIDIVE

Provider feeds may be empty while remaining valid iCalendar documents.

## Account readiness

Future account filters operate on canonical release type, genres, providers, language, date, and AniList ID. Calendar generation accepts filtered `Release` objects, so authentication and personalized feeds can be added without rewriting ingestion or calendar formatting.

## Release Intelligence (v0.5.0)

The canonical `Release` object now carries date status, release confidence, date precision, release variant, lifecycle, and structured evidence. Data ingestion assigns these values; output plugins only present them and never infer certainty independently.

```text
AniList airing schedule ──> confirmed / high / exact time
AniList media start date ─> reported / medium / exact date
Future prediction engine ─> estimated / scored / evidence-backed
```

This separation keeps factual source data, curated corrections, and future predictions auditable. Calendar, dashboard, account filtering, notifications, and APIs will consume the same intelligence fields.


## Personalization Layer

The `anime_calendar.personalization` package derives private views from immutable public releases. It owns identity and preference contracts, explainable filter decisions, and deterministic ranking. It does not own authentication sessions, passwords, database clients, or HTTP endpoints.

```text
Public Release Intelligence + Private User Preferences
                         |
                         v
              Personalization Engine
                         |
                         v
       Calendars / Dashboard / Notifications / API
```

External identity and persistence systems implement repository protocols at the adapter boundary. See ADR-0005 and `docs/PERSONALIZATION.md`.
