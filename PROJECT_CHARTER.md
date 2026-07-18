# Project Charter

> **Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

## Purpose

This charter defines the project's scope, governance, decision process, release authority, and quality expectations.

## Product scope

The project may include capabilities that help users understand:

- what anime releases;
- when it releases;
- where it is legally available;
- which version or format is available;
- why the information is trusted;
- how to receive a personalized view or notification.

The project does not host unauthorized media, index piracy sources, or optimize for engagement at the expense of accuracy or user control.

## Governance model

Anime Calendar v2 currently uses a maintainer-led governance model.

### Repository owner

The repository owner has final responsibility for project direction, access control, releases, security response, infrastructure spending, and appointment or removal of maintainers.

### Maintainers

Maintainers review contributions, protect architecture and mission alignment, manage releases, moderate community spaces, and document major decisions.

### Contributors

Contributors may propose features, fixes, data updates, documentation, tests, and architecture changes. Influence grows through sustained, trustworthy participation rather than title alone.

## Decision process

1. Small implementation decisions may be resolved through pull-request review.
2. Significant product or architecture decisions require written rationale.
3. Decisions meeting the ADR criteria in `CONTRIBUTING.md` require an ADR.
4. Security and privacy decisions require explicit threat and data-ownership review.
5. Maintainers seek consensus, but the repository owner resolves deadlocks.
6. Accepted decisions may be revisited when assumptions materially change; changes must be documented rather than silently reversed.

## Release authority

Only authorized maintainers may publish version tags, GitHub releases, production deployments, database migrations, or public schema changes.

A release must satisfy the quality gates in `RELEASE_PROCESS.md`. Emergency security fixes may use an abbreviated process, but skipped steps must be completed afterward.

## Data governance

- Public anime metadata and private user data are separate domains.
- Users retain control over their personal preferences and saved records.
- Account data must support export and deletion.
- Elevated credentials never belong in client code, calendar URLs, repository history, or logs.
- Curated knowledge requires evidence and confidence.
- Predictions must remain distinguishable from confirmed records.

## Compatibility and breaking changes

Breaking changes require:

- documented user impact;
- migration guidance;
- versioning consistent with project maturity;
- an ADR when the change affects architecture or public contracts;
- a reasonable deprecation path when feasible.

## Funding and conflicts

Any sponsorship, affiliate relationship, paid placement, or provider partnership must be disclosed. Commercial relationships must not silently alter ranking, confidence, or provider preference.

## Amendments

This charter may be changed through a documented pull request. Material governance changes require an ADR and repository-owner approval.
