# ADR-0004: Separate public release data from private user data

- **Status:** Accepted
- **Date:** 2026-07-17
- **Decision owners:** Project maintainers

## Context

v0.6 introduces accounts and preferences. Public anime metadata has different ownership, security, retention, and access requirements than private profiles, saved titles, filters, and calendar tokens.

## Decision

Keep canonical public release data and private account data in separate logical domains. Authentication and private records will use a dedicated backend with Row-Level Security. The generator remains independently runnable and account-agnostic. Personalized services filter canonical releases rather than modifying the ingestion engine.

## Alternatives considered

### Embed account logic in the generator

Rejected because it couples public ingestion to authentication, complicates testing, and risks exposing private data.

### Store user preferences in repository files

Rejected because repositories and GitHub Pages are not suitable secure multi-user backends.

## Consequences

### Positive

- Accounts can be added without rewriting the generator.
- Security boundaries and data ownership are clearer.
- Public calendars can remain static while private feeds become dynamic.

### Negative or costly

- Requires backend infrastructure and database migrations.
- Deployment becomes hybrid rather than GitHub-only.

### Follow-up

- Define Supabase schema, RLS policies, token model, export, and deletion flows in v0.6.
- Never expose service-role credentials or raw private feed tokens.

## Revisit conditions

Revisit if infrastructure changes, but preserve the separation principle regardless of vendor.
