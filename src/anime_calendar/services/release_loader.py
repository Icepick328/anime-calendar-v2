from __future__ import annotations

from anime_calendar.config import Settings
from anime_calendar.models import Release
from anime_calendar.providers.anilist import (
    fetch_airing_schedule,
    fetch_media_releases,
)
from anime_calendar.services.transformer import (
    merge_releases,
    transform_airing_schedule,
    transform_media_releases,
)


def load_live_releases(settings: Settings) -> list[Release]:
    episode_releases = transform_airing_schedule(
        fetch_airing_schedule(settings)
    )
    media_releases = transform_media_releases(
        fetch_media_releases(settings)
    )

    return merge_releases(
        episode_releases,
        media_releases,
    )
