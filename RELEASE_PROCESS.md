# Release Process

> **Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

Every release should answer:

1. What did we build?
2. Why did we build it?
3. What foundation did it create?

## Release stages

### 1. Define capability

Document the user problem, intended capability, explicit non-goals, risks, and success criteria. Update the roadmap when scope changes.

### 2. Review architecture

Identify affected engines, canonical models, schemas, data ownership, external services, security boundaries, and migrations. Create or update ADRs when required.

### 3. Implement

Prefer complete, cohesive changes. Preserve uncertainty and evidence. Avoid output-specific business logic when the capability belongs in a reusable engine.

### 4. Test

Required:

```powershell
python -m ruff check .
python -m pytest
python -m anime_calendar
```

Tests should cover new behavior, failure paths, model invariants, and regressions. External integrations require mocked contract tests where practical.

### 5. Validate CI

The main branch must have a green workflow. Generated calendars must be structurally valid and uploaded as artifacts.

### 6. Review product and trust

Confirm:

- mission alignment;
- transparent confidence and evidence;
- no unsupported claims;
- privacy and security implications addressed;
- user-facing terminology consistent with `BRAND.md`;
- no accidental piracy, credential, or personal-data exposure.

### 7. Update documentation

As applicable, update:

- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `TECHNICAL_DEBT.md`
- `docs/ARCHITECTURE.md`
- subsystem documentation
- ADRs
- setup and migration guides

### 8. Prepare release notes

Release notes explain capability, motivation, foundation created, upgrade steps, known limitations, and validation results.

### 9. Commit, tag, and publish

Example:

```powershell
git add .
git commit -m "v0.6.0: add accounts and preferences"
git push
git tag -a v0.6.0 -m "v0.6.0 — Accounts and Preferences"
git push origin v0.6.0
```

Publish a GitHub Release from the tag after CI succeeds.

## Quality gates

### Engineering

- Ruff passes.
- Tests pass.
- CI passes.
- Generated outputs validate.
- Dependencies and secrets are handled safely.

### Documentation

- Changelog is current.
- Architecture reflects behavior.
- Roadmap reflects scope.
- Setup and migration guidance is accurate.
- Important decisions are recorded.

### Product

- Capability solves the stated user problem.
- Uncertainty is visible.
- Terminology is consistent.
- Accessibility and privacy impact are considered.
- No undocumented user-facing behavior is introduced.

### Operations

For hosted features:

- rollback path exists;
- migrations are reviewed;
- monitoring and error handling are defined;
- credentials are stored only in approved secret managers;
- rate limits and failure modes are documented.

## Patch and emergency releases

Security or critical correctness fixes may be released quickly. At minimum, the fix must be reviewed, tested, documented, and followed by any deferred architecture or process work.
