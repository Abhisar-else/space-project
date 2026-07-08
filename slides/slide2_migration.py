# slides/slide2_migration.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from utils.colors import BG_COLOR, SPECIES_COLORS, apply_dark_style
from utils.generators import generate_migration_tracks

def render_migration(output_path="outputs/slide2_migration.png"):
    apply_dark_style()
    fig = plt.figure(figsize=(10, 10), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    
    ax.set_facecolor(BG_COLOR)
    try:
        ax.background_patch.set_facecolor(BG_COLOR)
    except AttributeError:
        ax.patch.set_facecolor(BG_COLOR)
    
    # Underlay simple dark land
    from utils.generators import load_natural_earth
    land_gdf = load_natural_earth("land")
    if land_gdf is not None:
        ax.add_geometries(land_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='#020c1b', edgecolor='none')
        ax.add_geometries(land_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='#001f3f', linewidth=0.3)
    else:
        ax.add_feature(cfeature.LAND, facecolor='#020c1b', edgecolor='none')
        ax.add_feature(cfeature.COASTLINE, edgecolor='#001f3f', linewidth=0.3)
    # Generate and plot migration paths
    from utils.generators import load_movebank_migration
    df = load_movebank_migration()
    if df is None:
        df = generate_migration_tracks()
    df = df.sort_values("timestamp")
    for species, group in df.groupby("species"):
        group = group.sort_values("timestamp")
        color = SPECIES_COLORS.get("blue_whale", "#00b4d8")
        ax.plot(group["longitude"], group["latitude"], transform=ccrs.PlateCarree(),
                color=color, linewidth=3, alpha=0.15)
        ax.plot(group["longitude"], group["latitude"], transform=ccrs.PlateCarree(),
                color=color, linewidth=1, alpha=0.9)
        ax.scatter(group["longitude"].iloc[-1], group["latitude"].iloc[-1],
                   transform=ccrs.PlateCarree(), color=color, s=15, edgecolors='#ffffff', zorder=5, linewidth=0.5)
    ax.set_title("SPECIES MIGRATION\nGlobal Animal Tracking & Migration Paths", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_migration()
