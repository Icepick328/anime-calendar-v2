# Upgrade to v0.7.1

## What changed

This release adds the first browser experience under `web/`. Demo Mode is the default root dashboard and requires no account or external services.

## Run the dashboard

```powershell
cd web
npm install
npm run dev
```

Open `http://localhost:3000`.

## Validate

```powershell
cd web
npm run lint
npm run build
```

The Python application remains independently testable from the repository root.
