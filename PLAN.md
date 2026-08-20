# plan.md — Water Body: Earth Systems Data Art

Context document for any AI agent (Copilot or otherwise) working on this repo.
Read this in full before changing code. It is the durable "why" — `task.md` in
the same directory is the concrete, sequenced "what to do right now."

(v2 — previous version was written but never committed; this replaces it,
updated against the actual current repo state as of commit `975d139`.)

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
    `outputs/`, displayed via `st.image()`. Used for slides 4-7.
  - Interactive: `build_X_globe()` — returns a Plotly `go.Figure` directly (no
    file write), displayed via `st.plotly_chart(fig, width='stretch')`. Used
    for slides 1, 2, 3, 8 — all four use `projection_type="orthographic"` so
    the globe is click-and-drag rotatable.
- `app.py` — Streamlit wiring only: imports, sidebar `st.sidebar.selectbox`
  (a dropdown, not `st.radio`), `st.cache_data`-wrapped calls to the
  interactive builders, one `if`/`elif` branch per slide.
- `AGENTS.md` — repo-level orientation for coding agents (Copilot-authored).
  Treat it as a quick map, not a source of truth — this file (`plan.md`) and
  `Rules.md` carry the actual rules and hard-won specifics.

## Non-negotiable rules

1. **Fallback contract**: every `load_*()`/`fetch_*()` function must return
   `None` (not raise) on any failure. The caller then falls through to the
   matching `generate_*()`. The app must never crash on missing data or a dead API.
2. **No hardcoded colors** outside `utils/colors.py`. If a token's value
   changes, update both `utils/colors.py` and `DESIGN_TOKENS.md` together.
3. **New data source → `DATA_SOURCES.md` entry first**, in the existing
   per-slide table format, before wiring the loader in.
4. **`PROGRESS.md` checkboxes reflect verified reality**, not intent or a
   commit message. A checkbox claiming real data is flowing must be
   independently confirmed by checking for the actual file on disk or the
   actual credential in `.env` — `data/` and `.env` are both gitignored, so a
   fresh clone alone cannot confirm this. Don't check the box from the repo;
   check it from the filesystem the app actually runs on.
5. **No copyrighted or borrowed imagery, ever.**
6. **Conda over pip** for anything with compiled C dependencies in
   human-facing setup docs: cartopy, geopandas, GDAL, rasterio.
7. **Targeted diffs, not full-file rewrites**, unless a file is genuinely
   structurally broken.

## Regression history (resolved as of `975d139` — stay alert for a repeat)

Earlier in this repo's history, the interactive-globe conversion for slides 1
and 2, and a Python-API fix to the Copernicus Marine downloader, were each
implemented, verified working, then silently reverted when a later commit was
built from an older checkout. Both are confirmed fixed now, verified directly
against commit `975d139`: `build_earth_globe`, `render_epic_thumbnail`,
`build_migration_globe` all present and imported; `load_ocean_sst_data` calls
`copernicusmarine.subset()` directly, not a subprocess.

**The operating principle this leaves behind: never trust that a previous fix
is still present just because it was implemented once. Grep for it and
confirm before building on top of it** — same as the verification commands
below do at the end of every task.

## Current state per slide (verified against commit `975d139`)

| # | Slide | Render style | Loader | Real source | Code status | Real data confirmed on disk? |
|---|---|---|---|---|---|---|
| 1 | Earth Overview | interactive globe | `render_epic_thumbnail` | NASA EPIC API | working | unverifiable from repo — needs `.env` |
| 2 | Species Migration | interactive globe | `load_movebank_migration` | Movebank | working | unverifiable from repo |
| 3 | River Veins | interactive globe | `load_hydrorivers` | HydroRIVERS v10 | working | unverifiable — needs `data/hydrorivers/` |
| 4 | Ocean Currents | static PNG | `load_ocean_sst_data` | Copernicus Marine GLORYS12V1 | working, auto-downloads via `copernicusmarine.subset()` | unverifiable |
| 5 | Sea Ice Cycle | animated GIF | `load_sea_ice_data` | Copernicus Marine (siconc) / NSIDC | working, **local-file-only, no auto-download** | unverifiable |
| 6 | Vegetation Index | static PNG | `load_ndvi_data` | Sentinel-2/Landsat | working, local-file-only | not yet — `PROGRESS.md` confirms still synthetic |
| 7 | Terrain & Hillshade | static PNG | `load_dem_hillshade` | SRTM / Copernicus GLO-30 DEM | working, needs `gdaldem` + local file | not yet |
| 8 | Satellite Tracking | interactive globe | `load_satellite_positions` | CelesTrak TLE (Skyfield/SGP4) | working, auto-fetches, no account needed | live once deployed with network access |

All 8 slides pass a full `AppTest` run with zero exceptions as of `975d139`.
`pytest` is 5/5.

## Tech stack

Python 3.11, Streamlit, Plotly, matplotlib + cartopy, GeoPandas, Shapely,
PyProj, Rasterio, GDAL (CLI via `gdaldem`), Skyfield, xarray, netCDF4,
copernicusmarine. Conda preferred locally (Windows dev environment); plain
pip works for CI/testing.

## Verification commands

```bash
pip install -r requirements.txt --dry-run

python3 -c "
import ast
from collections import Counter
tree = ast.parse(open('utils/generators.py').read())
names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
dupes = {k: v for k, v in Counter(names).items() if v > 1}
print('Duplicates:', dupes if dupes else 'none')
"

python3 -m pytest tests/ -q

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

## Out of scope

Do not attempt: a FastAPI backend, real-time satellite collision detection,
the full 16k+-object satellite catalog, or an AI/ML imagery-search feature.
Evaluated against reference projects (OrbitShield, SkyFi/TerraByte AI, Google
Weather Lab) and explicitly scoped out — the first needed a much bigger
system than one slide warrants, the other two need proprietary
foundation/forecast models this project has no access to. Confirmed via a
repo-wide search that no weather-forecast code exists — don't reintroduce
without new information (e.g. a genuinely free equivalent API/model appearing).