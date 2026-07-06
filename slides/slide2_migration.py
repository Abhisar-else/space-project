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
    ax.add_feature(cfeature.LAND, facecolor='#020c1b', edgecolor='none')
    ax.add_feature(cfeature.COASTLINE, edgecolor='#001f3f', linewidth=0.3)
    
    # Generate and plot migration paths
    df = generate_migration_tracks()
    for species, group in df.groupby("species"):
        color = SPECIES_COLORS.get(species, "#ffffff")
        # Format label name
        label_name = species.replace("_", " ").title()
        ax.plot(group["longitude"], group["latitude"], transform=ccrs.PlateCarree(),
                color=color, linewidth=1.5, alpha=0.8, label=label_name)
        # Glowing endpoint
        ax.scatter(group["longitude"].iloc[-1], group["latitude"].iloc[-1],
                   transform=ccrs.PlateCarree(), color=color, s=20, edgecolors='#ffffff', zorder=5)
    
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False, fontsize=8)
    ax.set_title("SPECIES MIGRATION\nGlobal Animal Tracking & Migration Paths", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_migration()
