# NASA Earth Systems Data Visualization

A 5-part data visualization suite recreating the visual language of "Water Body"
(marshmallowlaserfeast, 2026) using entirely open scientific datasets — original
code and renders, no borrowed imagery.

## What's inside

1. **Earth overview** — glowing globe rendered from Natural Earth + NASA EPIC
2. **Species migration** — 20-species movement tracks from Movebank / OBIS-SEAMAP
3. **River networks** — global river geometry from HydroRIVERS / HydroSHEDS
4. **Ocean currents + temperature** — Copernicus GLORYS12V1 + NASA Aqua-MODIS
5. **Sea ice cycle** — animated Arctic/Antarctic freeze-thaw from NSIDC

## Quick start

See [SETUP.md](./SETUP.md) for full environment instructions.

```bash
conda create -n nasaviz python=3.11 -y
conda activate nasaviz
conda install -c conda-forge cartopy geopandas xarray netcdf4 -y
pip install matplotlib cmocean imageio pandas numpy shapely pyproj requests streamlit

streamlit run app.py
```

## Project docs

- [PLAN.md](./PLAN.md) — full 4-week roadmap
- [SETUP.md](./SETUP.md) — install + environment
- [DATA_SOURCES.md](./DATA_SOURCES.md) — every dataset and where to get it
- [DESIGN_TOKENS.md](./DESIGN_TOKENS.md) — colors, typography, export specs
- [PROGRESS.md](./PROGRESS.md) — build log

## Data attribution

All datasets are free and open, credited to their original providers:
NASA (EPIC, SWOT, Aqua-MODIS), Copernicus Marine Service, HydroSHEDS/WWF,
Movebank, OBIS-SEAMAP (Duke University), NSIDC. See DATA_SOURCES.md for links.

## License

Code: MIT. Data: subject to each provider's own terms (all free/open for
non-commercial and portfolio use).
