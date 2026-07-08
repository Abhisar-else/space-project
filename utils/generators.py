# utils/generators.py
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import LineString


def generate_migration_tracks(num_species=4, points_per_track=100):
    data = []
    species_list = ["albatross", "blue_whale", "emperor_penguin", "loggerhead_turtle"]
    for i in range(min(num_species, len(species_list))):
        sp = species_list[i]
        lon, lat = np.random.uniform(-180, 180), np.random.uniform(-60, 60)
        for step in range(points_per_track):
            lon += np.random.normal(0, 2)
            lat += np.random.normal(0, 1.5)
            lon = (lon + 180) % 360 - 180
            lat = np.clip(lat, -85, 85)
            data.append({
                "species": sp,
                "longitude": lon,
                "latitude": lat,
                "timestamp": pd.Timestamp("2026-07-01") + pd.Timedelta(hours=step)
            })
    return pd.DataFrame(data)


def generate_river_network():
    lines = []
    coords = [(x, np.sin(x / 10) * 5) for x in np.linspace(-100, 100, 50)]
    lines.append(LineString(coords))
    for i in range(5):
        start_idx = np.random.randint(10, 40)
        start_pt = coords[start_idx]
        trib_coords = [start_pt]
        offset_y = np.random.choice([-1, 1])
        for x_offset in range(1, 10):
            pt = (start_pt[0] + x_offset * 3, start_pt[1] + offset_y * (x_offset * 1.5 + np.random.normal(0, 0.5)))
            trib_coords.append(pt)
        lines.append(LineString(trib_coords))
    return gpd.GeoDataFrame(geometry=lines)


def generate_sst_grid():
    """Create a climatology-like SST field using observed broad-scale patterns.

    The field combines:
    - a latitudinal temperature gradient that is warmest near the equator
    - a zonal structure that makes eastern boundary upwelling regions cooler
    - a modest warm anomaly in the western tropical Pacific and Atlantic
    """
    lons = np.linspace(-180, 180, 180)
    lats = np.linspace(-90, 90, 90)
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Baseline from latitude: warm tropics, cold poles
    sst = 30 - 0.6 * np.abs(lat_grid)

    # Stronger cooling in eastern boundary upwelling regions (e.g. Peru/California/Canary)
    eastern_cooling = 6 * np.exp(-((lon_grid + 80) / 20) ** 2) + 5 * np.exp(-((lon_grid - 120) / 20) ** 2)
    eastern_cooling += 4 * np.exp(-((lon_grid + 20) / 20) ** 2)

    # Warm western tropical Pacific/Atlantic anomaly to mimic warm pool behavior
    warm_pool = 2.2 * np.exp(-((lon_grid - 160) / 25) ** 2) * np.exp(-(lat_grid / 22) ** 2)
    warm_pool += 1.5 * np.exp(-((lon_grid - 30) / 25) ** 2) * np.exp(-(lat_grid / 20) ** 2)

    sst = sst - eastern_cooling + warm_pool
    sst = np.clip(sst, -2, 35)
    return lons, lats, sst


def load_ocean_sst_data(data_dir="data", pattern="*.nc"):
    """Load a local NetCDF SST dataset if present; otherwise try a real Copernicus download and fall back gracefully."""
    search_dir = Path(data_dir)
    search_dir.mkdir(parents=True, exist_ok=True)

    candidates = sorted(search_dir.rglob(pattern))
    for path in candidates:
        try:
            ds = xr.open_dataset(path)
            if "sst" in ds.data_vars:
                sst = ds["sst"].to_numpy()
                lons = np.asarray(ds["lon"].to_numpy())
                lats = np.asarray(ds["lat"].to_numpy())
                if sst.ndim == 2:
                    ds.close()
                    return lons, lats, sst
            ds.close()
        except Exception as exc:
            print(f"Ocean SST load failed for {path}: {exc}")

    try:
        import os
        from dotenv import load_dotenv

        load_dotenv()
        username = os.getenv("COPERNICUS_USERNAME")
        password = os.getenv("COPERNICUS_PASSWORD")
        if username and password:
            import subprocess
            output_path = search_dir / "glorys_sst.nc"
            cmd = [
                "copernicusmarine",
                "subset",
                "--dataset-id",
                "cmems_mod_glo_phy_my_0.083deg_P1D-m",
                "--variable",
                "thetao",
                "--start-date",
                "2023-01-01",
                "--end-date",
                "2023-01-02",
                "--north",
                "60",
                "--south",
                "-60",
                "--east",
                "180",
                "--west",
                "-180",
                "--output-dir",
                str(search_dir),
                "--force-download",
            ]
            subprocess.run(cmd, check=False, capture_output=True, text=True)
            if output_path.exists():
                ds = xr.open_dataset(output_path)
                if "thetao" in ds.data_vars:
                    sst = ds["thetao"].mean(dim="depth", keep_attrs=True).to_numpy()
                    lons = np.asarray(ds["longitude"].to_numpy())
                    lats = np.asarray(ds["latitude"].to_numpy())
                    if sst.ndim == 2:
                        ds.close()
                        return lons, lats, sst
                ds.close()
    except Exception as exc:
        print(f"Copernicus SST download failed: {exc}")

    return generate_sst_grid()


def load_sea_ice_data(data_dir="data", pattern="*.nc"):
    """Load a local sea-ice NetCDF dataset if present; otherwise fall back to the synthetic sequence."""
    search_dir = Path(data_dir)
    search_dir.mkdir(parents=True, exist_ok=True)

    candidates = sorted(search_dir.rglob(pattern))
    for path in candidates:
        try:
            ds = xr.open_dataset(path)
            for var_name in ("siconc", "sea_ice_fraction", "ice_conc"):
                if var_name in ds.data_vars:
                    data = np.asarray(ds[var_name].to_numpy())
                    lons = np.asarray(ds["lon"].to_numpy()) if "lon" in ds.coords else np.linspace(-180, 180, data.shape[-1])
                    lats = np.asarray(ds["lat"].to_numpy()) if "lat" in ds.coords else np.linspace(50, 90, data.shape[-2])
                    if data.ndim >= 2:
                        data = np.clip(data * 100, 0, 100)
                        ds.close()
                        return lons, lats, data
            ds.close()
        except Exception as exc:
            print(f"Sea ice load failed for {path}: {exc}")

    return generate_sea_ice_cycle()


def generate_sea_ice_cycle(frames=12):
    """Create a seasonal Arctic sea-ice cycle inspired by observed annual growth and melt.

    The pattern uses a stronger northward ice edge in winter and a retreat in summer,
    with a broad high-latitude band rather than a single sharp boundary.
    """
    lons = np.linspace(-180, 180, 100)
    lats = np.linspace(50, 90, 50)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    cycles = []

    for f in range(frames):
        phase = 2 * np.pi * f / frames
        # Seasonal ice edge follows a realistic annual cycle peaking in late winter.
        min_lat = 70 + 9 * np.sin(phase - np.pi / 2)
        edge_width = 8 + 3 * np.cos(phase)
        ice_edge = (lat_grid - min_lat) / edge_width
        concentration = np.clip(100 * (1 / (1 + np.exp(-ice_edge))) - 25, 0, 100)

        # Add a modest longitudinal modulation to mimic basin differences.
        basin_modulation = 8 * np.sin((lon_grid / 180) * np.pi + phase / 2)
        concentration = np.clip(concentration + basin_modulation, 0, 100)
        cycles.append(concentration)
    return lons, lats, cycles


def load_hydrorivers(data_dir="data/hydrorivers", gbd_name="HydroRIVERS_v10.gdb", layer="HydroRIVERS_v10", max_ord_flow=4):
    """Load real HydroRIVERS global network from a File Geodatabase, filtered to major rivers only."""
    path = Path(data_dir) / gbd_name
    if path.exists():
        try:
            return gpd.read_file(path, layer=layer, where=f"ORD_FLOW <= {max_ord_flow}")
        except Exception as exc:
            print(f"HydroRIVERS load failed: {exc}")
    return None


def load_river_network(shapefile_path="data/hydrorivers/HydroRIVERS_v10.shp", min_order=6):
    """Load real HydroRIVERS data; falls back to synthetic if missing."""
    if not Path(shapefile_path).exists():
        return generate_river_network()
    try:
        gdf = gpd.read_file(shapefile_path)
        if "ORD_FLOW" in gdf.columns:
            gdf = gdf[gdf["ORD_FLOW"] <= min_order]
        return gdf[["geometry"]]
    except Exception:
        return generate_river_network()


def load_natural_earth(feature, data_dir="data/naturalearth/shapefiles/natural_earth/physical"):
    """Load a local Natural Earth 110m shapefile. Returns None if not found."""
    path = Path(data_dir) / f"ne_110m_{feature}.shp"
    if path.exists():
        return gpd.read_file(path)
    return None


def load_epic_image(date=None):
    """Fetch a NASA EPIC full-disk Earth image metadata for a given date."""
    import os
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        return None

    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}
    if date:
        url += f"/date/{date}"

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        print(f"EPIC load failed: {exc}")
        return None


def download_epic_image(entry, save_dir="data/epic_cache"):
    """Download the actual PNG for one EPIC entry."""
    import os
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key or not entry:
        return None

    date_str = entry["date"].split(" ")[0].replace("-", "/")
    image_name = entry["image"]
    url = f"https://api.nasa.gov/EPIC/archive/natural/{date_str}/png/{image_name}.png"

    Path(save_dir).mkdir(parents=True, exist_ok=True)
    local_path = Path(save_dir) / f"{image_name}.png"

    try:
        resp = requests.get(url, params={"api_key": api_key}, timeout=15)
        resp.raise_for_status()
        local_path.write_bytes(resp.content)
        return str(local_path)
    except Exception as exc:
        print(f"EPIC image download failed: {exc}")
        return None


def list_movebank_studies(species_search=None):
    """List Movebank studies accessible with current credentials."""
    import os
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    username = os.getenv("MOVEBANK_USERNAME")
    password = os.getenv("MOVEBANK_PASSWORD")
    if not username or not password:
        return None

    url = "https://www.movebank.org/movebank/service/direct-read"
    params = {"entity_type": "study"}
    if species_search:
        params["i_can_see_data"] = "true"

    try:
        resp = requests.get(url, params=params, auth=(username, password), timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        print(f"Movebank study list failed: {exc}")
        return None


def fetch_movebank_locations(study_id):
    """Fetch real location data for a Movebank study."""
    import os
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    username = os.getenv("MOVEBANK_USERNAME")
    password = os.getenv("MOVEBANK_PASSWORD")
    if not username or not password:
        return None

    url = "https://www.movebank.org/movebank/service/direct-read"
    params = {"entity_type": "event", "study_id": study_id}

    try:
        resp = requests.get(url, params=params, auth=(username, password), timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        print(f"Movebank location fetch failed: {exc}")
        return None
def load_movebank_migration(study_id=1027467132, data_dir="data/movebank"):
    """Load real Movebank tracking data as a DataFrame matching the shape
    generate_migration_tracks() produces. Falls back to None if unavailable."""
    import io
    import pandas as pd
    from pathlib import Path

    # Try local cached CSV first (from manual download or prior fetch)
    cache_path = Path(data_dir) / f"study_{study_id}.csv"
    if cache_path.exists():
        try:
            df = pd.read_csv(cache_path)
        except Exception as exc:
            print(f"Movebank cache read failed: {exc}")
            df = None
    else:
        df = None

    if df is None:
        text = fetch_movebank_locations(study_id)
        if not text:
            return None
        try:
            df = pd.read_csv(io.StringIO(text))
            Path(data_dir).mkdir(parents=True, exist_ok=True)
            df.to_csv(cache_path, index=False)
        except Exception as exc:
            print(f"Movebank parse failed: {exc}")
            return None

    if not {"location_lat", "location_long", "individual_id", "timestamp"}.issubset(df.columns):
        return None

    out = pd.DataFrame({
        "species": "blue_fin_whale_" + df["individual_id"].astype(str),
        "longitude": df["location_long"],
        "latitude": df["location_lat"],
        "timestamp": pd.to_datetime(df["timestamp"]),
    })
    return out
def load_movebank_migration(study_id=1027467132, data_dir="data/movebank"):
    """Load real Movebank tracking data as a DataFrame matching the shape
    generate_migration_tracks() produces. Falls back to None if unavailable."""
    import io
    import pandas as pd
    from pathlib import Path

    cache_path = Path(data_dir) / f"study_{study_id}.csv"
    if cache_path.exists():
        try:
            df = pd.read_csv(cache_path)
        except Exception as exc:
            print(f"Movebank cache read failed: {exc}")
            df = None
    else:
        df = None

    if df is None:
        text = fetch_movebank_locations(study_id)
        if not text:
            return None
        try:
            df = pd.read_csv(io.StringIO(text))
            Path(data_dir).mkdir(parents=True, exist_ok=True)
            df.to_csv(cache_path, index=False)
        except Exception as exc:
            print(f"Movebank parse failed: {exc}")
            return None

    if not {"location_lat", "location_long", "individual_id", "timestamp"}.issubset(df.columns):
        return None

    out = pd.DataFrame({
        "species": "blue_fin_whale_" + df["individual_id"].astype(str),
        "longitude": df["location_long"],
        "latitude": df["location_lat"],
        "timestamp": pd.to_datetime(df["timestamp"]),
    })
    return out
def load_ocean_sst_data(data_dir="data", pattern="*.nc"):
    """Load a local NetCDF SST dataset if present; otherwise fall back to the synthetic generator."""
    search_dir = Path(data_dir)
    if not search_dir.exists():
        return generate_sst_grid()

    candidates = sorted(search_dir.rglob(pattern))
    for path in candidates:
        try:
            ds = xr.open_dataset(path)
            # Support both generic "sst" and Copernicus GLORYS "thetao" variable names
            var_name = "sst" if "sst" in ds.data_vars else ("thetao" if "thetao" in ds.data_vars else None)
            if var_name:
                data = ds[var_name]
                # Select first timestep and surface depth layer if present
                if "time" in data.dims:
                    data = data.isel(time=0)
                if "depth" in data.dims:
                    data = data.isel(depth=0)
                sst = data.to_numpy()
                lat_name = "lat" if "lat" in ds.coords else "latitude"
                lon_name = "lon" if "lon" in ds.coords else "longitude"
                lons = np.asarray(ds[lon_name].to_numpy())
                lats = np.asarray(ds[lat_name].to_numpy())
                if sst.ndim == 2:
                    ds.close()
                    return lons, lats, sst
            ds.close()
        except Exception as exc:
            print(f"Ocean SST load failed for {path}: {exc}")

    return generate_sst_grid()
def load_sea_ice_data(data_dir="data", pattern="*seaice*.nc"):
    """Load real sea ice concentration frames from a local NetCDF file
    (e.g. Copernicus GLORYS siconc). Falls back to the synthetic cycle if missing."""
    search_dir = Path(data_dir)
    if not search_dir.exists():
        return generate_sea_ice_cycle()

    candidates = sorted(search_dir.rglob(pattern))
    for path in candidates:
        try:
            ds = xr.open_dataset(path)
            if "siconc" in ds.data_vars:
                data = ds["siconc"]
                lat_name = "lat" if "lat" in ds.coords else "latitude"
                lon_name = "lon" if "lon" in ds.coords else "longitude"
                lons = np.asarray(ds[lon_name].to_numpy())
                lats = np.asarray(ds[lat_name].to_numpy())

                if "time" in data.dims:
                    frames = [np.clip(data.isel(time=t).to_numpy() * 100, 0, 100) for t in range(data.sizes["time"])]
                else:
                    frames = [np.clip(data.to_numpy() * 100, 0, 100)]

                if len(frames) > 0 and frames[0].ndim == 2:
                    ds.close()
                    return lons, lats, frames
            ds.close()
        except Exception as exc:
            print(f"Sea ice load failed for {path}: {exc}")

    return generate_sea_ice_cycle()