# utils/generators.py
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

def generate_migration_tracks(num_species=4, points_per_track=100):
    data = []
    species_list = ["albatross", "blue_whale", "emperor_penguin", "loggerhead_turtle"]
    for i in range(min(num_species, len(species_list))):
        sp = species_list[i]
        # Starting point
        lon, lat = np.random.uniform(-180, 180), np.random.uniform(-60, 60)
        for step in range(points_per_track):
            lon += np.random.normal(0, 2)
            lat += np.random.normal(0, 1.5)
            # Wrap longitude around [-180, 180]
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
    # Main channel
    coords = [(x, np.sin(x/10) * 5) for x in np.linspace(-100, 100, 50)]
    lines.append(LineString(coords))
    # Tributaries
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
    lons = np.linspace(-180, 180, 180)
    lats = np.linspace(-90, 90, 90)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    # Temperature decreases with absolute latitude, plus some noise/current patterns
    sst = 30 * np.cos(np.radians(lat_grid)) - 2
    sst += np.sin(lon_grid/20) * 3
    sst = np.clip(sst, -2, 35)
    return lons, lats, sst

def generate_sea_ice_cycle(frames=12):
    lons = np.linspace(-180, 180, 100)
    lats = np.linspace(50, 90, 50)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    cycles = []
    for f in range(frames):
        phase = 2 * np.pi * f / frames
        # Extent varies sinusoidally
        min_lat = 70 + 10 * np.sin(phase)
        concentration = np.clip((lat_grid - min_lat) / (90 - min_lat) * 100, 0, 100)
        cycles.append(concentration)
    return lons, lats, cycles
def load_hydrorivers(data_dir="data/hydrorivers", filename="HydroRIVERS_v10.shp"):
    """Load real HydroRIVERS global network. Returns None if missing,
    so callers fall back to generate_river_network()."""
    import os
    import geopandas as gpd

    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        return gpd.read_file(path)
    return None