from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    """Trusted identity returned by an authentication provider."""

    user_id: str
    email: str | None = None
    access_token: str | None = None

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty")


class AuthenticationProvider(Protocol):
    """Boundary for validating an external access token."""

    def authenticate(self, access_token: str) -> AuthenticatedUser: ...
