import pytest

from anime_calendar.integrations.supabase import SupabaseConfig
from anime_calendar.personalization.errors import ConfigurationError


def test_supabase_config_rejects_insecure_remote_url() -> None:
    with pytest.raises(ConfigurationError, match="HTTPS"):
        SupabaseConfig("http://example.com", "anon")


def test_supabase_config_allows_local_development() -> None:
    config = SupabaseConfig("http://localhost:54321", "anon")
    assert config.url == "http://localhost:54321"
