# NASA Earth Systems Data Viz — Project Plan

Inspired by "Water Body" (marshmallowlaserfeast, ARTIS Amsterdam Royal Zoo, 2026).
A 5-visualization suite built entirely from open scientific datasets — no borrowed
imagery, no copyrighted assets. Original code, original renders.

## Goal

Recreate the visual language of a professional data-art installation using
Python + free NASA/Copernicus/HydroSHEDS data, packaged as a Streamlit dashboard
and portfolio-ready GitHub repo.

## Timeline — 4 weeks

| Week | Phase | Output |
|---|---|---|
| 1 | Environment + data acquisition | All accounts registered, all raw data downloaded |
| 2 | Core visualizations | Slide 1 (globe), Slide 2 (migration), Slide 3 (rivers) as PNGs |
| 3 | Climate visualizations | Slide 4 (ocean), Slide 5 (sea ice) as PNG + GIF |
| 4 | Dashboard + polish | Streamlit app deployed, GitHub repo published |

## The 5 slides

1. **Earth overview** — glowing globe, ocean + coastlines. Data: Natural Earth, NASA EPIC.
2. **Species migration** — 20 species tracked (albatross, blue whale, penguin, turtle...). Data: Movebank, OBIS-SEAMAP.
3. **River networks** — glowing cyan river veins. Data: HydroRIVERS / HydroSHEDS.
4. **Ocean currents + temperature** — SST + chlorophyll blooms. Data: Copernicus GLORYS12V1, NASA Aqua-MODIS.
5. **Sea ice cycle** — Arctic/Antarctic annual freeze-thaw, animated. Data: NSIDC Sea Ice CDR.

## Definition of done

- [ ] All 5 static visualizations exported as 300dpi PNG
- [ ] Sea ice animation exported as GIF
- [ ] Streamlit dashboard runs locally and is deployed publicly
- [ ] README with data source citations for every slide
- [ ] Repo pushed to github.com/Abhisar-else
- [ ] No copyrighted/borrowed images anywhere in the repo

## See also

- [SETUP.md](./SETUP.md) — environment + install instructions
- [DATA_SOURCES.md](./DATA_SOURCES.md) — every dataset, where to get it, how to register
- [DESIGN_TOKENS.md](./DESIGN_TOKENS.md) — colors, typography, export specs
- [PROGRESS.md](./PROGRESS.md) — running log, update as you go
