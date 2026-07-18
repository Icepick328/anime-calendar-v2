# Watchlists and Library

**Anime Calendar v2 is an open-source Anime Release Intelligence Platform.**

v0.6.4 introduces a private user library as an independent personalization signal.

## Watch states

- `watching`
- `plan_to_watch`
- `completed`
- `on_hold`
- `dropped`

Each entry is keyed by owner and AniList ID and may store episode progress, a 0–100 score, and private notes.

## Calendar behavior

Library filters can restrict calendars to selected watch states, hide episodes at or below recorded progress, and decide whether series absent from the library remain eligible. Watching and planned series receive deterministic ranking boosts, while the public `Release` model is never modified.

## Privacy

Library rows are private account data. Supabase Row-Level Security requires `auth.uid() = owner_id` for every read and write. Deleting an account cascades through its library entries.

## Future imports

The domain model is provider-neutral so future AniList, MyAnimeList, Kitsu, or file imports can map into the same `LibraryEntry` contract.
