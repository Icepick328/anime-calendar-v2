# Upgrade to v0.6.3

1. Replace repository files while preserving `.git` and `.venv`.
2. Install development dependencies: `python -m pip install -e ".[dev]"`.
3. Run Ruff and pytest.
4. Apply `supabase/migrations/202607180002_personal_calendars.sql` only after the v0.6.2 migration.
5. Do not commit real Supabase credentials or plaintext feed tokens.
