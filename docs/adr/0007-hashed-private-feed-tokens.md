# ADR-0007: Hashed private feed tokens

- **Status:** Accepted
- **Date:** 2026-07-18

## Context

Calendar clients need a stable subscription URL but generally cannot send an interactive login token on every refresh.

## Decision

Use high-entropy bearer tokens for unlisted personal feeds. Persist only a SHA-256 hash, reveal plaintext only when issued, and permit token rotation. Private calendars are not token-resolvable until explicitly changed to `unlisted`.

## Consequences

A leaked URL grants feed access until rotation, so feed URLs must be treated as secrets. Database disclosure does not reveal usable plaintext feed credentials. Fully private interactive access remains authenticated through Supabase JWTs and RLS.
