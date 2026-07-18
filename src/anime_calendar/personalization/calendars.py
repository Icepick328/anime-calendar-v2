from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from secrets import token_urlsafe
from typing import Protocol

from icalendar import Calendar

from anime_calendar.calendars.ics_builder import build_calendar
from anime_calendar.models import Release
from anime_calendar.personalization.engine import PersonalizationEngine
from anime_calendar.personalization.models import PersonalCalendar, UserPreferences


@dataclass(frozen=True, slots=True)
class FeedToken:
    calendar_id: str
    plaintext: str
    token_hash: str
    created_at: datetime

    @classmethod
    def issue(cls, calendar_id: str) -> FeedToken:
        plaintext = token_urlsafe(32)
        return cls(
            calendar_id=calendar_id,
            plaintext=plaintext,
            token_hash=hash_feed_token(plaintext),
            created_at=datetime.now(UTC),
        )


@dataclass(frozen=True, slots=True)
class PersonalCalendarResult:
    definition: PersonalCalendar
    included_releases: tuple[Release, ...]
    calendar: Calendar


class PersonalCalendarRepository(Protocol):
    def get_calendar(self, calendar_id: str) -> PersonalCalendar | None: ...

    def list_calendars(self, owner_id: str) -> tuple[PersonalCalendar, ...]: ...

    def save_calendar(self, calendar: PersonalCalendar) -> None: ...

    def save_feed_token_hash(self, calendar_id: str, token_hash: str) -> None: ...

    def resolve_calendar_by_token_hash(self, token_hash: str) -> PersonalCalendar | None: ...


class PersonalCalendarService:
    def __init__(self, engine: PersonalizationEngine | None = None) -> None:
        self.engine = engine or PersonalizationEngine()

    def generate(
        self,
        definition: PersonalCalendar,
        releases: list[Release],
        preferences: UserPreferences,
        *,
        event_duration_minutes: int = 30,
    ) -> PersonalCalendarResult:
        if not definition.enabled:
            selected: tuple[Release, ...] = ()
        else:
            selected = tuple(
                item.release for item in self.engine.evaluate(releases, preferences)
            )
        calendar = build_calendar(
            list(selected),
            calendar_name=definition.name,
            event_duration_minutes=event_duration_minutes,
        )
        return PersonalCalendarResult(definition, selected, calendar)


def hash_feed_token(token: str) -> str:
    if not token.strip():
        raise ValueError("feed token must not be empty")
    return sha256(token.encode("utf-8")).hexdigest()
