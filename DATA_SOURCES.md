# Data sources

Every dataset used, exactly where to get it, and what it feeds.

## Slide 1 — Earth overview

| Source | Type | Access |
|---|---|---|
| Natural Earth | Land/ocean vector boundaries | Free download, naturalearthdata.com |
| NASA EPIC | Full-disk Earth photos (DSCOVR satellite) | api.nasa.gov/planetary/earth/imagery |

## Slide 2 — Species migration

| Source | Type | Access |
|---|---|---|
| Movebank | Animal tracking CSVs (albatross, whales, turtles) | Free account, movebank.org |
| OBIS-SEAMAP (Duke) | Marine species observations | seamap.env.duke.edu |
| EuroBIS / VLIZ | European marine biodiversity tracking | vliz.be/en/eurobis |
| SCAR Antarctic Tracking | Antarctic species movement data | scar.org |

## Slide 3 — River networks

| Source | Type | Access |
|---|---|---|
| HydroRIVERS / HydroSHEDS | Global river vector geometry | Free download, hydrosheds.org |
| NASA SWOT | Surface water extent/seasonality | podaac.jpl.nasa.gov (SWOT mission) |

## Slide 4 — Ocean currents + temperature

| Source | Type | Access |
|---|---|---|
| Copernicus Marine GLORYS12V1 | Ocean reanalysis, 8km res, currents+SST+sea level | Free account, marine.copernicus.eu; loader supports local NetCDF files in data/ |
| NASA Aqua-MODIS | Chlorophyll-a / phytoplankton | oceancolor.gsfc.nasa.gov |

## Slide 5 — Sea ice

| Source | Type | Access |
|---|---|---|
| NSIDC Sea Ice Index (CDR) | Monthly ice concentration grids, 1979–present | nsidc.org/data/G02202; loader supports local NetCDF files in data/ |
| Copernicus GLORYS (siconc) | Alternative ice concentration source | marine.copernicus.eu |

## Notes

- All sources are free and open — no paid API tiers required for this project scope.
- Movebank requires a free account and, for some datasets, permission requests
  from the data owner — apply early, this can take a few days.
- Copernicus Marine and NASA Earthdata both use OAuth-style tokens — store
  credentials in a local `.env` file, never commit them.
