# Windows upgrade guide — v0.3.0

## 1. Preserve the current working version

```powershell
cd $HOME\Documents\GitHub\anime-calendar-v2
git status
git push
```

## 2. Copy the release snapshot

Extract the downloaded ZIP. Copy everything inside `anime-calendar-v2-v0.3.0` into your repository folder:

```text
C:\Users\Brad\Documents\GitHub\anime-calendar-v2
```

Choose **Replace the files in the destination**.

Do not delete `.git` or `.venv`.

## 3. Refresh the editable installation

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## 4. Verify

```powershell
python -m ruff check .
python -m pytest
python -m anime_calendar
```

Expected tests:

```text
8 passed
```

Expected output files:

```text
output\anime_calendar.ics
output\all_releases.ics
output\episodes.ics
output\movies.ics
output\specials.ics
```

## 5. Commit

```powershell
git status
git add .
git commit -m "v0.3.0: add universal anime release generator"
git push
```
