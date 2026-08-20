import sys
import types
from pathlib import Path

import numpy as np
import xarray as xr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.generators import load_sea_ice_data


def test_load_sea_ice_data_clips_concentration_to_0_100(tmp_path):
    data_path = tmp_path / "seaice.nc"
    lons = np.array([0.0, 1.0])
    lats = np.array([60.0, 61.0])
    values = np.array([[[1.2, -0.1], [0.4, 1.1]], [[0.9, 0.2], [0.5, 0.8]]])
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
    assert len(cycles) == values.shape[0]
    assert cycles[0].shape == values.shape[1:]


def test_load_sea_ice_data_downloads_copernicus_data_when_no_local_file(tmp_path, monkeypatch):
    lons = np.array([0.0, 1.0])
    lats = np.array([60.0, 61.0])
    values = np.array([[[0.4, 1.2], [0.1, -0.2]]])

    def subset(**kwargs):
        assert kwargs["dataset_id"] == "cmems_mod_glo_phy_my_0.083deg_P1M-m"
        assert kwargs["variables"] == ["siconc"]
        output_path = Path(kwargs["output_directory"]) / kwargs["output_filename"]
        xr.Dataset(
            data_vars={"siconc": (("time", "lat", "lon"), values)},
            coords={"time": [0], "lat": lats, "lon": lons},
        ).to_netcdf(output_path)

    monkeypatch.setattr("os.getenv", lambda key: "value" if key.startswith("COPERNICUS_") else None)
    monkeypatch.setitem(sys.modules, "copernicusmarine", types.SimpleNamespace(subset=subset))

    loaded_lons, loaded_lats, cycles = load_sea_ice_data(data_dir=tmp_path)

    assert np.allclose(loaded_lons, lons)
    assert np.allclose(loaded_lats, lats)
    assert len(cycles) == 1
    assert np.nanmin(cycles[0]) >= 0
    assert np.nanmax(cycles[0]) <= 100
