# Anime Calendar v2

Anime Calendar v2 is a streaming-aware anime release generator. It combines AniList episode schedules and media start dates into Apple Calendar-compatible feeds for episodes, movies, OVAs, ONAs, specials, TV shorts, and music anime.

Version **0.4.0** adds the Streaming Intelligence Engine: canonical provider records, Crunchyroll-first ordering, confidence and evidence metadata, provider-specific calendars, and a curated knowledge package.

## Generated calendars

Running the application creates:

- `output/anime_calendar.ics` — backward-compatible combined feed
- `output/all_releases.ics` — all supported releases
- `output/episodes.ics` — episode airings
- `output/movies.ics` — anime movie premieres
- `output/specials.ics` — OVAs, ONAs, specials, TV shorts, and music anime
- `output/streaming_confirmed.ics` — releases with at least one resolved provider
- `output/crunchyroll.ics` — releases resolved to Crunchyroll
- `output/hidive.ics` — releases resolved to HIDIVE

Empty provider feeds are valid calendars. They mean no matching provider was confirmed in the current data window.

## Streaming intelligence

Provider records include:

- Canonical provider ID and display name
- Direct watch URL when available
- Confidence: verified, high, medium, low, or unknown
- Evidence: official streaming link, external link, or curated knowledge
- Optional regions
- Optional subtitle and dub languages
- Optional simulcast status

Official AniList links marked as streaming are treated as verified. Recognized provider links without that marker are high confidence. Curated records can supplement missing structured data without pretending that unknown availability is confirmed.

Crunchyroll is ordered first when multiple providers are available, matching this project's Crunchyroll-first preference while retaining every resolved provider.

## Release behavior

- Episodes use precise AniList airing timestamps and become timed events.
- Movies and other one-off releases use AniList start dates and become all-day events.
- Entries with incomplete dates are omitted instead of receiving invented dates.
- Duplicate media-start events are suppressed when an episode premiere exists on the same date.
- Stable event identifiers allow future calendar runs to update existing subscribed events.

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

Expected result for v0.4.0:

```text
11 passed
```

## Curated provider knowledge

Provider definitions live in:

```text
src/anime_calendar/knowledge/providers.json
```

Per-title curated records live in:

```text
src/anime_calendar/knowledge/anime_streaming.json
```

See `docs/STREAMING_KNOWLEDGE.md` before adding records.

## Artwork compatibility

Poster URLs are stored in event descriptions and as URI attachments. Calendar applications vary in whether remote images render inline, but the URLs remain accessible from the event.

## Documentation

- `docs/ARCHITECTURE.md`
- `docs/STREAMING_KNOWLEDGE.md`
- `ROADMAP.md`
- `TECHNICAL_DEBT.md`
- `CHANGELOG.md`
