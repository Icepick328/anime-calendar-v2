from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Protocol

from anime_calendar.experience.models import ExperienceTarget, WidgetSize


@dataclass(frozen=True, slots=True)
class WidgetContext:
    user_id: str
    target: ExperienceTarget = ExperienceTarget.WEB
    settings: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty")


@dataclass(frozen=True, slots=True)
class WidgetDescriptor:
    widget_id: str
    display_name: str
    description: str
    supported_targets: frozenset[ExperienceTarget]
    default_size: WidgetSize = WidgetSize.MEDIUM

    def __post_init__(self) -> None:
        if not self.widget_id.strip() or not self.display_name.strip():
            raise ValueError("widget identity fields must not be empty")
        if not self.supported_targets:
            raise ValueError("widget must support at least one experience target")


@dataclass(frozen=True, slots=True)
class WidgetResult:
    widget_id: str
    title: str
    data: Mapping[str, object]
    empty_state: str | None = None


class WidgetProvider(Protocol):
    descriptor: WidgetDescriptor

    def load(self, context: WidgetContext) -> WidgetResult: ...


class WidgetRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, WidgetProvider] = {}

    def register(self, provider: WidgetProvider) -> None:
        widget_id = provider.descriptor.widget_id
        if widget_id in self._providers:
            raise ValueError(f"widget already registered: {widget_id}")
        self._providers[widget_id] = provider

    def get(self, widget_id: str) -> WidgetProvider:
        try:
            return self._providers[widget_id]
        except KeyError as error:
            raise LookupError(f"unknown widget: {widget_id}") from error

    def available(self, target: ExperienceTarget) -> tuple[WidgetDescriptor, ...]:
        descriptors = (
            provider.descriptor
            for provider in self._providers.values()
            if target in provider.descriptor.supported_targets
        )
        return tuple(sorted(descriptors, key=lambda descriptor: descriptor.display_name.casefold()))
