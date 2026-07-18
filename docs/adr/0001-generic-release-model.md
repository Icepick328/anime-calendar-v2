# ADR-0001: Use a generic Release model

- **Status:** Accepted
- **Date:** 2026-07-17
- **Decision owners:** Project maintainers

## Context

The original prototype represented all schedule data as episodes. That model could not accurately express movies, OVAs, ONAs, specials, all-day dates, theatrical premieres, future streaming releases, or multiple versions.

## Decision

Use a canonical `Release` domain model that represents episodic and non-episodic availability records. Episode number is optional. Release type, date precision, version, lifecycle, confidence, and evidence are explicit fields.

## Alternatives considered

### Episode-only model

Rejected because non-episodic media would require misleading fake episode fields and repeated special cases.

### Separate unrelated models per format

Rejected because output engines, filtering, accounts, and notifications need one reusable release contract.

## Consequences

### Positive

- Supports episodes, movies, OVAs, ONAs, specials, and future formats.
- Allows common filtering and output generation.
- Makes accounts and personalized feeds additive rather than a rewrite.

### Negative or costly

- Requires optional fields and validation rules.
- Source ingestion must normalize heterogeneous upstream data.

### Follow-up

- Maintain model invariants through tests.
- Add migrations if the model is later persisted in a database.

## Revisit conditions

Revisit only if a release category cannot be represented without widespread ambiguity or if independent lifecycle models become operationally necessary.
