# AGENTS

## Purpose
This file helps AI coding agents understand the repository layout, development workflow, and code conventions so they can make productive changes quickly.

## Repository overview
- `app.py`: Streamlit dashboard orchestrating the visualization suite.
- `slides/*.py`: slide-specific renderers for globe, migration, rivers, ocean, sea ice, NDVI, terrain, and satellites.
- `utils/`: shared utilities for design tokens, synthetic data generation, and optional real-data loading.
- `data/`: anchor folder for raw input datasets; most modules fall back to synthetic data when real files are unavailable.
- `outputs/`: generated images, GIFs, and static slide artifacts.
- `tests/`: lightweight tests for local data loaders and synthetic fallback behavior.

## Key conventions
- The project targets Python 3.11 and prefers a conda environment because packages such as `cartopy` and `geopandas` have native dependencies.
- `slides/*.py` modules may use `sys.path.insert(0, ...)` so that `from utils.*` works when executed directly.
- `utils/generators.py` is the core data layer: real-data loader functions are named `load_*`, and synthetic fallback generators are named `generate_*`.
- Visualizations should remain runnable even without full raw datasets since synthetic fallback data is a first-class part of the design.
- The Streamlit app caches expensive slide builds to reduce repeated rendering overhead.

## Running and verifying
- `streamlit run app.py` — launch the interactive dashboard.
- `python -m pytest` — run the test suite.
- `python slides/slideX.py` — generate or update an individual slide output.
- `python -c "from utils.colors import BG_COLOR; print(BG_COLOR)"` — quick import sanity check.

## Dependencies and environment
- Base dependencies are documented in `README.md` and `SETUP.md`.
- Recommended install path uses conda plus `pip install matplotlib cmocean imageio pandas numpy shapely pyproj requests streamlit`.
- Optional data sources include NASA EPIC, Copernicus Marine, HydroRIVERS, Movebank, and NSIDC.

## Notes for agents
- Do not assume raw dataset files are present; preserve fallback behavior when modifying loaders or renderers.
- Prefer updates to `utils/generators.py` for adding robust synthetic defaults or improving local dataset detection.
- Keep visual style changes consistent with the dark, neon-cyan aesthetic in `utils/colors.py` and the Streamlit CSS in `app.py`.
- Link to existing documentation rather than duplicating it: `README.md`, `SETUP.md`, `DATA_SOURCES.md`, `DESIGN_TOKENS.md`, `IMPLEMENTATION_PLAN.md`.
- New repository skills are available under `skills/`:
  - `skills/claude-md-authoring/SKILL.md`
  - `skills/dev-lifecycle/SKILL.md`
  - `skills/ponytail-lazy-senior-dev/SKILL.md`
  - `skills/superpowers-dev-workflow/SKILL.md`

## Useful files
- `README.md` — project intent, quick start, asset list.
- `SETUP.md` — environment setup and dependency guidance.
- `DATA_SOURCES.md` — dataset provenance and download notes.
- `DESIGN_TOKENS.md` — color/typography design tokens.
- `IMPLEMENTATION_PLAN.md` — architecture and task plan.
- `tests/` — loader and fallback behavior tests.
