# Sprint 1 installation on Windows

## 1. Copy the snapshot

Extract the ZIP. Copy all files and folders from `anime-calendar-v2-sprint1` into:

```text
C:\Users\Brad\Documents\GitHub\anime-calendar-v2
```

The destination repository should contain `pyproject.toml`, `src`, `tests`, and the other files at its top level.

## 2. Create and activate the virtual environment

```powershell
cd $HOME\Documents\GitHub\anime-calendar-v2
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 3. Install Sprint 1

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## 4. Verify the code

```powershell
python -m ruff check .
python -m pytest
```

Expected test result:

```text
2 passed
```

## 5. Generate the calendar

```powershell
python -m anime_calendar
```

Expected file:

```text
output\anime_calendar.ics
```

## 6. Commit and push

```powershell
git add .
git commit -m "Sprint 1: establish Anime Calendar v2 foundation"
git push -u origin main
```

If Git asks you to identify yourself, run:

```powershell
git config --global user.name "Icepick328"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

Then repeat the commit command.
