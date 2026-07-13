# Progress log

Updated after reviewing the repository implementation and generated output assets.

## Week 1 — Environment + data

- [x] Project structure created with reusable utilities and slide modules
- [x] NASA API key obtained for the EPIC workflow
- [x] NASA Earthdata account registered for the climate-data workflow
- [x] Copernicus Marine account registered and client installed locally
- [x] Movebank account access checked and the migration workflow is implemented with fallback handling
- [x] HydroRIVERS data directory present locally in data/hydrorivers

## Week 2 — Core visualizations

- [x] Slide 1 — Earth globe rendered
- [x] Slide 2 — Species migration rendered
- [x] Slide 3 — River network rendered

## Week 3 — Climate visualizations

- [x] Slide 4 — Ocean SST rendered
- [x] Slide 4 — Copernicus-style SST loader added with NetCDF support and synthetic fallback
- [x] Slide 5 — Sea ice GIF rendered
- [x] Slide 5 — Sea-ice loader added with NetCDF support and synthetic fallback
- [x] Climate slides verified by local render command

## Week 4 — Dashboard + ship

- [x] Streamlit app.py built and wired to all five slides
- [x] Local dashboard verified through the Streamlit app
- [ ] EONET live layer added (optional stretch)
- [x] README created and populated with project overview and docs
- [x] Pushed to GitHub   <!-- confirmed live, was unchecked -->
## Week 5 — GIS toolkit additions
- [x] Fixed duplicate function defs in utils/generators.py
- [x] Fixed broken requirements.txt (-dotenv typo)
- [x] Slide 6 — Rasterio NDVI demo (synthetic fallback) built + wired into app.py
- [ ] Real Sentinel-2/Landsat NDVI integration
- [ ] Slide 7 — GDAL DEM/hillshade demo
- [ ] git rm reqirments.txt + untrack outputs/
- [ ] Deployed on Streamlit Community Cloud

## Verification notes

- Reviewed implementation in app.py, utils/colors.py, utils/generators.py, slides/slide1_globe.py, slides/slide2_migration.py, slides/slide3_rivers.py, slides/slide4_ocean.py, and slides/slide5_seaice.py.
- Confirmed output artifacts exist in outputs/ for slides 1–5.
- Verified the latest climate-slide render command completed successfully.

## Blockers / notes

- Remote repository is configured as origin, but no push/deployment verification was performed in this review.
