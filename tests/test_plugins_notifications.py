from dataclasses import dataclass

import pytest

from anime_calendar.experience import (
    NotificationMessage,
    PluginCapability,
    PluginManifest,
    PluginRegistry,
)


@dataclass
class DemoPlugin:
    manifest: PluginManifest


def test_plugin_registry_filters_by_capability() -> None:
    registry = PluginRegistry()
    registry.register(
        DemoPlugin(
            PluginManifest(
                plugin_id="demo.widgets",
                name="Demo Widgets",
                version="1.0.0",
                capabilities=frozenset({PluginCapability.WIDGETS}),
            )
        )
    )

    assert registry.supporting(PluginCapability.WIDGETS)[0].plugin_id == "demo.widgets"
    assert registry.supporting(PluginCapability.NOTIFICATIONS) == ()


def test_plugin_manifest_requires_capability() -> None:
    with pytest.raises(ValueError, match="capability"):
        PluginManifest(plugin_id="empty", name="Empty", version="1", capabilities=frozenset())


def test_notification_requires_content() -> None:
    with pytest.raises(ValueError, match="content"):
        NotificationMessage(notification_id="n1", user_id="u1", subject="", body="body")
