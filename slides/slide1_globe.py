# slides/slide1_globe.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from utils.colors import BG_COLOR, DEEP_OCEAN, apply_dark_style
import cartopy
cartopy.config['data_dir'] = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'naturalearth')
)

def render_globe(output_path="outputs/slide1_globe.png"):
    apply_dark_style()
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=20))
    
    # Set background colors
    ax.set_facecolor(BG_COLOR)
    # Support older cartopy/matplotlib facecolor setting
    try:
        ax.background_patch.set_facecolor(BG_COLOR)
    except AttributeError:
        ax.patch.set_facecolor(BG_COLOR)
    
    # Draw oceans and land
    from utils.generators import load_natural_earth
    ocean_gdf = load_natural_earth("ocean")
    land_gdf = load_natural_earth("land")

    if ocean_gdf is not None and land_gdf is not None:
        ax.add_geometries(ocean_gdf.geometry, crs=ccrs.PlateCarree(), facecolor=DEEP_OCEAN, edgecolor='none')
        ax.add_geometries(land_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='#0d1b2a', edgecolor='#00b4ff', linewidth=0.3)
    else:
        ax.add_feature(cfeature.OCEAN, facecolor=DEEP_OCEAN, edgecolor='none')
        ax.add_feature(cfeature.LAND, facecolor='#0d1b2a', edgecolor='#00b4ff', linewidth=0.3)
    ax.add_feature(cfeature.COASTLINE, edgecolor='#00b4ff', linewidth=0.5)
    
    # Add gridlines matching the river glow color
    ax.gridlines(draw_labels=False, linewidth=0.2, color='#00b4ff', alpha=0.5, linestyle='--')
    
    ax.set_title("EARTH OVERVIEW\nDeep Planet Oceans & Continents", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_globe()
