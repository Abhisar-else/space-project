import sys
from pathlib import Path

import numpy as np
import xarray as xr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.generators import generate_sst_grid, load_ocean_sst_data, load_sea_ice_data


def test_load_ocean_sst_data_falls_back_when_no_real_file(tmp_path):
    result = load_ocean_sst_data(data_dir=tmp_path)
    lons, lats, sst = result

    assert lons.shape[0] > 0
    assert lats.shape[0] > 0
    assert sst.shape == (len(lats), len(lons))


def test_realistic_sst_grid_has_strong_tropical_contrast():
    lons, lats, sst = generate_sst_grid()
    equator_idx = int(np.argmin(np.abs(lats)))
    warm_lon_idx = int(np.argmin(np.abs(lons - 160)))
    cool_lon_idx = int(np.argmin(np.abs(lons + 80)))

    assert sst[equator_idx, warm_lon_idx] - sst[equator_idx, cool_lon_idx] > 6


def test_load_sea_ice_data_clips_to_realistic_concentration_range(tmp_path):
    data_path = tmp_path / "seaice.nc"
    lons = np.linspace(-180, 180, 3)
    lats = np.linspace(60, 90, 2)
    values = np.array([[1.2, 0.1, 0.0], [0.8, 1.0, 0.5]])
    ds = xr.Dataset(
        data_vars={"siconc": (("lat", "lon"), values)},
        coords={"lat": lats, "lon": lons},
    )
    ds.to_netcdf(data_path)

    result = load_sea_ice_data(data_dir=tmp_path)
    loaded_lons, loaded_lats, loaded_data = result

    assert np.allclose(loaded_lons, lons)
    assert np.allclose(loaded_lats, lats)
    assert np.nanmax(loaded_data) <= 100
    assert np.nanmin(loaded_data) >= 0


def test_load_ocean_sst_data_reads_local_netcdf(tmp_path):
    data_path = tmp_path / "sample.nc"
    lons = np.linspace(-180, 180, 5)
    lats = np.linspace(-80, 80, 4)
    sst = np.array([[18.0, 19.0, 20.0, 21.0, 22.0],
                    [20.0, 21.0, 22.0, 23.0, 24.0],
                    [22.0, 23.0, 24.0, 25.0, 26.0],
                    [24.0, 25.0, 26.0, 27.0, 28.0]])
    ds = xr.Dataset(
        data_vars={"sst": (("lat", "lon"), sst)},
        coords={"lat": lats, "lon": lons},
    )
    ds.to_netcdf(data_path)

    result = load_ocean_sst_data(data_dir=tmp_path)
    loaded_lons, loaded_lats, loaded_sst = result

    assert np.allclose(loaded_lons, lons)
    assert np.allclose(loaded_lats, lats)
    assert np.allclose(loaded_sst, sst)
