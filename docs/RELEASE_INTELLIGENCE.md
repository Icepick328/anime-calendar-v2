# Release Intelligence

Version 0.5.0 introduces explicit release intelligence. Calendar dates are no longer treated as equally certain merely because they exist.

## Date status

- `confirmed` — a precise scheduled airing supplied by AniList's airing schedule.
- `reported` — a date listed in upstream media metadata, but without enough context to claim an official regional or streaming release.
- `estimated` — a future prediction. Version 0.5.0 defines this state but does not generate predictions.
- `unknown` — no dependable classification is available.

## Confidence

Release confidence is independent from streaming-provider confidence:

- `verified`
- `high`
- `medium`
- `low`
- `unknown`

Current mappings:

- AniList episode airing timestamp: `confirmed` / `high`
- AniList media start date: `reported` / `medium`

## Precision

- `exact_time` — a timezone-aware timestamp.
- `exact_date` — an all-day date with no invented time.
- `partial_date` — reserved for future use.
- `unknown` — no usable precision.

## Version

The model can distinguish:

- original
- sub
- dub
- unknown

Current AniList-derived records are marked `original`. No dub dates are generated in v0.5.0.

## Evidence

Every enriched release can retain evidence records containing:

- Evidence type
- Human-readable source name
- Source URL
- An explanatory note

This makes future predictions auditable and allows calendars, dashboards, and APIs to explain why a date is believed.

## Lifecycle

The engine reports scheduled or released based on the current date. Explicit delayed and cancelled states are reserved for future official or curated evidence.

## Calendar feeds

Version 0.5.0 adds:

- `confirmed_releases.ics`
- `reported_releases.ics`
- `estimated_releases.ics`

The estimated feed is intentionally empty until a transparent prediction engine is implemented.
