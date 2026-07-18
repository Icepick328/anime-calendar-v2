# Changelog

## 0.6.2 - 2026-07-18

### Added
- Supabase-ready authentication and PostgREST adapters.
- Versioned PostgreSQL migration with Row-Level Security.
- Account export and application-data deletion contracts.
- Identity/persistence security documentation and ADR-0006.
- Adapter serialization, configuration, repository, and authentication tests.


## [0.6.1] - 2026-07-17

### Added

- Personalization domain package with immutable identity, profile, preference, and personal-calendar models.
- Authentication-agnostic repository protocols for identity and preference persistence.
- Deterministic filtering and ranking engine with explainable decision reasons.
- ADR-0005 defining the public/private data boundary.
- Personalization architecture documentation and twelve focused tests.

### Architecture

- Public release intelligence remains account-independent and immutable.
- Hosted authentication and storage are deferred to adapters in later v0.6 releases.

## 0.5.1 — Project Constitution

- Add project foundation and mission documents.
- Add product values, scope boundaries, north star, and success criteria.
- Add project charter and maintainer-led governance model.
- Add formal release process and engineering, documentation, product, and operational quality gates.
- Add contributor standards and architecture-change requirements.
- Add project-specific code of conduct.
- Add brand voice, canonical terminology, and uncertainty language.
- Add Architecture Decision Record template and four initial accepted ADRs.
- Expand architecture documentation with engine philosophy and public/private data separation.
- Commit v0.6.0 accounts and preferences as the next planned capability.
- Preserve the v0.5.0 runtime and fourteen-test baseline.


## 0.5.0 — Release Intelligence Foundation

- Add confirmed, reported, estimated, and unknown date states.
- Add release-specific confidence levels independent of provider confidence.
- Add exact-time and exact-date precision metadata.
- Add original, sub, dub, and unknown release variants.
- Add scheduled, released, delayed, cancelled, and unknown lifecycle states.
- Add structured release evidence with source names, URLs, and notes.
- Classify AniList airing timestamps as confirmed/high-confidence records.
- Classify AniList media start dates as reported/medium-confidence records.
- Add Release Intelligence and Evidence sections to calendar notes.
- Prefix estimated event summaries clearly when predictions are eventually added.
- Add confirmed, reported, and estimated calendar feeds.
- Prefer the highest-confidence duplicate when merging release sources.
- Expand automated coverage to fourteen tests.

## 0.4.0 — Streaming Intelligence Engine

- Add canonical streaming-provider records.
- Add provider normalization and curated knowledge.
- Add Crunchyroll-first ordering and provider-specific feeds.
- Add streaming evidence and confidence metadata.

## 0.3.0 — Universal Anime Release Generator

- Add movies, OVAs, ONAs, specials, TV shorts, and music anime.
- Add generic release model and multiple calendar feeds.

## 0.2.0 — Metadata Engine

- Add rich anime metadata and calendar descriptions.

## 0.1.0 — Foundation

- Add AniList ingestion, ICS generation, tests, logging, and CI.

## [0.6.3] - 2026-07-18

### Added
- Personal calendar definitions and preference-driven ICS generation.
- Hashed private feed credentials and Supabase persistence.
- Personal calendar migration, RLS policies, documentation, ADR, and tests.
