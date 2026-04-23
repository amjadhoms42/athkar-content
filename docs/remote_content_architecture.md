# Remote Content Architecture

## Overview

```
Google Sheets
     │  (Google Sheets API)
     ▼
Python script (convert_sheets.py)
     │  generates
     ▼
data/*.json  +  data/manifest.json
     │  committed to GitHub
     ▼
GitHub raw content CDN
     │  (HTTPS)
     ▼
Flutter app (RemoteDataSource)
     │  on startup / background
     ▼
DataSyncService
  ├─ fetch manifest
  ├─ compare version vs cached
  ├─ if newer → download files
  └─ save to Hive (content_box)
     │
     ▼
ContentRepository
  ├─ reads from Hive cache
  └─ falls back to seed data if cache is empty / corrupted
     │
     ▼
Screens & Widgets
```

## Data Flow Details

### 1. Manifest Check (network-first)
- App fetches `manifest.json` on every cold start (fire-and-forget after `runApp`)
- Compares `version` field against `getSyncVersion()` stored in Hive
- If version matches → no download, uses cached data

### 2. File Download (only when newer)
- Downloads only the files listed in `fileHashes`
- Each file is validated with `jsonDecode()` before saving
- On any network or parse error → silently skips, keeps old cached data

### 3. Offline Fallback
- `ContentRepository` checks Hive cache first
- If cache is empty or returns an empty array → falls back to `kSeedXxx` constants
- App is always functional even with no network

### 4. Data Update Frequency
- GitHub Actions runs daily at 03:00 UTC
- Can also be triggered manually from GitHub → Actions tab
- Flutter checks on every app start (lightweight: only downloads manifest first)

## Security Notes
- `GOOGLE_SERVICE_ACCOUNT_JSON` and `GOOGLE_SHEET_ID` are **GitHub Secrets** — never in code
- The GitHub repository URL in `app_constants.dart` is public (raw content CDN is public by design)
- No write access is ever given to the Flutter app
- The Python script has **read-only** Sheets scope

## Files

| File | Purpose |
|------|---------|
| `data/manifest.json` | Version + file hashes, fetched first |
| `data/items.json` | All dhikr/dua items |
| `data/readings.json` | Reading/wird metadata |
| `data/segments.json` | Reading text segments |
| `data/hijri_content.json` | Hijri calendar content |
| `tools/content_pipeline/convert_sheets.py` | Sheets → JSON converter |
| `tools/content_pipeline/validate_data.py` | CI validation step |
| `.github/workflows/sync_content.yml` | GitHub Actions workflow |
| `lib/data/remote/remote_data_source.dart` | HTTP fetcher |
| `lib/core/services/data_sync_service.dart` | Sync orchestrator |
| `lib/data/repositories/content_repository.dart` | Cache + fallback provider |
