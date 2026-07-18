from __future__ import annotations

from dataclasses import dataclass

from anime_calendar.experience.models import DashboardDefinition
from anime_calendar.experience.widgets import WidgetContext, WidgetRegistry, WidgetResult


@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    dashboard: DashboardDefinition
    widgets: tuple[WidgetResult, ...]


class DashboardComposer:
    def __init__(self, widgets: WidgetRegistry) -> None:
        self.widgets = widgets

    def compose(self, dashboard: DashboardDefinition) -> DashboardSnapshot:
        results: list[WidgetResult] = []
        for placement in dashboard.ordered_widgets():
            if not placement.visible:
                continue
            provider = self.widgets.get(placement.widget_id)
            if dashboard.target not in provider.descriptor.supported_targets:
                continue
            context = WidgetContext(
                user_id=dashboard.owner_id,
                target=dashboard.target,
                settings=placement.settings,
            )
            results.append(provider.load(context))
        return DashboardSnapshot(dashboard=dashboard, widgets=tuple(results))
