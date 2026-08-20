# task.md — Water Body: Earth Systems Data Art (v2)

Read `plan.md` first. Task 0 and Task 1 from the previous version of this file
are **done and verified** as of commit `975d139` — don't redo them, just don't
regress them (see `plan.md`'s "Regression history" section for why that
warning is there twice now).

This version covers what's genuinely still open.

---

## Task A — Verify the real-data claims in PROGRESS.md are actually true

`PROGRESS.md` currently checks off "NASA API key obtained," "Copernicus
Marine account registered," "Movebank account access checked," and
"HydroRIVERS data directory present locally." None of this is verifiable from
a fresh clone — `data/` and `.env` are both gitignored. Run this **on the
machine that actually has those files/credentials**, not in a fresh CI
checkout, and only leave the boxes checked if every line below prints `True`
or a real path:

```bash
python3 -c "
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

print('NASA_API_KEY set:', bool(os.getenv('NASA_API_KEY')))
print('MOVEBANK creds set:', bool(os.getenv('MOVEBANK_USERNAME')) and bool(os.getenv('MOVEBANK_PASSWORD')))
print('COPERNICUS creds set:', bool(os.getenv('COPERNICUS_USERNAME')) and bool(os.getenv('COPERNICUS_PASSWORD')))
print('HydroRIVERS gdb present:', Path('data/hydrorivers/HydroRIVERS_v10.gdb').exists())
print('Rasterio NDVI source present:', any(Path('data/rasterio').glob('*.tif')) if Path('data/rasterio').exists() else False)
print('GDAL DEM source present:', any(Path('data/gdal').glob('*.tif')) if Path('data/gdal').exists() else False)
"
```

Then confirm the loaders are actually *using* real data, not just falling
through silently — add a one-off print and run each slide, or check for the
loader's own downloaded artifacts:
```bash
ls data/glorys_sst.nc 2>/dev/null && echo "Slide 4 has a real Copernicus file"
ls data/*seaice*.nc 2>/dev/null && echo "Slide 5 has a real file"
```
If any of these are missing, the corresponding `PROGRESS.md` checkbox is
currently wrong and should be unchecked until the file/credential actually
exists.

---

## Task B — Fix two stale lines in PROGRESS.md

- [ ] Remove or rewrite the "Blockers / notes" line: *"Remote repository is
      configured as origin, but no push/deployment verification was performed
      in this review."* This is no longer true — the repo has been cloned and
      verified live multiple times as of `975d139`.
- [ ] Slide 7 (GDAL/terrain) is currently `[ ]` unchecked in the Week 5
      section despite `slides/slide7_terrain.py` existing and passing the
      `AppTest` check in `plan.md`. Check it.

## Task C — Fix stale note in DATA_SOURCES.md

The `## Notes` section ends with *"Add `SKYFIELD` and `sgp4` to
`requirements.txt` to enable satellite propagation."* — `skyfield` is already
in `requirements.txt` (`sgp4` installs automatically as its dependency, no
separate line needed). Delete this line.

---

## Task D — Deploy to Streamlit Community Cloud

This has been on the roadmap since `PLAN.md` week 4 and has never been done.

- [ ] Push the repo (already done) — confirm `main` branch is what Streamlit
      Cloud will build from.
- [ ] On share.streamlit.io: New app → point at this repo → `app.py` as the
      entry point.
- [ ] Add secrets via the Streamlit Cloud dashboard's Secrets manager (**not**
      a committed `.env`): `NASA_API_KEY`, `MOVEBANK_USERNAME`,
      `MOVEBANK_PASSWORD`, `COPERNICUS_USERNAME`, `COPERNICUS_PASSWORD`. Note
      `utils/generators.py` reads these via `python-dotenv`'s `load_dotenv()`
      + `os.getenv()` — Streamlit Cloud secrets are exposed as environment
      variables at runtime, so this works without code changes.
- [ ] `gdaldem` (Slide 7's real-data path) is a system binary, not a pip
      package — Streamlit Cloud won't have it unless a `packages.txt` file at
      repo root lists `gdal-bin`. Add one if real DEM data is going into
      deployment; otherwise Slide 7 will just run on its synthetic fallback in
      the cloud, which is fine (that's exactly what the fallback is for) but
      worth knowing rather than being surprised by.
- [ ] After deploy, run through all 8 slides in the actual deployed app once
      — cloud environments occasionally differ from local (memory limits,
      missing system libs) in ways `AppTest` locally won't catch.
- [ ] Once confirmed live, check the `PROGRESS.md` box: "Deployed on Streamlit
      Community Cloud."

---

## Task E — Optional: extend Slide 5's Copernicus fetch to auto-download

Right now Slide 4 (`load_ocean_sst_data`) auto-downloads `thetao` from
Copernicus Marine via `copernicusmarine.subset()`, but Slide 5
(`load_sea_ice_data`) only checks for a local file — same account, same API,
but no auto-fetch path. Since both slides already require the same
`COPERNICUS_USERNAME`/`COPERNICUS_PASSWORD`, this is a small win: extend
`load_sea_ice_data()` with the same `copernicusmarine.subset(variables=["siconc"], ...)`
pattern used in `load_ocean_sst_data()`, following the exact same
try/fallback structure. Low priority — not blocking anything, just an
inconsistency worth closing if you're back in that function.

---

## Task F — Real data files, if not already done (see Task A for how to check)

| Slide | Needs | Account | .env vars | Goes in |
|---|---|---|---|---|
| 2 | Movebank whale study access | movebank.org **+ permission request to the study owner** — slow, apply early | `MOVEBANK_USERNAME`, `MOVEBANK_PASSWORD` | fetched live |
| 3 | HydroRIVERS v10 geodatabase | none | — | `data/hydrorivers/HydroRIVERS_v10.gdb` |
| 6 | Sentinel-2 L2A red/NIR (or Landsat) | Copernicus **Data Space** (dataspace.copernicus.eu) — separate account from Copernicus *Marine* | — | `data/rasterio/*.tif` |
| 7 | DEM raster | none (Copernicus GLO-30) or free USGS/OpenTopography (SRTM) | — | `data/gdal/*.tif`; also needs `gdaldem` installed locally |

`.env.example` already exists at repo root and lists the right variable names
— copy it to `.env` and fill in real values, don't recreate it.