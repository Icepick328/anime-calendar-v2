# Architecture

## Pipeline

```text
AniList episode schedule ─┐
                         ├─> Transformers ─> Canonical Release objects ─> Filters ─> Outputs
AniList media start dates ┘                                             ├─ ICS feeds
                                                                        ├─ dashboard (future)
                                                                        └─ API (future)
```

## Canonical release model

`Release` is the central domain object. It represents both timed episode airings and date-only media releases.

- Episode releases use timezone-aware datetimes from AniList `AiringSchedule`.
- Movies and other one-off formats use AniList `Media.startDate`.
- Incomplete start dates are omitted rather than assigned invented dates.
- Date-only releases become all-day iCalendar events.
- Stable keys prevent duplicates and allow subscribed calendars to update existing events.

## Supported release types

- Episode
- Movie
- OVA
- ONA
- Special
- TV short
- Music anime
- Other future formats

## Output feeds

- `anime_calendar.ics` — backward-compatible combined feed
- `all_releases.ics` — combined feed
- `episodes.ics` — timed episode releases
- `movies.ics` — movie premieres
- `specials.ics` — OVAs, ONAs, specials, shorts, and music anime

## Account readiness

Future user filters operate on canonical fields such as release type, genres, providers, language, date, and AniList ID. Calendar generation accepts already-filtered `Release` objects, so accounts can be added without rewriting ingestion or ICS formatting.
