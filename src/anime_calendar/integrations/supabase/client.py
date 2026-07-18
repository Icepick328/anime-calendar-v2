from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

from anime_calendar.personalization.errors import ConfigurationError, PersistenceError


@dataclass(frozen=True, slots=True)
class SupabaseConfig:
    url: str
    anon_key: str
    timeout_seconds: float = 10.0

    def __post_init__(self) -> None:
        if not self.url.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            raise ConfigurationError("SUPABASE_URL must use HTTPS or a local HTTP address")
        if not self.anon_key.strip():
            raise ConfigurationError("SUPABASE_ANON_KEY must not be empty")
        if self.timeout_seconds <= 0:
            raise ConfigurationError("timeout_seconds must be positive")

    @classmethod
    def from_environment(cls) -> SupabaseConfig:
        url = os.getenv("SUPABASE_URL", "").rstrip("/")
        anon_key = os.getenv("SUPABASE_ANON_KEY", "")
        if not url or not anon_key:
            raise ConfigurationError("SUPABASE_URL and SUPABASE_ANON_KEY are required")
        return cls(url=url, anon_key=anon_key)


class SupabaseRestClient:
    """Small PostgREST client that always acts with the user's JWT and RLS."""

    def __init__(self, config: SupabaseConfig, session: requests.Session | None = None) -> None:
        self.config = config
        self.session = session or requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        access_token: str,
        params: dict[str, str] | None = None,
        json: object | None = None,
        prefer: str | None = None,
    ) -> Any:
        headers = {
            "apikey": self.config.anon_key,
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        response = self.session.request(
            method,
            f"{self.config.url}/rest/v1/{path.lstrip('/')}",
            headers=headers,
            params=params,
            json=json,
            timeout=self.config.timeout_seconds,
        )
        if not response.ok:
            raise PersistenceError(
                f"Supabase request failed ({response.status_code}): {response.text[:300]}"
            )
        if response.status_code == 204 or not response.content:
            return None
        return response.json()
