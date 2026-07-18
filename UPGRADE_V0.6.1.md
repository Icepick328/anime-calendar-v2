# Upgrade to v0.6.1

This is a source-compatible foundation release. It does not require credentials, database setup, or configuration changes.

## Windows PowerShell

1. Preserve local work:

   ```powershell
   git status
   git push
   ```

2. Copy the contents of the v0.6.1 snapshot over the repository root. Keep `.git` and `.venv`.

3. Refresh and validate:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\.venv\Scripts\Activate.ps1
   python -m pip install -e ".[dev]"
   python -m ruff check .
   python -m pytest
   python -m anime_calendar
   ```

Expected test result: `26 passed`.

4. Commit:

   ```powershell
   git add .
   git commit -m "v0.6.1: add personalization foundation"
   git push
   ```
