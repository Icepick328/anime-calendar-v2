# Experience Platform

> **Anime Calendar v2 is an open-source Anime Release Intelligence Platform dedicated to accuracy, transparency, personalization, and long-term maintainability.**

## Purpose

The Experience Platform translates application capabilities into calm, explainable, and customizable user experiences. It does not own release intelligence or private user data. It composes those capabilities for a specific delivery target.

## Product priority

1. **Web dashboard** — the primary experience and first public interface.
2. **Customizable desktop application** — a native-feeling experience that reuses the same contracts and allows user-controlled layouts.
3. **Public API** — an integration surface after the primary user experiences are established.

The priority controls delivery order, not architectural importance. All three targets share framework-neutral models.

## Components

### Dashboard definitions

A dashboard is an immutable description of its owner, target, theme, refresh policy, and ordered widget placements. It contains no React, Tauri, HTTP, or database objects.

### Widget framework

Widgets declare:

- a stable identifier;
- a human-readable purpose;
- supported experience targets;
- a default size;
- a load operation that returns structured data.

Rendering remains the client's responsibility.

### Event bus

The synchronous in-memory event bus establishes the contract for decoupled reactions such as:

- `library.updated`;
- `preferences.updated`;
- `calendar.generated`;
- `release.changed`.

A durable queue may replace or supplement it later without changing event producers.

### Plugins and capabilities

Plugins declare capabilities instead of requiring the core to know concrete implementations. Initial capabilities cover widgets, notifications, exports, metadata, and recommendations.

### Notification contracts

Notifications are transport-neutral messages. Email, Discord, web push, RSS, and future channels will implement the same delivery contract.

## Non-goals for v0.7.0

- No React or Next.js application yet.
- No Tauri shell yet.
- No HTTP API server.
- No asynchronous or durable event broker.
- No third-party plugin execution.

Those capabilities build on this release rather than being mixed into it.
