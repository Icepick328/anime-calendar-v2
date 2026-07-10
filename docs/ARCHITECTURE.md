# Architecture

Anime Calendar v2 is organized as a metadata pipeline with replaceable input and output layers.

```text
AniList airing schedule
        |
        v
Provider layer
        |
        v
Metadata transformation
        |
        v
Typed domain model
        |
        v
Output builders
```

## Provider layer

`providers/anilist.py` is responsible only for retrieving public schedule and media metadata. It does not decide how the data should be displayed or classified.

## Metadata engine

`services/transformer.py` normalizes provider-specific dictionaries into typed models. It cleans descriptions, selects preferred titles and artwork, normalizes studios, trailers, and external links, and removes duplicate releases.

## Domain model

`models.py` is the stable internal contract used by all future engines and outputs. Sprint 2 adds rich metadata while keeping release scheduling separate from anime-level information.

Key objects:

- `Anime`: normalized series metadata.
- `EpisodeRelease`: an episode number and release timestamp associated with an anime.
- `ExternalLink`: a typed external destination.
- `Trailer`: normalized trailer information and canonical URL generation.
- `ReleaseLabel`: episode, season premiere, or season finale.

## Calendar output

`calendars/ics_builder.py` converts domain objects to iCalendar events. It owns calendar-specific concerns such as stable UIDs, event summaries, descriptions, categories, timestamps, and poster attachments.

## Future engines

The internal model is intentionally provider-neutral so future services can enrich the same objects without rewriting the calendar builder:

- Platform intelligence
- Confirmed dub tracking
- Artwork processing
- HTML dashboard
- RSS and notification outputs
