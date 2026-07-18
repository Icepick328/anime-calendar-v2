# ADR-0009: Framework-Neutral Personal API

- Status: Accepted
- Date: 2026-07-18

## Decision

Expose private account use cases through a framework-neutral application service. HTTP frameworks and Supabase remain adapters.

## Consequences

Use cases can be tested without a server, reused by CLI or background jobs, and transported later through FastAPI without coupling domain code to request objects. Authentication context is explicit and owner checks happen before persistence calls, while Row-Level Security remains authoritative.
