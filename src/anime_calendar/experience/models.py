from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import timedelta
from enum import StrEnum
from types import MappingProxyType


class ExperienceTarget(StrEnum):
    WEB = "web"
    DESKTOP = "desktop"
    API = "api"


class DashboardTheme(StrEnum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


class WidgetSize(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    FULL = "full"


@dataclass(frozen=True, slots=True)
class RefreshPolicy:
    interval: timedelta = timedelta(minutes=15)
    refresh_on_focus: bool = True

    def __post_init__(self) -> None:
        if self.interval < timedelta(minutes=1):
            raise ValueError("refresh interval must be at least one minute")


@dataclass(frozen=True, slots=True)
class WidgetPlacement:
    widget_id: str
    position: int
    size: WidgetSize = WidgetSize.MEDIUM
    visible: bool = True
    settings: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.widget_id.strip():
            raise ValueError("widget_id must not be empty")
        if self.position < 0:
            raise ValueError("position must not be negative")
        object.__setattr__(self, "settings", MappingProxyType(dict(self.settings)))


@dataclass(frozen=True, slots=True)
class DashboardDefinition:
    dashboard_id: str
    owner_id: str
    name: str
    target: ExperienceTarget = ExperienceTarget.WEB
    theme: DashboardTheme = DashboardTheme.SYSTEM
    widgets: tuple[WidgetPlacement, ...] = ()
    refresh_policy: RefreshPolicy = field(default_factory=RefreshPolicy)

    def __post_init__(self) -> None:
        if not self.dashboard_id.strip():
            raise ValueError("dashboard_id must not be empty")
        if not self.owner_id.strip():
            raise ValueError("owner_id must not be empty")
        if not self.name.strip():
            raise ValueError("name must not be empty")
        widget_ids = [placement.widget_id for placement in self.widgets]
        if len(widget_ids) != len(set(widget_ids)):
            raise ValueError("dashboard widget IDs must be unique")
        positions = [placement.position for placement in self.widgets]
        if len(positions) != len(set(positions)):
            raise ValueError("dashboard widget positions must be unique")

    def ordered_widgets(self) -> tuple[WidgetPlacement, ...]:
        return tuple(sorted(self.widgets, key=lambda placement: placement.position))
