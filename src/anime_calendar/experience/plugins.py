from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class PluginCapability(StrEnum):
    WIDGETS = "widgets"
    NOTIFICATIONS = "notifications"
    EXPORTS = "exports"
    METADATA = "metadata"
    RECOMMENDATIONS = "recommendations"


@dataclass(frozen=True, slots=True)
class PluginManifest:
    plugin_id: str
    name: str
    version: str
    capabilities: frozenset[PluginCapability]

    def __post_init__(self) -> None:
        if not self.plugin_id.strip() or not self.name.strip() or not self.version.strip():
            raise ValueError("plugin manifest fields must not be empty")
        if not self.capabilities:
            raise ValueError("plugin must declare at least one capability")


class ExperiencePlugin(Protocol):
    manifest: PluginManifest


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, ExperiencePlugin] = {}

    def register(self, plugin: ExperiencePlugin) -> None:
        plugin_id = plugin.manifest.plugin_id
        if plugin_id in self._plugins:
            raise ValueError(f"plugin already registered: {plugin_id}")
        self._plugins[plugin_id] = plugin

    def get(self, plugin_id: str) -> ExperiencePlugin:
        try:
            return self._plugins[plugin_id]
        except KeyError as error:
            raise LookupError(f"unknown plugin: {plugin_id}") from error

    def supporting(self, capability: PluginCapability) -> tuple[PluginManifest, ...]:
        manifests = (
            plugin.manifest
            for plugin in self._plugins.values()
            if capability in plugin.manifest.capabilities
        )
        return tuple(sorted(manifests, key=lambda manifest: manifest.name.casefold()))
