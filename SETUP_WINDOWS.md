# Windows Setup and v0.5.1 Upgrade

## Upgrade an existing repository

1. Commit and push the current version.
2. Extract the v0.5.1 snapshot.
3. Copy everything inside the extracted folder into the repository root.
4. Replace destination files when prompted.
5. Do not delete `.git` or `.venv`.

Activate and refresh the project:

```powershell
cd $HOME\Documents\GitHub\anime-calendar-v2
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Validate:

```powershell
python -m ruff check .
python -m pytest
python -m anime_calendar
```

Expected test result:

```text
14 passed
```

Commit:

```powershell
git status
git add .
git commit -m "v0.5.1: add project constitution"
git push
```
