from pathlib import Path
import shutil

path = Path("src/anime_calendar/cli/diagnostics.py")
backup = path.with_suffix(".py.quality-backup")

text = path.read_text(encoding="utf-8")

import_target = (
    "from anime_calendar.config import load_settings\n"
    "from anime_calendar.logging_config import configure_logging\n"
)

import_replacement = (
    "from anime_calendar.config import load_settings\n"
    "from anime_calendar.diagnostics.quality import build_quality_report\n"
    "from anime_calendar.diagnostics.report import format_quality_report\n"
    "from anime_calendar.logging_config import configure_logging\n"
)

flow_target = (
    "        report = diagnose_releases(releases)\n"
    "        print(\n"
    "            format_diagnostic_report(\n"
)

flow_replacement = (
    "        report = diagnose_releases(releases)\n"
    "        quality_report = build_quality_report(releases, report.findings)\n"
    "        print(format_quality_report(quality_report))\n"
    "        print()\n"
    "        print(\n"
    "            format_diagnostic_report(\n"
)

if import_target not in text:
    raise SystemExit(
        "Import target was not found. No changes were made."
    )

if flow_target not in text:
    raise SystemExit(
        "Diagnostics flow target was not found. No changes were made."
    )

if "from anime_calendar.diagnostics.quality import" in text:
    raise SystemExit(
        "Quality report integration already appears to exist."
    )

shutil.copy2(path, backup)

updated = text.replace(import_target, import_replacement, 1)
updated = updated.replace(flow_target, flow_replacement, 1)

path.write_text(updated, encoding="utf-8")

print(f"Created backup: {backup}")
print(f"Updated: {path}")
