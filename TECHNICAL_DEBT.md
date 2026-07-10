# Technical Debt

## Open items

- AniList media start dates do not identify region, theatrical market, or streaming availability; they remain `reported`, not `confirmed`.
- The generator currently omits partial dates instead of preserving year-only or month-only records.
- No official delay or cancellation source is integrated yet.
- No dub-date prediction is implemented. The estimated feed is intentionally empty.
- Release lifecycle is derived from the current date unless an explicit delayed or cancelled state is supplied.
- Provider region and language coverage is incomplete and depends on structured links or curated knowledge.
- Remote poster rendering varies between calendar clients.

## Accepted design choices

- Accuracy is preferred over calendar completeness.
- Unknown information remains unknown.
- Episode timestamps and date-only media releases remain distinct precision classes.
- Provider confidence and release-date confidence are separate concepts.
