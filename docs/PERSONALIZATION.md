# Personalization Foundation

**Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

## Purpose

The personalization layer answers one question without altering public release facts:

> Should this release appear for this user, and why?

## Domain Objects

- `UserIdentity` — stable account identity and status
- `UserProfile` — display name, locale, and IANA timezone
- `UserPreferences` — genres, studios, providers, variants, release types, and favorites
- `PersonalCalendar` — ownership and visibility metadata for a future personal feed
- `FilterDecision` — inclusion result, reasons, and deterministic score
- `PersonalizedRelease` — a public release paired with a private decision

## Security Boundary

The package contains no authentication tokens, passwords, provider sessions, or database code. Persistence is represented by protocols so a future adapter can apply authentication and row-level security outside the domain model.

## Current Rules

1. Excluded genres override positive matches.
2. Favorite anime receive the strongest score.
3. Release-type and variant selections are strict filters.
4. Genre, studio, and provider matches increase relevance.
5. Unmatched releases may be included or excluded explicitly.
6. Public `Release` objects are never mutated.

## Not Yet Implemented

- Supabase authentication
- Database migrations
- Row-level security policies
- Watchlists
- Personal ICS endpoints
- Web dashboard

These are later v0.6 milestones built on the contracts introduced here.
