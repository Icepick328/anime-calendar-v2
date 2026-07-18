# Upgrade to v0.7.0

v0.7.0 introduces the Experience Platform Foundation. It does not require database migrations or environment variables.

## Upgrade

Copy the snapshot contents over the existing repository while preserving `.git` and `.venv`, then run:

```powershell
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
python -m anime_calendar
```

## Expected result

- Ruff passes.
- 72 tests pass.
- Existing public and personal calendar behavior remains unchanged.

## New imports

```python
from anime_calendar.experience import (
    DashboardDefinition,
    ExperienceEvent,
    InMemoryEventBus,
    PluginRegistry,
    WidgetRegistry,
)
```
