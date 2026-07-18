# Contributing

> **Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

Thank you for helping improve the project. Contributions should strengthen user trust, architectural clarity, and long-term maintainability—not merely add surface area.

## Before contributing

Read:

- `FOUNDATION.md`
- `MISSION.md`
- `ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `PROJECT_CHARTER.md`
- relevant files in `docs/adr/`

For significant behavior or architecture changes, open an issue or design discussion before implementation.

## Contribution principles

- Explain the user problem before proposing the technical solution.
- Preserve uncertainty; never turn an estimate into an unlabeled fact.
- Prefer canonical models and reusable engines over output-specific logic.
- Keep public anime metadata separate from private account data.
- Do not introduce scraping, piracy links, credential handling, or provider integrations without legal, security, and architectural review.
- Leave the codebase easier to understand than you found it.

## Development setup

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Required checks

Before submitting a pull request:

```powershell
python -m ruff check .
python -m pytest
python -m anime_calendar
```

All checks must pass. New behavior requires tests. User-facing or architectural changes require documentation updates.

## Pull-request expectations

A pull request should state:

1. What problem does this solve?
2. Why is this the right layer for the change?
3. What alternatives were considered?
4. How is uncertainty represented?
5. What tests were added or updated?
6. What documentation changed?
7. Does this require an ADR, migration, privacy review, or security review?

Keep changes focused. Unrelated cleanup should be separated unless necessary for correctness.

## Architecture changes

Create an Architecture Decision Record when a change:

- introduces or replaces a major subsystem;
- changes a canonical model or public schema;
- adds an infrastructure dependency;
- changes authentication, authorization, privacy, or data ownership;
- establishes a convention future contributors must follow;
- accepts meaningful technical debt.

Copy `docs/adr/0000-template.md`, assign the next number, and document context, decision, alternatives, consequences, and status.

## Data contributions

Curated streaming or release knowledge must include a source and confidence. Do not add unsupported claims. Prefer official provider pages, official announcements, and first-party metadata.

Never commit:

- passwords, API secrets, private feed tokens, or service-role keys;
- personal user records;
- copyrighted media files without permission;
- links intended primarily for unauthorized access.

## Commit and release style

Use clear, imperative commit messages. Versioned changes should update `CHANGELOG.md`, `ROADMAP.md`, and applicable documentation.

Examples:

```text
Add provider evidence normalization
Document account data ownership model
Fix duplicate movie premiere merging
```

## Review standard

Reviewers evaluate correctness, evidence, security, privacy, readability, test quality, documentation, and mission alignment. Passing tests alone do not guarantee acceptance.

## Conduct

All participation is governed by `CODE_OF_CONDUCT.md`.
