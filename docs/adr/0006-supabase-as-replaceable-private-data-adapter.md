# ADR-0006: Use Supabase as a Replaceable Private-Data Adapter

- **Status:** Accepted
- **Date:** 2026-07-18

## Context

v0.6.2 needs authenticated persistence, PostgreSQL migrations, and Row-Level Security without coupling the personalization domain to one vendor SDK.

## Decision

Use Supabase Auth and PostgREST as the first infrastructure adapter. Domain code depends only on authentication and repository protocols. The adapter uses the anonymous project key plus each user's verified JWT, preserving Row-Level Security. Service-role credentials are forbidden in clients and local configuration committed to Git.

## Consequences

- Authentication and persistence can be tested without a live backend.
- Supabase may later be replaced without rewriting personalization rules.
- SQL migrations and RLS policies become version-controlled release artifacts.
- Administrative actions, including final deletion of an Auth user, require a trusted server-side endpoint.
