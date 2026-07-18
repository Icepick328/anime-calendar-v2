# Personal API

Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.

`PersonalApiService` is a framework-neutral application layer for authenticated private operations. It exposes profiles, preferences, personal calendars, feed-token rotation, library records, account export, and application-data deletion while delegating authorization to an authenticated context and persistence adapters.

## Boundary

The service contains use-case orchestration only. It does not parse HTTP, issue JWTs, own database credentials, or depend on FastAPI, Flask, or Supabase. A future transport can map HTTP requests to these methods without moving domain rules into controllers.

## Security

Every mutating operation derives ownership from `PersonalApiContext.user_id`. Caller-supplied owner IDs are validated and Supabase Row-Level Security remains the final enforcement layer. Plaintext feed tokens are returned only at issuance; repositories receive only hashes.
