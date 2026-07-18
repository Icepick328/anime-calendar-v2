from anime_calendar.experience import ExperienceEvent, InMemoryEventBus


def test_event_bus_publishes_and_records_history() -> None:
    bus = InMemoryEventBus()
    received: list[str] = []
    bus.subscribe("library.updated", lambda event: received.append(event.name))

    event = ExperienceEvent(name="library.updated", aggregate_id="user-1")
    bus.publish(event)

    assert received == ["library.updated"]
    assert bus.history() == (event,)


def test_event_bus_unsubscribe_stops_delivery() -> None:
    bus = InMemoryEventBus()
    received: list[str] = []
    unsubscribe = bus.subscribe("*", lambda event: received.append(event.name))
    unsubscribe()

    bus.publish(ExperienceEvent(name="preferences.updated"))

    assert received == []
