# Supabase setup for v0.6.2

This directory contains reviewed, versioned SQL for the private account domain.

1. Create a Supabase project.
2. Install and authenticate the Supabase CLI.
3. Link the local repository to the project.
4. Review the migration.
5. Run `supabase db push`.
6. Set `SUPABASE_URL` and `SUPABASE_ANON_KEY` locally.

Never commit the service-role key. The Python adapters use the anonymous project key plus the authenticated user's JWT so Row-Level Security remains active.

The included deletion RPC removes application-owned private records. Deleting the corresponding `auth.users` record requires a trusted server-side endpoint and is intentionally not performed by the client adapter.
