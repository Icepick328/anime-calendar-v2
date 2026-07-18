from dataclasses import dataclass

import pytest

from anime_calendar.experience import (
    DashboardComposer,
    DashboardDefinition,
    ExperienceTarget,
    WidgetContext,
    WidgetDescriptor,
    WidgetPlacement,
    WidgetRegistry,
    WidgetResult,
)


@dataclass
class StaticWidget:
    descriptor: WidgetDescriptor

    def load(self, context: WidgetContext) -> WidgetResult:
        return WidgetResult(
            widget_id=self.descriptor.widget_id,
            title=self.descriptor.display_name,
            data={"user_id": context.user_id, "target": context.target.value},
        )


def widget(widget_id: str, target: ExperienceTarget = ExperienceTarget.WEB) -> StaticWidget:
    return StaticWidget(
        WidgetDescriptor(
            widget_id=widget_id,
            display_name=widget_id.title(),
            description="Test widget",
            supported_targets=frozenset({target}),
        )
    )


def test_widget_registry_and_dashboard_composer() -> None:
    registry = WidgetRegistry()
    registry.register(widget("upcoming"))
    dashboard = DashboardDefinition(
        dashboard_id="main",
        owner_id="user-1",
        name="Mission Control",
        widgets=(WidgetPlacement(widget_id="upcoming", position=0),),
    )

    snapshot = DashboardComposer(registry).compose(dashboard)

    assert snapshot.widgets[0].data["user_id"] == "user-1"


def test_dashboard_skips_target_incompatible_widget() -> None:
    registry = WidgetRegistry()
    registry.register(widget("desktop-only", ExperienceTarget.DESKTOP))
    dashboard = DashboardDefinition(
        dashboard_id="main",
        owner_id="user-1",
        name="Mission Control",
        widgets=(WidgetPlacement(widget_id="desktop-only", position=0),),
    )

    assert DashboardComposer(registry).compose(dashboard).widgets == ()


def test_registry_rejects_duplicate_widget() -> None:
    registry = WidgetRegistry()
    registry.register(widget("upcoming"))

    with pytest.raises(ValueError, match="already registered"):
        registry.register(widget("upcoming"))
