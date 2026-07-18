from __future__ import annotations

import requests

from anime_calendar.integrations.supabase.client import SupabaseConfig
from anime_calendar.personalization.auth import AuthenticatedUser
from anime_calendar.personalization.errors import AuthenticationError


class SupabaseAuthProvider:
    """Validates a user JWT with Supabase Auth; never accepts unverified token claims."""

    def __init__(self, config: SupabaseConfig, session: requests.Session | None = None) -> None:
        self.config = config
        self.session = session or requests.Session()

    def authenticate(self, access_token: str) -> AuthenticatedUser:
        if not access_token.strip():
            raise AuthenticationError("access token must not be empty")
        response = self.session.get(
            f"{self.config.url}/auth/v1/user",
            headers={
                "apikey": self.config.anon_key,
                "Authorization": f"Bearer {access_token}",
            },
            timeout=self.config.timeout_seconds,
        )
        if not response.ok:
            raise AuthenticationError(
                f"Supabase authentication failed ({response.status_code})"
            )
        payload = response.json()
        user_id = str(payload.get("id", "")).strip()
        if not user_id:
            raise AuthenticationError("Supabase response did not include a user id")
        email = payload.get("email")
        return AuthenticatedUser(user_id=user_id, email=email, access_token=access_token)
