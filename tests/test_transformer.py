from datetime import UTC, datetime

from anime_calendar.services.transformer import transform_airing_schedule


def test_transform_airing_schedule_prefers_english_title_and_deduplicates() -> None:
    raw = [
        {
            "airingAt": 1780000000,
            "episode": 3,
            "media": {
                "id": 42,
                "siteUrl": "https://anilist.co/anime/42",
                "title": {"romaji": "Romaji Name", "english": "English Name"},
                "genres": ["Action"],
                "coverImage": {"extraLarge": "https://example.com/poster.jpg", "large": None},
            },
        },
        {
            "airingAt": 1780000000,
            "episode": 3,
            "media": {
                "id": 42,
                "siteUrl": "https://anilist.co/anime/42",
                "title": {"romaji": "Romaji Name", "english": "English Name"},
                "genres": ["Action"],
                "coverImage": {"extraLarge": "https://example.com/poster.jpg", "large": None},
            },
        },
    ]

    releases = transform_airing_schedule(raw)

    assert len(releases) == 1
    assert releases[0].anime.title == "English Name"
    assert releases[0].airing_at == datetime.fromtimestamp(1780000000, tz=UTC)
