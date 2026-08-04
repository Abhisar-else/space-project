# Product Requirements Document — Space Project (Image Application)

## Purpose
Deliver a single-file Streamlit image application showcasing eight interactive visualizations of Earth system datasets for portfolio and demonstration purposes.

## Goals
- Interactive, fast-loading visualizations for slides 1–3 and 8 using Plotly orthographic globe.
- High-fidelity static/raster slides (4–7) rendered from scientific datasets with synthetic fallbacks.
- Reusable data-loader contract: `load_*()` returns None when data missing so generators fallback.
- Clear setup and credentials guidance for users to load real data.

## Slides (Functional Requirements)
1. Earth Overview — interactive Plotly globe; NASA EPIC companion photo; `render_globe` retains thumbnail behavior.
2. Species Migration — interactive Plotly globe; uses `load_movebank_migration()` with fallback.
3. River Veins — interactive Plotly globe; `build_river_globe()` cached for fast reloads.
4. Ocean Currents — static high-res SST map with vector overlay, NetCDF loader.
5. Sea Ice Cycle — animated GIF from NetCDF or synthetic generator.
6. Vegetation Index — NDVI from rasterio or synthetic grid.
7. Terrain & Hillshade — GDAL/rasterio hillshade or synthetic DEM.
8. Satellite Tracking — Skyfield + CelesTrak TLE loader + synthetic fallback; short TTL caching.

## Non-functional Requirements
- All visual styles driven by `utils/colors.py` tokens.
- `requirements.txt` must list runtime dependencies; avoid misspellings.
- Document data sources and .env variables in `DATA_SOURCES.md` and `SETUP.md`.
- Tests must cover loader fallbacks (existing pytest files).

## Acceptance Criteria
- `streamlit run app.py` starts with no import errors on a properly provisioned environment.
- All slides render using either real data (if present) or deterministic synthetic fallback.
- New slide 8 integrates and is selectable from the sidebar.

## Risks
- External APIs require credentials (Movebank, Copernicus, NASA). Provide clear .env examples.
- Large datasets (HydroRIVERS, GLORYS) must be downloaded manually or via separate scripts and are not bundled.

## Next Steps
- Finalize PR with documentation updates and commit message describing added Skyfield support and satellite slide.
