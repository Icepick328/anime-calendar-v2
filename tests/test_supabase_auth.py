from unittest.mock import Mock

import pytest

from anime_calendar.integrations.supabase import SupabaseAuthProvider, SupabaseConfig
from anime_calendar.personalization.errors import AuthenticationError


def test_auth_provider_returns_verified_identity() -> None:
    session = Mock()
    session.get.return_value = Mock(
        ok=True,
        json=Mock(return_value={"id": "user-1", "email": "brad@example.com"}),
    )
    provider = SupabaseAuthProvider(SupabaseConfig("https://example.supabase.co", "anon"), session)

    user = provider.authenticate("valid-token")

    assert user.user_id == "user-1"
    assert user.email == "brad@example.com"
    assert user.access_token == "valid-token"


def test_auth_provider_rejects_invalid_token() -> None:
    session = Mock()
    session.get.return_value = Mock(ok=False, status_code=401)
    provider = SupabaseAuthProvider(SupabaseConfig("https://example.supabase.co", "anon"), session)

    with pytest.raises(AuthenticationError, match="401"):
        provider.authenticate("bad-token")
