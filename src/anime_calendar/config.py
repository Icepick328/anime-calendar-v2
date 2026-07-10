from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Settings:
    calendar_name: str = "Anime Releases"
    lookahead_days: int = 90
    max_pages: int = 10
    events_per_page: int = 50
    event_duration_minutes: int = 30
    output_path: str = "output/anime_calendar.ics"
    request_timeout_seconds: int = 30


def load_settings(path: str | Path = "config.json") -> Settings:
    config_path = Path(path)
    if not config_path.exists():
        return Settings()

    try:
        raw: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {config_path}: {exc}") from exc

    allowed = {field_name for field_name in Settings.__dataclass_fields__}
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError(f"Unknown configuration keys: {', '.join(unknown)}")

    return Settings(**raw)
