"""Supabase authentication and persistence adapters."""

from anime_calendar.integrations.supabase.auth import SupabaseAuthProvider
from anime_calendar.integrations.supabase.client import SupabaseConfig, SupabaseRestClient
from anime_calendar.integrations.supabase.repositories import (
    SupabaseAccountRepository,
    SupabaseIdentityRepository,
    SupabasePreferenceRepository,
)

__all__ = [
    "SupabaseAccountRepository",
    "SupabaseAuthProvider",
    "SupabaseConfig",
    "SupabaseIdentityRepository",
    "SupabasePreferenceRepository",
    "SupabaseRestClient",
]
