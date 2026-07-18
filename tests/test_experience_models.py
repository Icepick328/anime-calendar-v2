from datetime import timedelta

import pytest

from anime_calendar.experience import (
    DashboardDefinition,
    ExperienceTarget,
    RefreshPolicy,
    WidgetPlacement,
)


def test_dashboard_orders_widgets() -> None:
    dashboard = DashboardDefinition(
        dashboard_id="main",
        owner_id="user-1",
        name="Mission Control",
        widgets=(
            WidgetPlacement(widget_id="timeline", position=2),
            WidgetPlacement(widget_id="upcoming", position=0),
        ),
    )

    assert [item.widget_id for item in dashboard.ordered_widgets()] == ["upcoming", "timeline"]
    assert dashboard.target is ExperienceTarget.WEB


def test_dashboard_rejects_duplicate_positions() -> None:
    with pytest.raises(ValueError, match="positions"):
        DashboardDefinition(
            dashboard_id="main",
            owner_id="user-1",
            name="Mission Control",
            widgets=(
                WidgetPlacement(widget_id="one", position=0),
                WidgetPlacement(widget_id="two", position=0),
            ),
        )


def test_refresh_policy_rejects_too_frequent_refresh() -> None:
    with pytest.raises(ValueError, match="one minute"):
        RefreshPolicy(interval=timedelta(seconds=30))
