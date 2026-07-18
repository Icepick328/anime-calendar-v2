# ADR-0003: Preserve confidence and evidence

- **Status:** Accepted
- **Date:** 2026-07-17
- **Decision owners:** Project maintainers

## Context

Anime release and streaming data varies in certainty. Treating every upstream date or provider link as equally authoritative would mislead users and make future predictions indistinguishable from confirmed facts.

## Decision

Important release and provider claims carry explicit status, confidence, and evidence. Confirmed, reported, estimated, and unknown states remain distinct. Predictions must be visibly labeled and must not overwrite stronger facts.

## Alternatives considered

### Boolean confirmed flag

Rejected because it cannot distinguish reported, inferred, estimated, and unknown information.

### Hide uncertainty from outputs

Rejected because apparent simplicity would reduce trust and make errors harder to diagnose.

## Consequences

### Positive

- Users can judge reliability.
- Multiple sources can be merged without losing provenance.
- Dub and movie-streaming predictions can be added responsibly.

### Negative or costly

- Models and interfaces are more detailed.
- Contributors must provide sources and choose confidence carefully.

## Revisit conditions

Confidence vocabulary may be refined if calibrated models or user research demonstrate a clearer representation.
