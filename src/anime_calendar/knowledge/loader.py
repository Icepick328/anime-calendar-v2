from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Any


@lru_cache(maxsize=1)
def load_provider_catalog() -> dict[str, dict[str, Any]]:
    resource = files("anime_calendar.knowledge").joinpath("providers.json")
    return json.loads(resource.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_anime_streaming_knowledge() -> dict[str, list[dict[str, Any]]]:
    resource = files("anime_calendar.knowledge").joinpath("anime_streaming.json")
    return json.loads(resource.read_text(encoding="utf-8"))
