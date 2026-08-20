# task.md - Water Body: Earth Systems Data Art (v3)

Read `PLAN.md` first. This file is the current next-action list after commit
`d6dc2bf` on GitHub.

Verified on 2026-08-20:

- GitHub `main` and local `main` both point at `d6dc2bf`.
- `python -m pytest` passes: 6 tests.
- Streamlit `AppTest` passes all 8 slides.
- Slide 8 live satellite tracking is implemented with `st.fragment(run_every="5s")`.
- Local `.env` has NASA, Movebank, and Copernicus credentials present.
- Local data exists for EPIC cache, Movebank CSV, HydroRIVERS, sea ice, Natural Earth, and CelesTrak TLE.
- Local NDVI GeoTIFF input is missing.
- Local DEM GeoTIFF input is missing.

---

## Task 1 - Deploy to Streamlit Community Cloud

This is the main remaining blocker. Code is ready; deployment needs the user's
Streamlit/GitHub account access.

- [ ] Open Streamlit Community Cloud: `https://share.streamlit.io`
- [ ] Create a new app from `https://github.com/Abhisar-else/space-project`
- [ ] Set main file path to `app.py`
- [ ] Add secrets in the Streamlit dashboard, not in Git:

```toml
NASA_API_KEY = "..."
MOVEBANK_USERNAME = "..."
MOVEBANK_PASSWORD = "..."
COPERNICUS_USERNAME = "..."
COPERNICUS_PASSWORD = "..."
```

- [ ] Deploy from `main`.
- [ ] Click through all 8 deployed slides.
- [ ] Confirm Slide 8 satellite markers update every 5 seconds.
- [ ] Add the deployed URL to `PROGRESS.md`.
- [ ] Check `[x] Deployed on Streamlit Community Cloud` in `PROGRESS.md`.

Verification:

```bash
git status --short --branch
python -m pytest
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py'); at.run(timeout=90); print('exceptions:', at.exception)"
```

---

## Task 2 - Add real NDVI input for Slide 6

Slide 6 currently works, but on this machine it falls back to synthetic data
because `data/rasterio/*.tif` is missing.

Use one of these inputs:

- A precomputed NDVI GeoTIFF, one band, values in `[-1, 1]`
- A two-band GeoTIFF stack where band 1 is red and band 2 is NIR

Place it under:

```text
data/rasterio/
```

Then verify:

```bash
python -c "from pathlib import Path; print(any(Path('data/rasterio').glob('*.tif')))"
python slides/slide6_ndvi.py
```

Do not commit `data/`; it is intentionally gitignored.

---

## Task 3 - Add real DEM input for Slide 7

Slide 7 currently works, but on this machine it falls back to synthetic terrain
because `data/gdal/*.tif` is missing.

Use a DEM GeoTIFF from Copernicus GLO-30, SRTM, or OpenTopography and place it
under:

```text
data/gdal/
```

Then verify:

```bash
python -c "from pathlib import Path; print(any(Path('data/gdal').glob('*.tif')))"
python slides/slide7_terrain.py
```

The current code computes hillshade in Python, so `gdaldem` is not required for
the app path. Keep `gdal-bin` as optional deployment guidance only if future
work switches back to GDAL CLI processing.

---

## Task 4 - Confirm deployed real-data behavior

After deployment, check whether each slide is using real data or fallback data
in the cloud environment. Do not infer this from local files, because `data/`
is gitignored and will not automatically exist in Streamlit Cloud.

| Slide | Expected cloud behavior |
|---|---|
| 1 Earth Overview | Real EPIC metadata/image if `NASA_API_KEY` is set; fallback if API fails |
| 2 Species Migration | Real Movebank if credentials and study permission work; fallback otherwise |
| 3 River Veins | Synthetic unless HydroRIVERS is provided in cloud storage or committed another way |
| 4 Ocean Currents | Can auto-fetch Copernicus SST with Copernicus Marine credentials |
| 5 Sea Ice Cycle | Can auto-fetch Copernicus `siconc` with Copernicus Marine credentials |
| 6 Vegetation Index | Synthetic unless an NDVI GeoTIFF is provided in the cloud filesystem |
| 7 Terrain & Hillshade | Synthetic unless a DEM GeoTIFF is provided in the cloud filesystem |
| 8 Satellite Tracking | Real CelesTrak TLE fetch if outbound network works; synthetic fallback otherwise |

If real local-only files are required in the hosted app, add a separate data
hosting strategy. Do not commit large raw datasets just to make Streamlit Cloud
see them.

---

## Task 5 - Completed: Slide 5 Copernicus auto-fetch

`load_sea_ice_data()` now checks local `*seaice*.nc` files first, then downloads
Arctic monthly 2023 `siconc` data from Copernicus Marine when credentials are
available, and finally falls back to the synthetic cycle. The downloader is
covered by a mocked regression test.

Verification:

```bash
python -m pytest tests/test_sea_ice_loader.py
python slides/slide5_seaice.py
```

Keep the fallback contract: any API/file failure returns the synthetic sea-ice
cycle, never an app crash.
