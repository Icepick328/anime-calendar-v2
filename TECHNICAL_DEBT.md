# Technical debt

## Known data limitations

- AniList media start dates do not represent every regional theatrical or streaming date.
- Date-only releases are intentionally all-day events because an exact time is unavailable.
- Entries with incomplete month/day values are skipped.
- Provider availability may vary by region even when a global provider link exists.
- AniList external links do not consistently include subtitle languages, dub languages, or simulcast status.
- Curated provider knowledge is currently repository-managed JSON rather than a database.
- The model stores one canonical non-episode release per AniList title and release type. Regional theatrical and home-video releases require a future release-variant model.

## Conscious decisions

- Unknown streaming availability is not guessed.
- Crunchyroll-first means display priority, not automatic classification.
- Empty provider calendars remain valid feeds.
- Provider confidence applies to availability evidence, not release timing.

## Planned improvements

- Add regional release variants.
- Add theatrical, streaming, digital, and physical distribution stages.
- Add source URLs and review metadata to curated knowledge records.
- Add confirmed versus predicted dub-release objects.
- Persist normalized releases in a database for account filtering and personalized feeds.
