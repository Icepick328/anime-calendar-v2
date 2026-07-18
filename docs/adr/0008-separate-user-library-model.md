# ADR-0008: Separate User Library Model

- Status: Accepted
- Date: 2026-07-18

## Context

Watch state and progress are private, mutable user data. Public release intelligence is shared, source-derived data.

## Decision

Represent watchlists as separate `LibraryEntry` records keyed by owner and AniList ID. The personalization engine may consume library entries, but release objects never contain user state.

## Consequences

- Public release data remains immutable and cacheable.
- Multiple import providers can map to one domain contract.
- Row-Level Security cleanly protects private library records.
- Personalized calendars can explain library-based decisions.
