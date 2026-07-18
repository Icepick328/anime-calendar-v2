from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import RLock
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ExperienceEvent:
    name: str
    aggregate_id: str | None = None
    payload: Mapping[str, object] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("event name must not be empty")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")


EventHandler = Callable[[ExperienceEvent], None]


class InMemoryEventBus:
    """Small synchronous event bus for domain-to-experience integration."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._history: deque[ExperienceEvent] = deque(maxlen=500)
        self._lock = RLock()

    def subscribe(self, event_name: str, handler: EventHandler) -> Callable[[], None]:
        if not event_name.strip():
            raise ValueError("event_name must not be empty")
        with self._lock:
            self._handlers[event_name].append(handler)

        def unsubscribe() -> None:
            with self._lock:
                handlers = self._handlers.get(event_name, [])
                if handler in handlers:
                    handlers.remove(handler)

        return unsubscribe

    def publish(self, event: ExperienceEvent) -> None:
        with self._lock:
            handlers = tuple(self._handlers.get(event.name, ()))
            wildcard_handlers = tuple(self._handlers.get("*", ()))
            self._history.append(event)
        for handler in (*handlers, *wildcard_handlers):
            handler(event)

    def history(self) -> tuple[ExperienceEvent, ...]:
        with self._lock:
            return tuple(self._history)
