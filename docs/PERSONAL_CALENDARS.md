# Personal Calendar Engine

**Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

v0.6.3 turns a public release set into a user-specific ICS feed without modifying canonical release data.

## Security model

Feed credentials are random bearer tokens. Only a SHA-256 hash is persisted. The plaintext token is shown once when issued and should be rotated after suspected exposure. Personal calendars are private by default; token resolution only returns enabled calendars explicitly marked `unlisted`.

Authenticated management operations continue to use the anonymous Supabase key, the user's JWT, and Row-Level Security. Public feed resolution is narrowly limited to the token-resolution function.

## Generation flow

1. Load a personal calendar definition.
2. Load the owner's preferences.
3. Evaluate canonical releases with the personalization engine.
4. Generate an ICS calendar from included releases.
5. Return the calendar without mutating public release objects.

A future HTTP delivery layer will expose these generated feeds through stable subscription URLs.
