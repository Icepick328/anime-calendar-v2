from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import requests

from anime_calendar.config import Settings

LOGGER = logging.getLogger(__name__)
ANILIST_URL = "https://graphql.anilist.co"

QUERY = """
query ($page: Int!, $perPage: Int!, $airingAtGreater: Int!, $airingAtLesser: Int!) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      hasNextPage
    }
    airingSchedules(
      airingAt_greater: $airingAtGreater
      airingAt_lesser: $airingAtLesser
      sort: TIME
    ) {
      airingAt
      episode
      media {
        id
        siteUrl
        title {
          romaji
          english
          native
        }
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
        coverImage {
          extraLarge
          large
        }
        bannerImage
        studios(isMain: true) {
          nodes {
            name
            isAnimationStudio
          }
        }
        trailer {
          id
          site
          thumbnail
        }
        externalLinks {
          site
          url
          type
          language
        }
      }
    }
  }
}
"""


class AniListError(RuntimeError):
    """Raised when AniList cannot return a usable schedule."""


def fetch_airing_schedule(settings: Settings) -> list[dict[str, Any]]:
    now = datetime.now(UTC)
    end = now + timedelta(days=settings.lookahead_days)
    results: list[dict[str, Any]] = []

    with requests.Session() as session:
        session.headers.update({"User-Agent": "anime-calendar-v2/0.2"})

        for page in range(1, settings.max_pages + 1):
            variables = {
                "page": page,
                "perPage": settings.events_per_page,
                "airingAtGreater": int(now.timestamp()),
                "airingAtLesser": int(end.timestamp()),
            }

            try:
                response = session.post(
                    ANILIST_URL,
                    json={"query": QUERY, "variables": variables},
                    timeout=settings.request_timeout_seconds,
                )
                response.raise_for_status()
                payload = response.json()
            except (requests.RequestException, ValueError) as exc:
                raise AniListError(f"AniList request failed on page {page}: {exc}") from exc

            if payload.get("errors"):
                raise AniListError(f"AniList returned GraphQL errors: {payload['errors']}")

            page_data = payload.get("data", {}).get("Page")
            if not page_data:
                raise AniListError("AniList response did not contain Page data.")

            schedules = page_data.get("airingSchedules") or []
            results.extend(schedules)
            LOGGER.info("Fetched page %s with %s releases", page, len(schedules))

            if not page_data.get("pageInfo", {}).get("hasNextPage"):
                break

    return results
