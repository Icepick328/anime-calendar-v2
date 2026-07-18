# ADR-0005: Derive Personal Views Without Mutating Public Releases

- **Status:** Accepted
- **Date:** 2026-07-17

## Context

Anime Calendar now needs user identity, preferences, personal calendars, and future watchlists. The public release intelligence engine must remain reusable and trustworthy regardless of whether accounts are enabled.

## Decision

Personalization is a separate domain layer. Public `Anime` and `Release` objects contain no user identifiers or private preference data. The personalization engine accepts immutable releases plus private user preferences and returns derived inclusion decisions and ranking scores.

Persistence is defined through repository protocols. A future Supabase adapter may implement those protocols without making the core domain depend on Supabase.

## Consequences

- Public calendar generation remains deterministic and account-independent.
- Private data can receive stronger security, retention, deletion, and export rules.
- Tests can exercise personalization without network services.
- Dashboards, calendars, notifications, and APIs can reuse the same decisions.
- Authentication and storage integrations remain replaceable adapters.

## Alternatives Rejected

### Add user fields to `Release`

Rejected because it mixes public facts with private state, duplicates releases per user, and creates privacy risks.

### Make Supabase types the domain model

Rejected because it would couple business rules to one hosted service and make local testing harder.
