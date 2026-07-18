from datetime import datetime

from anime_calendar.models import ReleaseType, ReleaseVariant
from anime_calendar.personalization.calendars import (
    FeedToken,
    PersonalCalendarService,
    hash_feed_token,
)
from anime_calendar.personalization.models import PersonalCalendar, UserPreferences
from tests.test_personalization_engine import make_release


def test_feed_token_hash_is_stable_and_plaintext_is_not_hash():
    token = FeedToken.issue("calendar-1")
    assert token.token_hash == hash_feed_token(token.plaintext)
    assert token.plaintext not in token.token_hash
    assert len(token.token_hash) == 64


def test_empty_feed_token_is_rejected():
    try:
        hash_feed_token("   ")
    except ValueError as error:
        assert "must not be empty" in str(error)
    else:
        raise AssertionError("expected ValueError")


def test_personal_calendar_generates_only_matching_releases():
    favorite = make_release(anilist_id=1, genres=("Action",))
    excluded = make_release(anilist_id=2, genres=("Horror",))
    preferences = UserPreferences(excluded_genres=frozenset({"Horror"}))
    definition = PersonalCalendar("cal-1", "user-1", "Brad's Anime")

    result = PersonalCalendarService().generate(definition, [excluded, favorite], preferences)

    assert result.included_releases == (favorite,)
    assert "Brad's Anime" in result.calendar.to_ical().decode()


def test_disabled_calendar_is_empty():
    release = make_release(anilist_id=1)
    definition = PersonalCalendar("cal-1", "user-1", "Disabled", enabled=False)
    result = PersonalCalendarService().generate(definition, [release], UserPreferences())
    assert result.included_releases == ()


def test_calendar_timestamps_must_be_timezone_aware():
    try:
        PersonalCalendar(
            "cal-1",
            "user-1",
            "Broken",
            created_at=datetime(2026, 1, 1),
        )
    except ValueError as error:
        assert "timezone-aware" in str(error)
    else:
        raise AssertionError("expected ValueError")


def test_variant_and_release_type_preferences_apply_to_calendar():
    episode = make_release(
        anilist_id=1,
        release_type=ReleaseType.EPISODE,
        variant=ReleaseVariant.SUB,
    )
    movie = make_release(
        anilist_id=2,
        release_type=ReleaseType.MOVIE,
        variant=ReleaseVariant.ORIGINAL,
    )
    preferences = UserPreferences(
        preferred_release_types=frozenset({ReleaseType.EPISODE}),
        preferred_variants=frozenset({ReleaseVariant.SUB}),
    )
    definition = PersonalCalendar("cal-1", "user-1", "Subs")
    result = PersonalCalendarService().generate(definition, [movie, episode], preferences)
    assert result.included_releases == (episode,)
