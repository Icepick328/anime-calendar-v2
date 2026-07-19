# Anime Calendar v0.7.3 — Media Timezone Fix

This package fixes the 40 `naive_release_datetime` errors found by the new diagnostics CLI.

## Root cause

`transform_media_releases()` converted AniList media start dates into plain Python `date` values.

The diagnostics system correctly identified those values as lacking timezone information.

## Fix

Media start dates are now represented as midnight UTC datetimes:

```python
datetime.combine(
    release_date,
    datetime.min.time(),
    tzinfo=UTC,
)
```

The release still retains `EXACT_DATE` precision, so midnight UTC is only the normalized internal representation—not a claim that AniList supplied a release time.

The merge logic was also adjusted so it continues comparing calendar dates correctly after media releases become datetimes.

## Included files

- `src/anime_calendar/services/transformer.py`
- `tests/test_transformer_timezone.py`

The package replaces `transformer.py` with the complete corrected file. It adds a separate regression-test file and does not overwrite your existing `tests/test_transformer.py`.

## Install

Extract the ZIP into:

```text
C:\Users\Brad\Documents\GitHub\anime-calendar-v2
```

Allow the `src` and `tests` folders to merge. Approve replacing:

```text
src\anime_calendar\services\transformer.py
```

## Verify installation

```powershell
Test-Path src\anime_calendar\services\transformer.py
Test-Path tests\test_transformer_timezone.py
```

Both should return `True`.

## Run focused tests

```powershell
python -m pytest tests\test_transformer.py tests\test_transformer_timezone.py
```

Expected result:

```text
8 passed
```

The exact count may differ if your existing transformer test file has changed.

## Run the complete suite

```powershell
python -m pytest
```

Expected result:

```text
116 passed
```

## Run live diagnostics

```powershell
python -m anime_calendar.cli.diagnostics --limit 20
```

Target:

```text
Errors                 0
Warnings               0
```

## Commit after successful verification

```powershell
git status
git diff --stat
git add src/anime_calendar/services/transformer.py
git add tests/test_transformer_timezone.py
git commit -m "v0.7.3: normalize media release dates to UTC"
git status
```
