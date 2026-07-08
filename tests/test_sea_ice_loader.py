import sys
from pathlib import Path

import numpy as np
import xarray as xr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.generators import load_sea_ice_data


def test_load_sea_ice_data_clips_concentration_to_0_100(tmp_path):
    data_path = tmp_path / "seaice.nc"
    lons = np.array([0.0, 1.0])
    lats = np.array([60.0, 61.0])
    values = np.array([[[1.2, -0.1]], [[0.4, 1.1]]])
    ds = xr.Dataset(
        data_vars={"siconc": (("time", "lat", "lon"), values)},
        coords={"time": np.array([0, 1]), "lat": lats, "lon": lons},
    )
    ds.to_netcdf(data_path)

    loaded_lons, loaded_lats, cycles = load_sea_ice_data(data_dir=tmp_path)

    assert np.allclose(loaded_lons, lons)
    assert np.allclose(loaded_lats, lats)
    assert np.nanmin(cycles) >= 0
    assert np.nanmax(cycles) <= 100
    assert cycles.shape == values.shape
