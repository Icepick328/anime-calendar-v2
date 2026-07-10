# Anime Calendar v2

Anime Calendar v2 generates a rich Apple Calendar-compatible `.ics` feed from AniList's upcoming airing schedule.

## Version 0.2 features

- AniList GraphQL schedule and metadata provider
- Configurable look-ahead window
- Typed anime, release, link, and trailer models
- Duplicate protection
- Stable event UIDs for subscribed calendars
- Rich event notes containing:
  - English, Romaji, and native titles
  - Synopsis
  - Genres and studios
  - Season and year
  - Format, status, and source
  - Episode count and duration
  - AniList score
  - Poster, banner, trailer, and official links
- Season premiere and finale labels when episode totals are known
- Poster URL attached to ICS events where supported
- Logging, graceful error handling, linting, tests, and CI artifacts

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
python -m ruff check .
python -m pytest
```

## Configuration

Edit `config.json` to change the calendar name, look-ahead period, pagination, event duration, output path, or request timeout.

## Artwork compatibility

The calendar stores poster URLs in event notes and as URI attachments. Calendar applications vary in whether they render remote images inline. Apple Calendar will always retain the URL, but visual presentation can differ by macOS/iOS version and account type.

## Roadmap

1. Core AniList-to-ICS engine
2. Rich metadata engine
3. Crunchyroll-first platform intelligence
4. Confirmed dub tracking and separate SUB/DUB calendars
5. GitHub Pages publishing
6. HTML dashboard and notifications
