# Anime Calendar v2

Anime Calendar v2 is a streaming-aware anime release intelligence engine. It combines AniList episode schedules and media start dates into Apple Calendar-compatible feeds for episodes, movies, OVAs, ONAs, specials, TV shorts, and music anime.

Version **0.5.1** establishes the Project Constitution while preserving the v0.5.0 Release Intelligence engine: explicit date status, confidence, precision, version, lifecycle, and evidence. The generator distinguishes confirmed episode timestamps from reported movie and special dates instead of presenting every upstream date with the same certainty.

## Generated calendars

Running the application creates:

- `output/anime_calendar.ics` — backward-compatible combined feed
- `output/all_releases.ics` — all supported releases
- `output/episodes.ics` — episode airings
- `output/movies.ics` — anime movie premieres
- `output/specials.ics` — OVAs, ONAs, specials, TV shorts, and music anime
- `output/streaming_confirmed.ics` — releases with a resolved provider
- `output/crunchyroll.ics` — releases resolved to Crunchyroll
- `output/hidive.ics` — releases resolved to HIDIVE
- `output/confirmed_releases.ics` — precise confirmed dates
- `output/reported_releases.ics` — upstream dates that remain context-dependent
- `output/estimated_releases.ics` — transparent future predictions; intentionally empty today

Empty feeds are valid calendars and communicate that no matching records were available in the current window.

## Release intelligence

Each release can include:

- Date status: confirmed, reported, estimated, or unknown
- Confidence: verified, high, medium, low, or unknown
- Precision: exact time, exact date, partial date, or unknown
- Version: original, sub, dub, or unknown
- Lifecycle: scheduled, released, delayed, cancelled, or unknown
- Evidence records explaining the source of the date

Current rules are deliberately conservative:

- AniList airing schedules become confirmed, high-confidence, exact-time episode records.
- AniList media start dates become reported, medium-confidence, exact-date records.
- No dub date or movie streaming date is predicted in v0.5.0.

Calendar notes include a Release Intelligence section and supporting evidence.

## Streaming intelligence

Provider records include canonical identity, watch URL, confidence, evidence, optional regions, languages, and simulcast status. Crunchyroll is prioritized for display without discarding other confirmed providers.

## Release behavior

- Episodes use precise timezone-aware airing timestamps.
- Movies and other one-off releases use all-day dates when only a date is available.
- Incomplete dates are omitted instead of receiving invented values.
- Media-start duplicates are suppressed when an episode premiere exists on the same date.
- Stable event identifiers allow subscribed calendars to update existing events.

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

Expected result for v0.6.1:

```text
14 passed
```

## Documentation

- `FOUNDATION.md`
- `MISSION.md`
- `PROJECT_CHARTER.md`
- `RELEASE_PROCESS.md`
- `BRAND.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `docs/ARCHITECTURE.md`
- `docs/adr/`
- `docs/STREAMING_KNOWLEDGE.md`
- `docs/RELEASE_INTELLIGENCE.md`
- `ROADMAP.md`
- `TECHNICAL_DEBT.md`
- `CHANGELOG.md`


## Personalization Foundation

Version 0.6.1 introduces account-independent domain contracts and an explainable personalization engine. Public release data remains immutable; private preferences produce derived inclusion and ranking decisions. Authentication and hosted persistence are intentionally deferred to adapter-based milestones. See `docs/PERSONALIZATION.md`.
