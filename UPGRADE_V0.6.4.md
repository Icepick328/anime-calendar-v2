# Upgrade to v0.6.4

1. Replace repository files while preserving `.git` and `.venv`.
2. Install the editable development package.
3. Run Ruff and pytest.
4. Apply Supabase migrations in order, ending with `202607180003_watchlists_and_library.sql`.
5. Commit as `v0.6.4: add watchlists and library`.

No Supabase credentials are required for local tests or public calendar generation.
