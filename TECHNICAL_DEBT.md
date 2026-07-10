# Technical debt

## Known data limitations

- AniList media start dates do not represent every regional theatrical or streaming date.
- Date-only releases are intentionally all-day events because an exact time is unavailable.
- Entries with incomplete month/day values are skipped.
- The current model stores one canonical non-episode release per AniList title and release type. Regional theatrical and home-video releases require a future release-variant model.
- Streaming-provider resolution and dub release intelligence are planned for later releases.

## Planned improvements

- Add source/provenance and confidence fields to every release.
- Add regional release variants.
- Add theatrical, streaming, digital, and physical distribution stages.
- Persist normalized releases in a database for account filtering and personalized feeds.
