# ADR-0002: Model streaming providers as canonical records

- **Status:** Accepted
- **Date:** 2026-07-17
- **Decision owners:** Project maintainers

## Context

Raw provider names and URLs are inconsistent. Plain strings cannot preserve provider identity, region, language, evidence, confidence, watch URL, or future provider-specific capabilities.

## Decision

Represent legal availability with canonical `StreamingProvider` records. Normalize aliases and domains, preserve multiple providers, prioritize Crunchyroll for display when relevant, and retain evidence and confidence.

## Alternatives considered

### Store provider names as strings

Rejected because it cannot support reliable filtering, region handling, account preferences, or trust metadata.

### Hard-code one preferred provider

Rejected because Crunchyroll-first preference should influence ordering, not erase valid alternatives.

## Consequences

### Positive

- Enables provider-specific calendars and account preferences.
- Supports multiple services and future regions/languages.
- Keeps provider confidence separate from release-date confidence.

### Negative or costly

- Requires normalization and curated knowledge maintenance.
- Availability can remain region-dependent and incomplete.

## Revisit conditions

Revisit if a stable official provider standard replaces the need for project normalization.
