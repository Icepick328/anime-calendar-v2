# Upgrade to v0.6.2

1. Replace repository files while preserving `.git` and `.venv`.
2. Run `python -m pip install -e ".[dev]"`.
3. Run `python -m ruff check .` and `python -m pytest`.
4. Do not create a Supabase project until you are ready to test live authentication.
5. When ready, review `supabase/README.md` and the migration before applying it.

No environment variables are required for the existing public calendar generator or unit tests.
