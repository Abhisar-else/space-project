# Water Body: Earth Systems Data Art

A Streamlit dashboard of Earth-systems visualizations inspired by the
*Water Body* installation (marshmallowlaserfeast, ARTIS Amsterdam Royal Zoo,
2026). Built entirely from open scientific datasets and original Python
code — no borrowed imagery, no copyrighted assets. Every visual is generated
from real data where available, with a synthetic fallback so the app never
crashes on a missing file or a dead API.

Beyond the visuals, this project is a working demonstration of the Python
geospatial stack: **GeoPandas, Shapely, PyProj, Rasterio, GDAL-style
processing**, alongside **Plotly, Skyfield, xarray, and cartopy**.

## Slides

**8 slides are wired into the live app today.** A 9th (meteor showers) is
implemented and tested as a standalone module but not yet wired into
`app.py` — see [Slide 9](#slide-9--meteor-shower-calendar-not-yet-wired) below.

| # | Slide | Render pattern | Primary real data source |
|---|---|---|---|
| 1 | Earth Overview | Interactive orthographic globe (Plotly) + static NASA EPIC thumbnail | Natural Earth · NASA EPIC |
| 2 | Species Migration | Interactive orthographic globe (Plotly) | Movebank |
| 3 | River Veins | Interactive orthographic globe (Plotly) | HydroRIVERS / HydroSHEDS |
| 4 | Ocean Currents | Static image (matplotlib) | Copernicus Marine GLORYS12V1 |
| 5 | Sea Ice Cycle | Animated GIF (matplotlib) | Copernicus Marine (`siconc`) / NSIDC-format NetCDF |
| 6 | Vegetation Index (NDVI) | Static image (matplotlib) | Sentinel-2 / Landsat red+NIR raster |
| 7 | Terrain & Hillshade | Static image (matplotlib) | Copernicus GLO-30 DEM / SRTM |
| 8 | Satellite Tracking | Interactive globe, **live-updating every 5 seconds** | CelesTrak (TLE) + Skyfield/SGP4 |
| 9 | Meteor Shower Calendar | Plotly timeline (not a globe — see note) | IAU Meteor Data Center |

Slides 1–3 and 8 drag-to-rotate; slides 4–7 are pre-rendered static
visuals; slide 9 is a calendar timeline, not a projection.

### Why Slide 9 isn't a globe

A meteor shower's radiant is given in **Right Ascension / Declination** —
a direction in the sky — not a latitude/longitude point on Earth's surface.
Plotting it on the same orthographic-globe pattern as rivers or satellites
would be a coordinate-system error, not a style choice. Instead,
`build_meteor_calendar()` converts each shower's solar longitude to a
calendar date (a low-precision solar-ecliptic-longitude formula, Meeus'
*Astronomical Algorithms* ch. 25) and renders it as a `plotly.express.timeline`.

### Slide 9 — meteor shower calendar (not yet wired)

`slides/slide9_meteors.py` and `build_meteor_calendar()` exist, parse
correctly, and were validated against known real shower peak dates during
development. It is **not currently imported or dispatched in `app.py`**, so
it won't appear in the running app's sidebar yet, and it has no
`DATA_SOURCES.md` entry. Wiring it in is a small, well-scoped next task:
add the import, add `"9. Meteor Showers"` to the sidebar `selectbox`, add a
dispatch branch, and add the corresponding `DATA_SOURCES.md` row.

## Fallback behavior

Every real-data loader (`load_*()` / `fetch_*()` in `utils/generators.py`)
returns `None` on any failure — missing file, missing credentials, dead
API, network timeout — rather than raising. The calling slide then falls
back to the matching `generate_*()` synthetic function. **The app never
crashes on missing data**, whether run locally without any `.env` file or
deployed without any credentials configured.

## Quick start

### Recommended (virtual environment)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

### Alternative (conda)

Cartopy and GeoPandas have C-library dependencies that pip frequently fails
to build, especially on Windows — conda avoids this:

```bash
conda create -n nasaviz python=3.11 -y
conda activate nasaviz
conda install -c conda-forge cartopy geopandas xarray netcdf4 rasterio -y
pip install -r requirements.txt
streamlit run app.py
```

### Environment variables (optional)

Every credential below is optional — without them, the affected slides
render with synthetic data instead of failing.

```text
NASA_API_KEY=
MOVEBANK_USERNAME=
MOVEBANK_PASSWORD=
COPERNICUS_USERNAME=
COPERNICUS_PASSWORD=
```

Store these in a local `.env` file (already gitignored). In production,
use your host's secrets manager instead of a committed `.env` file.

## Architecture

```
utils/colors.py       — every design token (hex colors, fonts, DPI). Nothing
                         else in the project hardcodes a hex value.
utils/generators.py   — all data access. generate_*() = synthetic, always
                         succeeds. load_*()/fetch_*() = tries real data,
                         returns None on any failure.
slides/slideN_*.py    — one file per slide, render/build functions only.
                         Never call requests/rasterio/xr.open_dataset
                         directly — only via utils/generators.py.
app.py                — Streamlit wiring only (sidebar selectbox, caching,
                         dispatch, live-refresh fragment for Slide 8).
```

## Project docs

- [PLAN.md](./PLAN.md) — project roadmap and architecture
- [SETUP.md](./SETUP.md) — environment setup and dependency guidance
- [DATA_SOURCES.md](./DATA_SOURCES.md) — every dataset and how to access it
- [DESIGN_TOKENS.md](./DESIGN_TOKENS.md) — color, typography, and export specs
- [PROGRESS.md](./PROGRESS.md) — build log and verification notes
- [DEPLOYMENT.md](./DEPLOYMENT.md) — Streamlit Community Cloud deployment steps

## Data attribution

All datasets are free and open, credited to their original providers: NASA
(EPIC), Copernicus Marine Service, Copernicus Sentinel-2 / GLO-30 DEM,
HydroSHEDS/WWF, Movebank, USGS/EarthExplorer, CelesTrak, and the IAU Meteor
Data Center. See [DATA_SOURCES.md](./DATA_SOURCES.md) for full links and
access details.

## License

Code is intended to be released under the MIT License; **no `LICENSE` file
is committed to this repository yet** — add one before treating the project
as formally licensed. Data is subject to each provider's own terms (all
sources used here are free/open for non-commercial and portfolio use).
