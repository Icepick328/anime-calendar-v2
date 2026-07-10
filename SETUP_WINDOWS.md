# Windows setup and v0.4.0 upgrade

## Upgrade an existing clone

1. Commit and push your current work.
2. Extract the v0.4.0 ZIP.
3. Copy everything inside the extracted folder into the repository root.
4. Replace files when Windows asks.
5. Do not delete `.git` or `.venv`.

Then run:

```powershell
cd $HOME\Documents\GitHub\anime-calendar-v2
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
python -m anime_calendar
```

Expected tests:

```text
11 passed
```

Generated calendars include:

```text
output\anime_calendar.ics
output\all_releases.ics
output\episodes.ics
output\movies.ics
output\specials.ics
output\streaming_confirmed.ics
output\crunchyroll.ics
output\hidive.ics
```

Empty provider feeds are valid and indicate that no matching provider was confirmed during the current look-ahead window.
