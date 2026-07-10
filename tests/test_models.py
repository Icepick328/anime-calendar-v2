from anime_calendar.models import Anime, ExternalLink, Trailer


def test_anime_season_label_and_trailer_url() -> None:
    anime = Anime(
        anilist_id=1,
        title="Example",
        romaji_title="Example",
        native_title=None,
        synopsis=None,
        genres=(),
        studios=(),
        season="WINTER",
        season_year=2026,
        media_format=None,
        status=None,
        source=None,
        total_episodes=None,
        duration_minutes=None,
        average_score=None,
        site_url="https://anilist.co/anime/1",
        cover_image_url=None,
        banner_image_url=None,
        trailer=Trailer(site="youtube", trailer_id="xyz"),
        external_links=(ExternalLink(site="Official Site", url="https://example.com"),),
    )

    assert anime.season_label == "Winter 2026"
    assert anime.trailer is not None
    assert anime.trailer.url == "https://www.youtube.com/watch?v=xyz"
