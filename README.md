# Anime Calendar v2

Anime Calendar v2 generates Apple Calendar-compatible anime release feeds from AniList.

Version 0.3.0 expands the generator beyond TV episodes to include movies, OVAs, ONAs, specials, TV shorts, and music anime.

## Generated calendars

Running the application creates:

- `output/anime_calendar.ics` — backward-compatible combined feed
- `output/all_releases.ics` — all supported releases
- `output/episodes.ics` — episode airings
- `output/movies.ics` — anime movie premieres
- `output/specials.ics` — OVAs, ONAs, specials, TV shorts, and music anime

## Release behavior

- Episodes use AniList's precise airing timestamps and become timed events.
- Movies and other one-off releases use AniList start dates and become all-day events.
- Entries with incomplete dates are omitted instead of being assigned invented dates.
- Duplicate media-start events are suppressed when AniList also provides an episode premiere on the same date.
- Stable event identifiers allow future calendar runs to update existing subscribed events.

## Rich metadata

Calendar notes can include:

- English, Romaji, and native titles
- Synopsis
- Genres and studios
- Season and year
- Format, status, and source material
- Episode count and duration
- AniList score
- Poster, banner, trailer, AniList, and official links
- Premiere and finale labels when known

## Requirements

- Python 3.12 or newer
- Git

## Install on Windows

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

## Test

```powershell
python -m ruff check .
python -m pytest
```

Expected result for v0.3.0:

```text
8 passed
```

## Configuration

Edit `config.json` to control:

- Calendar name
- Look-ahead period
- Episode and media pagination
- Event duration
- Output directory
- Request timeout
- Included non-episode AniList formats

## Artwork compatibility

Poster URLs are stored in event descriptions and as URI attachments. Calendar applications vary in whether remote images render inline, but the URLs remain accessible from the event.

## Documentation

- `docs/ARCHITECTURE.md`
- `ROADMAP.md`
- `TECHNICAL_DEBT.md`
- `CHANGELOG.md`
