# Deployment Checklist — Water Body: Earth Systems Data Art

**Target:** Streamlit Community Cloud (share.streamlit.io)
**Status:** Ready for deployment
**Date:** 2026-08-20

## Pre-deployment verification

- [x] All 8 slides render without exceptions (verified via AppTest)
- [x] All 5 tests pass (`pytest`)
- [x] No syntax errors in core modules (Pylance checked)
- [x] Satellite tracking refactored for live auto-refresh every 5 seconds
- [x] Bug fix applied: TLE age-calculation that was silently breaking real data fetch
- [x] Code imports clean (unused imports removed where applicable)
- [x] Documentation updated (PROGRESS.md, DATA_SOURCES.md stale notes fixed)
- [x] Fallback behavior preserved across all loaders
- [x] Git repo ready (`main` branch has latest commit `975d139`)

---

## Deployment Steps

### 1. Push to GitHub (if not already done)

```bash
git status
git add -A
git commit -m "Real-time satellite tracking + documentation updates"
git push origin main
```

Confirm `main` branch on GitHub has the latest commits.

---

### 2. Deploy via Streamlit Cloud Dashboard

1. Go to **share.streamlit.io** and sign in (GitHub OAuth recommended)
2. Click **New app** → **From existing repo**
3. Enter repo URL: `https://github.com/Abhisar-else/space-project`
4. Main file path: `app.py`
5. Click **Deploy**

---

### 3. Add Secrets (Streamlit Cloud Dashboard → Settings)

In the **Secrets** panel, add one key-value pair per line (TOML format):

```toml
NASA_API_KEY = "your-api-key-here"
MOVEBANK_USERNAME = "your-username"
MOVEBANK_PASSWORD = "your-password"
COPERNICUS_USERNAME = "your-copernicus-marine-username"
COPERNICUS_PASSWORD = "your-copernicus-marine-password"
```

**Note:** These environment variables are automatically exposed at runtime; no code changes needed. The app reads them via `python-dotenv`'s `load_dotenv()` + `os.getenv()`.

---

### 4. Optional: Add System Dependencies (if real Slide 7 data is deployed)

If you're adding real Copernicus GLO-30 DEM or SRTM raster data to `data/gdal/` before deployment, add a `packages.txt` file to the repo root:

```
gdal-bin
```

This installs the GDAL CLI tools (including `gdaldem` for Slide 7 hillshade computation).

**If not adding real DEM data:** skip this step — Slide 7 will gracefully fall back to synthetic terrain, which is fine.

---

### 5. Verify After Deploy

Once the app builds and goes live (takes ~2–3 min):

1. **Test all 8 slides** in the deployed app — click through each one:
   - Slide 1: Earth globe should render; EPIC photo should fetch or show placeholder
   - Slide 2: Migration globe should render; Movebank data should fetch or show synthetic
   - Slide 3: River network should render (HydroRIVERS local file or synthetic)
   - Slide 4: Ocean SST should render (Copernicus download or synthetic)
   - Slide 5: Sea ice GIF should animate (local file or synthetic)
   - Slide 6: NDVI should render (local raster or synthetic)
   - Slide 7: Terrain hillshade should render (local DEM or synthetic)
   - **Slide 8: Satellite Tracking should update positions every 5 seconds** (watch for movement)

2. **Check the sidebar** — all 8 slides should appear in the dropdown

3. **Check cloud logs** — click **Manage app** → **View logs** to confirm:
   - No unhandled exceptions
   - Skyfield TLE fetch attempts appear in logs (even if they fail gracefully)

---

## Expected Behavior in Cloud

- **With credentials in Secrets:** Real data sources fetch and display
- **Without credentials:** App falls back to synthetic data silently (by design)
- **Network hiccup:** Falls back to synthetic; app never crashes
- **Slide 8 satellite tracking:** Positions recompute every 5 seconds; no network re-fetch of TLEs (cached 1 hour)

---

## Post-deployment: Update PROGRESS.md

Once verified live, add this to `PROGRESS.md`:

```markdown
- [x] Deployed on Streamlit Community Cloud
  - **URL:** share.streamlit.io/[your-github-username]/space-project/main/app.py
  - **Live since:** 2026-08-20
  - **Verified:** All 8 slides render; Slide 8 live tracking confirmed
```

---

## Rollback / Troubleshooting

- **App won't build:** Check `requirements.txt` for syntax errors or missing packages. Redeploy.
- **Secrets not working:** Restart the app via Streamlit Cloud dashboard (small circular icon).
- **Slide shows only synthetic data when you expected real:** Check logs for API fetch errors; verify credentials are correct in Secrets.
- **Slide 8 positions not updating:** Check browser console for JavaScript errors; refresh page. Satellite tracking uses `@st.fragment(run_every="5s")` which requires Streamlit >= 1.39.

---

## Notes for Future Maintenance

- TLE cache is 1 hour; positions update every 5 seconds (pure math, no network overhead)
- Real data loaders return `None` on any failure; the fallback generator takes over automatically
- Secrets are injected at runtime; no `.env` file is needed in the cloud
- `data/` folder is gitignored; real datasets do not push to GitHub
