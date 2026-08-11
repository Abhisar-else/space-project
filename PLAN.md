# plan.md — Water Body: Earth Systems Data Art

Context document for any AI agent (Copilot or otherwise) working on this repo.
Read this in full before changing code. It is the durable "why" — `task.md` in
the same directory is the concrete, sequenced "what to do right now."

## What this project is

An 8-slide interactive Streamlit dashboard, inspired by the *Water Body* data-art
installation (marshmallowlaserfeast, ARTIS Amsterdam Royal Zoo, 2026), built
entirely from open scientific datasets and original code. It doubles as a
portfolio demonstration of the Python geospatial toolkit: GeoPandas, Shapely,
PyProj, Rasterio, and GDAL, plus Plotly, Skyfield, xarray, and cartopy.

Live repo: `github.com/Abhisar-else/space-project`

## Architecture (do not restructure without a strong reason)

- `utils/colors.py` — every design token (hex colors, fonts, dpi). Slide files
  and `app.py` import from here; never hardcode a hex value elsewhere.
- `utils/generators.py` — **all** data access lives here. Every function is
  either `generate_*()` (synthetic, no external dependency, always succeeds)
  or `load_*()`/`fetch_*()` (tries real data, returns `None` on any failure —
  never raises). Slide files never call `requests`, `rasterio.open`, `xr.open_dataset`,
  etc. directly; they only call functions from this module.
- `slides/slideN_*.py` — one module per slide, render functions only. Two
  patterns coexist:
  - Static: `render_X(output_path=...)` — matplotlib, saves a PNG/GIF to
    `outputs/`, displayed via `st.image()`. Used for slides 4–7.
  - Interactive: `build_X_globe()` — returns a Plotly `go.Figure` directly (no
    file write), displayed via `st.plotly_chart(fig, width='stretch')`. Used
    for slides 1, 2, 3, 8. All four use `projection_type="orthographic"` so
    the globe is click-and-drag rotatable — this was a deliberate move away
    from pre-rendered auto-rotating GIFs, which slides 1 and 3 both used to be.
- `app.py` — Streamlit wiring only: imports, sidebar `st.sidebar.selectbox`
  (a dropdown, not `st.radio` — also deliberate, for a growing slide list),
  `st.cache_data`-wrapped calls to the interactive builders, and one
  `if`/`elif` branch per slide.

## Non-negotiable rules

1. **Fallback contract**: every `load_*()`/`fetch_*()` function must return
   `None` (not raise) on any failure — missing file, missing credentials,
   network error, parse error. The caller then falls through to the matching
   `generate_*()`. The app must never crash on missing data or a dead API.
2. **No hardcoded colors** outside `utils/colors.py`. If a token's value
   changes, update both `utils/colors.py` and `DESIGN_TOKENS.md` together.
3. **New data source → `DATA_SOURCES.md` entry first**, in the existing
   per-slide table format (`## Slide N — <name>` + a `| Source | Type | Access |`
   table), before wiring the loader in. Citations in `app.py`'s citation boxes
   must describe what the code actually does — never cite a source the
   synthetic fallback is silently substituting for.
4. **`PROGRESS.md` checkboxes reflect verified reality**, not intent. Only
   check a box after running the verification commands below and confirming
   the result — not because a commit message says it's done.
5. **No copyrighted or borrowed imagery, ever.** Only generated visuals from
   code + open datasets.
6. **Conda over pip** for anything with compiled C dependencies in
   human-facing setup docs (`SETUP.md`): cartopy, geopandas, GDAL, rasterio.
   `requirements.txt` still lists pip names for CI/simple installs.
7. **Targeted diffs, not full-file rewrites**, unless a file is genuinely
   structurally broken (e.g. duplicate function definitions — see history
   below). Preserve everything not directly relevant to the task at hand.

## Known regression history — read before touching slides 1, 2, or 4

This repo has, twice now, lost work because a later change was built from an
older checkout that predated an earlier fix. Concretely: the interactive-globe
conversion for slides 1 and 2, and a Python-API fix to the Copernicus Marine
downloader in `utils/generators.py`, were each implemented, verified working,
then silently reverted when the satellite-tracking slide was added on top of
a stale base.

**The operating principle this implies: never trust that a previous fix is
still present. Grep for it and confirm before building on top of it.**
`task.md` Task 0 re-applies both regressions in full, with exact code, so
there's no ambiguity to re-derive incorrectly a third time.

## Current state per slide

| # | Slide | Render style | Real data loader | Real source | Status |
|---|---|---|---|---|---|
| 1 | Earth Overview | interactive globe (Plotly) + NASA EPIC photo | `render_epic_thumbnail` | NASA EPIC API | **regressed — see task.md Task 0** |
| 2 | Species Migration | interactive globe (Plotly) | `load_movebank_migration` | Movebank | **regressed — see task.md Task 0** |
| 3 | River Veins | interactive globe (Plotly) | `load_hydrorivers` | HydroRIVERS v10 | intact; needs real geodatabase file |
| 4 | Ocean Currents | static PNG (matplotlib) | `load_ocean_sst_data` | Copernicus Marine GLORYS12V1 | **Copernicus fetch regressed — see task.md Task 0**; needs account |
| 5 | Sea Ice Cycle | animated GIF (matplotlib) | `load_sea_ice_data` | Copernicus Marine (siconc) | intact; needs same Copernicus account as #4 |
| 6 | Vegetation Index | static PNG (matplotlib) | `load_ndvi_data` | Sentinel-2/Landsat | intact; needs a real raster file |
| 7 | Terrain & Hillshade | static PNG (matplotlib) | `load_dem_hillshade` | SRTM / Copernicus GLO-30 DEM | intact; needs `gdaldem` installed + a real DEM file |
| 8 | Satellite Tracking | interactive globe (Plotly) | `load_satellite_positions` | CelesTrak TLE (Skyfield/SGP4) | intact; works with no account, just needs network access |

## Tech stack

Python 3.11, Streamlit, Plotly (interactive globes), matplotlib + cartopy
(static slides), GeoPandas, Shapely, PyProj, Rasterio, GDAL (CLI, via
`gdaldem`), Skyfield, xarray, netCDF4. Conda preferred locally (Windows dev
environment); plain pip works for CI/testing.

## Verification commands (run these, don't assume)

```bash
# 1. Dependencies resolve cleanly
pip install -r requirements.txt --dry-run

# 2. No duplicate function definitions (this repo has had this bug before)
python3 -c "
import ast
from collections import Counter
tree = ast.parse(open('utils/generators.py').read())
names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
dupes = {k: v for k, v in Counter(names).items() if v > 1}
print('Duplicates:', dupes if dupes else 'none')
"

# 3. Existing tests pass
python3 -m pytest tests/ -q

# 4. Every slide actually runs (this is the one that caught both regressions —
#    a plain import-error check is not enough, you have to select each slide)
python3 -c "
from streamlit.testing.v1 import AppTest
slides = ['1. Earth Overview', '2. Species Migration', '3. River Veins', '4. Ocean Currents',
          '5. Sea Ice Cycle', '6. Vegetation Index', '7. Terrain & Hillshade', '8. Satellite Tracking']
for s in slides:
    at = AppTest.from_file('app.py')
    at.run(timeout=90)
    at.sidebar.selectbox[0].set_value(s).run(timeout=90)
    print(s, 'OK' if not at.exception else f'EXCEPTION: {at.exception[0]}')
"
```

## Out of scope for this pass

Do not attempt: a FastAPI backend, a real-time collision-detection system for
satellites, the full 16k+-object satellite catalog, or an AI/ML imagery search
feature. These were evaluated against reference projects and explicitly
scoped out — see the "why" in `task.md`'s notes if this comes up again.