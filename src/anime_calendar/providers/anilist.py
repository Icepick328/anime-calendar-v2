from __future__ import annotations

import logging
from datetime import UTC, date, datetime, timedelta
from typing import Any

import requests

from anime_calendar.config import Settings

LOGGER = logging.getLogger(__name__)
ANILIST_URL = "https://graphql.anilist.co"

_MEDIA_FIELDS = """
  id
  siteUrl
  title { romaji english native }
  description(asHtml: false)
  genres
  season
  seasonYear
  format
  status
  source
  episodes
  duration
  averageScore
  coverImage { extraLarge large }
  bannerImage
  studios(isMain: true) { nodes { name isAnimationStudio } }
  trailer { id site thumbnail }
  externalLinks { site url type language }
"""

AIRING_QUERY = f"""
query ($page: Int!, $perPage: Int!, $airingAtGreater: Int!, $airingAtLesser: Int!) {{
  Page(page: $page, perPage: $perPage) {{
    pageInfo {{ hasNextPage }}
    airingSchedules(
      airingAt_greater: $airingAtGreater
      airingAt_lesser: $airingAtLesser
      sort: TIME
    ) {{
      airingAt
      episode
      media {{ {_MEDIA_FIELDS} }}
    }}
  }}
}}
"""

MEDIA_RELEASE_QUERY = f"""
query (
  $page: Int!
  $perPage: Int!
  $startDateGreater: FuzzyDateInt!
  $startDateLesser: FuzzyDateInt!
  $formats: [MediaFormat!]
) {{
  Page(page: $page, perPage: $perPage) {{
    pageInfo {{ hasNextPage }}
    media(
      type: ANIME
      startDate_greater: $startDateGreater
      startDate_lesser: $startDateLesser
      format_in: $formats
      sort: START_DATE
    ) {{
      {_MEDIA_FIELDS}
      startDate {{ year month day }}
    }}
  }}
}}
"""


class AniListError(RuntimeError):
    """Raised when AniList cannot return usable release data."""


def _fuzzy_date(value: date) -> int:
    return int(value.strftime("%Y%m%d"))


def _post(session: requests.Session, query: str, variables: dict[str, Any]) -> dict[str, Any]:
    try:
        response = session.post(
            ANILIST_URL,
            json={"query": query, "variables": variables},
            timeout=variables.pop("_timeout"),
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise AniListError(f"AniList request failed: {exc}") from exc

    if payload.get("errors"):
        raise AniListError(f"AniList returned GraphQL errors: {payload['errors']}")
    return payload


def fetch_airing_schedule(settings: Settings) -> list[dict[str, Any]]:
    now = datetime.now(UTC)
    end = now + timedelta(days=settings.lookahead_days)
    results: list[dict[str, Any]] = []

    with requests.Session() as session:
        session.headers.update({"User-Agent": "anime-calendar-v2/0.5"})
        for page in range(1, settings.max_pages + 1):
            payload = _post(
                session,
                AIRING_QUERY,
                {
                    "page": page,
                    "perPage": settings.events_per_page,
                    "airingAtGreater": int(now.timestamp()),
                    "airingAtLesser": int(end.timestamp()),
                    "_timeout": settings.request_timeout_seconds,
                },
            )
            page_data = payload.get("data", {}).get("Page")
            if not page_data:
                raise AniListError("AniList airing response did not contain Page data.")

            schedules = page_data.get("airingSchedules") or []
            results.extend(schedules)
            LOGGER.info("Fetched airing page %s with %s releases", page, len(schedules))
            if not page_data.get("pageInfo", {}).get("hasNextPage"):
                break

    return results


def fetch_media_releases(settings: Settings) -> list[dict[str, Any]]:
    today = datetime.now(UTC).date()
    end = today + timedelta(days=settings.lookahead_days)
    results: list[dict[str, Any]] = []

    with requests.Session() as session:
        session.headers.update({"User-Agent": "anime-calendar-v2/0.5"})
        for page in range(1, settings.media_max_pages + 1):
            payload = _post(
                session,
                MEDIA_RELEASE_QUERY,
                {
                    "page": page,
                    "perPage": settings.events_per_page,
                    "startDateGreater": _fuzzy_date(today - timedelta(days=1)),
                    "startDateLesser": _fuzzy_date(end + timedelta(days=1)),
                    "formats": list(settings.non_episode_formats),
                    "_timeout": settings.request_timeout_seconds,
                },
            )
            page_data = payload.get("data", {}).get("Page")
            if not page_data:
                raise AniListError("AniList media response did not contain Page data.")

            media = page_data.get("media") or []
            results.extend(media)
            LOGGER.info("Fetched media page %s with %s releases", page, len(media))
            if not page_data.get("pageInfo", {}).get("hasNextPage"):
                break

    return results
