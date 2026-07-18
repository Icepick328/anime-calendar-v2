"""Framework-neutral contracts for dashboards, widgets, events, and plugins."""

from anime_calendar.experience.dashboard import DashboardComposer, DashboardSnapshot
from anime_calendar.experience.events import ExperienceEvent, InMemoryEventBus
from anime_calendar.experience.models import (
    DashboardDefinition,
    DashboardTheme,
    ExperienceTarget,
    RefreshPolicy,
    WidgetPlacement,
    WidgetSize,
)
from anime_calendar.experience.notifications import (
    DeliveryReceipt,
    NotificationChannel,
    NotificationMessage,
    NotificationUrgency,
)
from anime_calendar.experience.plugins import (
    ExperiencePlugin,
    PluginCapability,
    PluginManifest,
    PluginRegistry,
)
from anime_calendar.experience.widgets import (
    WidgetContext,
    WidgetDescriptor,
    WidgetProvider,
    WidgetRegistry,
    WidgetResult,
)

__all__ = [
    "DashboardComposer",
    "DashboardDefinition",
    "DashboardSnapshot",
    "DashboardTheme",
    "DeliveryReceipt",
    "ExperienceEvent",
    "ExperiencePlugin",
    "ExperienceTarget",
    "InMemoryEventBus",
    "NotificationChannel",
    "NotificationMessage",
    "NotificationUrgency",
    "PluginCapability",
    "PluginManifest",
    "PluginRegistry",
    "RefreshPolicy",
    "WidgetContext",
    "WidgetDescriptor",
    "WidgetPlacement",
    "WidgetProvider",
    "WidgetRegistry",
    "WidgetResult",
    "WidgetSize",
]
