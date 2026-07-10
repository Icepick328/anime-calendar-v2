# Anime Calendar v2

Anime Calendar v2 generates an Apple Calendar-compatible `.ics` feed from AniList's upcoming airing schedule.

## Sprint 1 features

- AniList GraphQL schedule provider
- Configurable look-ahead window
- Typed anime and episode models
- Duplicate protection
- Stable event UIDs for subscribed calendars
- Apple Calendar-compatible ICS output
- Logging and graceful error handling
- Automated tests

## Requirements

- Python 3.12 or newer
- Git

## Windows setup

From PowerShell in the repository folder:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run

```powershell
python -m anime_calendar
```

Expected result:

```text
output/anime_calendar.ics
```

## Test

```powershell
python -m pytest
```

## Configuration

Edit `config.json` to change the calendar name, look-ahead period, pagination, event duration, output path, or request timeout.

## Sprint roadmap

1. Core AniList-to-ICS engine
2. Rich event metadata and formatting
3. Crunchyroll-first platform intelligence
4. Confirmed dub tracking and separate SUB/DUB calendars
5. GitHub Actions and GitHub Pages publishing
6. HTML dashboard and notifications
