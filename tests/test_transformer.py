from datetime import UTC, datetime

from anime_calendar.services.transformer import transform_airing_schedule


def test_transform_airing_schedule_enriches_metadata_and_deduplicates() -> None:
    raw_item = {
        "airingAt": 1780000000,
        "episode": 12,
        "media": {
            "id": 42,
            "siteUrl": "https://anilist.co/anime/42",
            "title": {
                "romaji": "Romaji Name",
                "english": "English Name",
                "native": "日本語名",
            },
            "description": "A <b>great</b> anime.<br>Second line.",
            "genres": ["Action", "Fantasy"],
            "season": "SUMMER",
            "seasonYear": 2026,
            "format": "TV",
            "status": "RELEASING",
            "source": "LIGHT_NOVEL",
            "episodes": 12,
            "duration": 24,
            "averageScore": 82,
            "coverImage": {
                "extraLarge": "https://example.com/poster.jpg",
                "large": None,
            },
            "bannerImage": "https://example.com/banner.jpg",
            "studios": {
                "nodes": [
                    {"name": "Example Studio", "isAnimationStudio": True},
                ]
            },
            "trailer": {
                "site": "youtube",
                "id": "abc123",
                "thumbnail": "https://example.com/trailer.jpg",
            },
            "externalLinks": [
                {
                    "site": "Official Site",
                    "url": "https://example.com/anime",
                    "type": "INFO",
                    "language": "Japanese",
                }
            ],
        },
    }

    releases = transform_airing_schedule([raw_item, raw_item])

    assert len(releases) == 1
    release = releases[0]
    anime = release.anime
    assert anime.title == "English Name"
    assert anime.native_title == "日本語名"
    assert anime.synopsis == "A great anime. Second line."
    assert anime.studios == ("Example Studio",)
    assert anime.season_label == "Summer 2026"
    assert anime.trailer is not None
    assert anime.trailer.url == "https://www.youtube.com/watch?v=abc123"
    assert anime.external_links[0].site == "Official Site"
    assert release.airing_at == datetime.fromtimestamp(1780000000, tz=UTC)
