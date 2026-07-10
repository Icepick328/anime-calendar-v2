# Architecture

The application follows a small pipeline:

1. `providers/anilist.py` fetches raw schedule records.
2. `services/transformer.py` converts raw records into typed domain models.
3. `calendars/ics_builder.py` creates and writes the iCalendar feed.
4. `main.py` coordinates configuration, logging, error handling, and output.

The provider, transformation, and output layers are intentionally separated so streaming enrichment and dub tracking can be added without rewriting the core schedule pipeline.
