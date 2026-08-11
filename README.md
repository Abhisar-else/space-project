# Water Body: Earth Systems Data Art

An 8-slide interactive Streamlit dashboard inspired by the *Water Body*
installation (marshmallowlaserfeast, 2026). The project uses entirely open
scientific datasets and original Python code; no borrowed imagery is included.

## What's inside

1. **Earth Overview** — interactive globe with Natural Earth and NASA EPIC
2. **Species Migration** — tracked marine and terrestrial migration paths
3. **River Veins** — global HydroRIVERS river network on an orthographic globe
4. **Ocean Currents** — Copernicus GLORYS SST and current visualization
5. **Sea Ice Cycle** — animated polar sea ice concentration sequence
6. **Vegetation Index** — NDVI raster visualization from Sentinel/Landsat
7. **Terrain & Hillshade** — DEM hillshade rendering using GDAL-style processing
8. **Satellite Tracking** — live/ synthetic LEO tracks from CelesTrak and Skyfield

## Quick start

### Recommended (virtual environment)

```powershell
cd "C:\Users\VINOD SHARMA\space project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### Alternative (conda)

```bash
conda create -n nasaviz python=3.11 -y
conda activate nasaviz
conda install -c conda-forge cartopy geopandas xarray netcdf4 python-dotenv -y
pip install -r requirements.txt
python -m streamlit run app.py
```

### Environment variables

Create a local `.env` file from `.env.example` for optional dataset credentials:

```text
NASA_API_KEY=
MOVEBANK_USERNAME=
MOVEBANK_PASSWORD=
COPERNICUS_USERNAME=
COPERNICUS_PASSWORD=
```

## Notes

- `requirements.txt` contains the Python dependencies used by the app.
- The app is designed to fall back to synthetic data when real datasets are
  unavailable or credentials are missing.
- Run the app with the project `.venv` to ensure the same environment as the
  rest of the repo.

## Project docs

- [PLAN.md](./PLAN.md) — project roadmap and architecture
- [SETUP.md](./SETUP.md) — environment setup and dependency guidance
- [DATA_SOURCES.md](./DATA_SOURCES.md) — datasets used and access details
- [DESIGN_TOKENS.md](./DESIGN_TOKENS.md) — color and visual style tokens
- [PROGRESS.md](./PROGRESS.md) — build log and verification notes

## Data attribution

All datasets are free and open, credited to their original providers:
NASA (EPIC, AQUA-MODIS), Copernicus Marine Service, HydroSHEDS/WWF,
Movebank, OBIS-SEAMAP (Duke University), NSIDC, CelesTrak. See `DATA_SOURCES.md`
for full links and access notes.

## License

Code: MIT. Data: subject to each provider's own terms (all free/open for
non-commercial and portfolio use).
