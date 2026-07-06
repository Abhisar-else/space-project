# Setup

## 1. Create environment (conda recommended)

Cartopy has C-library dependencies that pip frequently fails to build on
Windows. Conda avoids this entirely.

```bash
conda create -n nasaviz python=3.11 -y
conda activate nasaviz
conda install -c conda-forge cartopy geopandas xarray netcdf4 -y
pip install matplotlib cmocean imageio pandas numpy shapely pyproj requests streamlit
```

## 2. If you must use pip only

```bash
pip install matplotlib geopandas xarray netCDF4 requests pillow \
    cmocean imageio scipy pandas numpy shapely pyproj streamlit
pip install cartopy --no-binary cartopy
```

## 3. Verify install

```bash
python -c "
import matplotlib, cartopy, geopandas, xarray, cmocean
print('OK:', matplotlib.__version__, cartopy.__version__, geopandas.__version__)
"
```

## 4. Accounts needed (all free)

| Service | Why | Link |
|---|---|---|
| NASA API | EPIC + APOD imagery | api.nasa.gov |
| NASA Earthdata | NSIDC sea ice access | urs.earthdata.nasa.gov |
| Copernicus Marine | GLORYS ocean + ice data | marine.copernicus.eu |
| Movebank | Species migration CSVs | movebank.org |

## 5. Download raw data (do this once)

```bash
cd data
# HydroRIVERS shapefile — download manually from:
# https://www.hydrosheds.org/products/hydrorivers
# unzip into data/hydrorivers/

# GLORYS + NSIDC — downloaded via Copernicus/Earthdata portals (see DATA_SOURCES.md)
```

## 6. Run a slide script

```bash
python slides/slide3_rivers.py
# check outputs/slide3_rivers.png
```

## 7. Run the dashboard

```bash
streamlit run app.py
```
