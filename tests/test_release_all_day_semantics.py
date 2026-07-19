from datetime import UTC, date, datetime

from anime_calendar.models import (
    Release,
    ReleasePrecision,
    ReleaseType,
)
from tests.test_models import make_anime


def test_exact_date_datetime_is_all_day() -> None:
    release = Release(
        anime=make_anime(media_format="MOVIE"),
        release_type=ReleaseType.MOVIE,
        released_at=datetime(2026, 8, 14, tzinfo=UTC),
        precision=ReleasePrecision.EXACT_DATE,
    )

    assert release.is_all_day


def test_exact_time_datetime_is_not_all_day() -> None:
    release = Release(
        anime=make_anime(),
        release_type=ReleaseType.EPISODE,
        episode_number=1,
        released_at=datetime(2026, 8, 14, 12, tzinfo=UTC),
        precision=ReleasePrecision.EXACT_TIME,
    )

    assert not release.is_all_day


def test_plain_date_remains_all_day_for_compatibility() -> None:
    release = Release(
        anime=make_anime(media_format="OVA"),
        release_type=ReleaseType.OVA,
        released_at=date(2026, 8, 14),
        precision=ReleasePrecision.UNKNOWN,
    )

    assert release.is_all_day
