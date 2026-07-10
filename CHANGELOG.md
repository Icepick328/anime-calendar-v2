# Changelog

## 0.3.0 — Universal Release Generator

- Replace the episode-only domain object with a generic `Release` model.
- Add first-class release types for episodes, movies, OVAs, ONAs, specials, TV shorts, and music anime.
- Add a second AniList ingestion path for media start dates.
- Preserve exact episode timestamps while representing date-only releases as all-day calendar events.
- Generate combined, episode-only, movie-only, and specials calendar feeds.
- Add cross-source deduplication and stable release identifiers.
- Expand automated tests and CI artifact validation.

## 0.2.0 — Rich Metadata Engine

- Add synopsis, artwork, studios, season data, scores, trailers, and external links.
- Add premiere and finale labels.
- Enrich Apple Calendar event descriptions.

## 0.1.0 — Foundation

- Add AniList schedule ingestion, typed models, ICS generation, tests, linting, and CI.
