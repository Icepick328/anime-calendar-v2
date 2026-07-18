# Roadmap

> **Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

The roadmap communicates intent, not guarantees. Scope may change when evidence, security, maintainability, or user value argues for a better sequence.

## Completed foundations

### v0.1.0 — Foundation

AniList ingestion, canonical package structure, ICS output, logging, tests, and continuous integration.

### v0.2.0 — Metadata Engine

Rich title metadata, synopsis, genres, studios, artwork, trailers, season information, and calendar descriptions.

### v0.3.0 — Universal Release Generator

Episodes, movies, OVAs, ONAs, specials, TV shorts, music anime, mixed date precision, duplicate suppression, and multiple feeds.

### v0.4.0 — Streaming Intelligence

Canonical streaming-provider records, provider normalization, evidence, confidence, curated knowledge, and provider-specific feeds.

### v0.5.0 — Release Intelligence Foundation

Confirmed, reported, estimated, and unknown dates; confidence; precision; version; lifecycle; evidence; and intelligence-specific feeds.

### v0.5.1 — Project Constitution

Mission, foundation, governance, contributor standards, release process, brand voice, quality gates, and architecture decision records.

## Next release

### v0.6.0 — Accounts and Preferences

**Capability:** Answer “What do I care about?”

Planned scope:

- Supabase-backed authentication architecture;
- email account creation, verification, sign-in, reset, and deletion;
- user profiles and timezone preferences;
- genre include/exclude rules;
- release-type preferences;
- preferred and hidden streaming providers;
- saved, favorite, hidden, watching, and plan-to-watch anime states;
- database migrations and Row-Level Security policies;
- separation between public release data and private user data;
- export and deletion foundations;
- security documentation and tests.

Accounts will not require rewriting the generator. The account layer filters canonical releases produced by the existing engine.

## Planned releases

### v0.7.0 — Personalized Calendar Feeds

**Capability:** Deliver “My releases.”

- revocable private feed tokens;
- multiple named calendar profiles;
- watchlist-only, genre, provider, format, sub, dub, and movie feeds;
- secure dynamic ICS endpoints;
- token rotation and audit-safe logging.

### v0.8.0 — Personalized Dashboard

**Capability:** Visualize what matters now.

- upcoming personalized releases;
- search and saved anime management;
- calendar-profile management;
- evidence and confidence presentation;
- accessible, responsive interface.

### v0.9.0 — Prediction and Notification Engines

**Capability:** Explain what may happen next and notify responsibly.

- transparent dub estimates;
- theatrical-to-streaming lifecycle modeling;
- schedule-delay detection;
- email, Discord, RSS, and webhook outputs;
- confidence thresholds and user-controlled notification rules.

### v1.0.0 — Public Launch

**Capability:** A stable, trustworthy public product.

Quality bar:

- stable deployment and migration process;
- comprehensive automated testing;
- privacy and security review;
- user export and deletion flows;
- complete user and contributor documentation;
- accessibility review;
- performance targets for large release datasets;
- operational monitoring and incident guidance;
- clear support and governance expectations.

## Beyond v1.0

Potential directions include AniList account sync, Sign in with Apple, mobile clients, public API access, recommendation and “Anime DNA” features, localization, regional theatrical tracking, Home Assistant integration, and community-maintained knowledge contributions.

These are exploratory until promoted into a scheduled release.
