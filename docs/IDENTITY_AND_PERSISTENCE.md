# Identity and Persistence

Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.

v0.6.2 adds the first real private-data infrastructure boundary.

## Security model

1. A client receives a Supabase access token through an approved sign-in flow.
2. `SupabaseAuthProvider` validates the token against Supabase Auth.
3. Repository adapters send the anonymous project key and that user token.
4. PostgreSQL Row-Level Security verifies `auth.uid() = user_id`.
5. The domain layer never trusts a user ID supplied without an authenticated context.

## Data ownership

Private account tables are owned by the authenticated user. Public anime and release intelligence remain account-independent. Private records cascade from `account_identities` and can be exported before deletion.

## Secrets

Safe in a public client: `SUPABASE_URL`, `SUPABASE_ANON_KEY`.

Never expose: service-role keys, database passwords, private feed tokens, refresh tokens, or raw access tokens in logs.

## Current scope

This release provides contracts, adapters, migration SQL, export, and application-data deletion. It does not ship a login UI or a trusted administrative endpoint for deleting the Supabase Auth user. Those arrive in later application/API work.
