# ADR-0010: Framework-neutral experience platform

- **Status:** Accepted
- **Date:** 2026-07-18

## Context

The project will deliver a web dashboard first, followed by a customizable desktop application and later a public API. Coupling dashboard concepts directly to React, Next.js, Tauri, or HTTP would duplicate business rules and make future clients harder to maintain.

## Decision

Define dashboards, widgets, events, notifications, plugins, and experience targets in a framework-neutral Python package.

The web dashboard is the default target and first delivery priority. Desktop and API remain explicit targets supported by shared contracts.

## Consequences

- Experience rules can be tested without a browser or server.
- React and Tauri clients can reuse the same concepts.
- Renderers must translate structured widget results into their native UI.
- Durable events, remote plugins, and network APIs require later adapters.
