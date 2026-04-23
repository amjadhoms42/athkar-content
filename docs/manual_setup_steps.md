# Manual Setup Steps

Follow these steps **once** after cloning the repository to activate the full data pipeline.

---

## Step 1 — Create a GitHub Repository

1. Go to github.com → New repository
2. Name it anything (e.g. `athkar-content`)
3. Set visibility to **Public** (required for free raw content CDN)
4. Push this codebase to it:
   ```bash
   git init
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git add .
   git commit -m "init"
   git push -u origin main
   ```

---

## Step 2 — Update the App's Remote URL

Open [lib/core/constants/app_constants.dart](../athkar_rtl_core/lib/core/constants/app_constants.dart) and replace the placeholders:

```dart
static const String remoteDataBaseUrl =
    'https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/data';
```

Commit and push.

---

## Step 3 — Create a Google Cloud Service Account

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use an existing one)
3. Enable **Google Sheets API**: APIs & Services → Enable APIs → search "Sheets"
4. Go to **IAM & Admin → Service Accounts → Create Service Account**
   - Name: `sheets-reader`
   - Role: none needed (read-only access is granted at sheet level)
5. Click the service account → **Keys → Add Key → JSON**
6. Download the JSON file — keep it safe, **never commit it**

---

## Step 4 — Create a Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com) → New spreadsheet
2. Create four tabs named exactly:
   - `items`
   - `readings`
   - `segments`
   - `hijri_content`
3. Add the column headers from [docs/google_sheet_schema.md](google_sheet_schema.md)
4. Share the sheet with the service account email (from Step 3) as **Viewer**
5. Copy the Sheet ID from the URL:
   `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`

---

## Step 5 — Add GitHub Secrets

1. Go to your GitHub repository → **Settings → Secrets and variables → Actions**
2. Add two secrets:

   | Name | Value |
   |------|-------|
   | `GOOGLE_SERVICE_ACCOUNT_JSON` | Paste the entire contents of the JSON key file |
   | `GOOGLE_SHEET_ID` | The Sheet ID from Step 4 |

---

## Step 6 — Run the Workflow

1. Go to your repository → **Actions → Sync Content from Google Sheets**
2. Click **Run workflow → Run workflow**
3. Watch the logs — it should:
   - Fetch your sheet data
   - Write JSON files to `data/`
   - Validate them
   - Commit and push the updated files

---

## Step 7 — Test in the App

1. Run the Flutter app
2. After the splash screen, the background sync will fire automatically
3. Check that content appears (if your sheet has data)
4. To force-test locally, temporarily add a debug print in `DataSyncService.syncIfNeeded()`

---

## Step 8 — (Optional) Local Script Testing

```bash
cd tools/content_pipeline
pip install -r requirements.txt

# Copy and fill in the example config
cp config.example.json config.json
# Edit config.json with your real GOOGLE_SHEET_ID

# Place service_account.json here (never commit it — it's gitignored)
cp ~/Downloads/your-key.json service_account.json

# Run
python convert_sheets.py
python validate_data.py
```

---

## Step 9 — Android Release Signing (before Play Store upload)

1. Generate a keystore (do this once, keep it safe — never commit it):
   ```bash
   keytool -genkey -v -keystore ~/athkar-release.jks \
     -keyalg RSA -keysize 2048 -validity 10000 \
     -alias athkar
   ```
2. Create `android/key.properties` (gitignored automatically):
   ```
   storePassword=YOUR_STORE_PASSWORD
   keyPassword=YOUR_KEY_PASSWORD
   keyAlias=athkar
   storeFile=/absolute/path/to/athkar-release.jks
   ```
3. Build release APK / AAB:
   ```bash
   flutter build appbundle --release
   ```

---

## Ongoing Usage

- **Add/edit content**: Update rows in the Google Sheet
- **Deploy update**: Go to GitHub Actions → Run workflow manually, OR wait for the daily 03:00 UTC auto-run
- **App update**: Users get new content on next app start (no Play Store update needed)
- **Emergency rollback**: Revert the `data/` commit on GitHub — apps will pick up the old version next sync
