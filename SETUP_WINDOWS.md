# Sprint 2 installation on Windows

## 1. Back up the working milestone

From the repository root, confirm Sprint 1.1 is committed and pushed:

```powershell
git status
git push
```

## 2. Copy the Sprint 2 snapshot

Extract the ZIP. Copy every file and folder from inside `anime-calendar-v2-sprint2` into your existing repository:

```text
C:\Users\Brad\Documents\GitHub\anime-calendar-v2
```

Choose **Replace the files in the destination** when Windows prompts. Do not delete `.git` or `.venv`.

## 3. Refresh the editable installation

```powershell
cd $HOME\Documents\GitHub\anime-calendar-v2
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## 4. Verify Sprint 2

```powershell
python -m ruff check .
python -m pytest
python -m anime_calendar
```

Expected result:

```text
4 passed
output\anime_calendar.ics
```

## 5. Commit and push

```powershell
git status
git add .
git commit -m "Sprint 2: add rich metadata engine"
git push
```

The Continuous Integration workflow should lint, test, generate, verify, and upload the calendar artifact.
