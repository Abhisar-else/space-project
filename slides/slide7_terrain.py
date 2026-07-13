# slides/slide7_terrain.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from utils.colors import BG_COLOR, TERRAIN_SHADOW, TERRAIN_MID, TERRAIN_LIT, apply_dark_style
from utils.generators import load_dem_hillshade


def render_terrain(output_path="outputs/slide7_terrain.png"):
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)

    lons, lats, shaded = load_dem_hillshade()
    cmap = LinearSegmentedColormap.from_list("custom_terrain", [TERRAIN_SHADOW, TERRAIN_MID, TERRAIN_LIT])
    im = ax.pcolormesh(lons, lats, shaded, cmap=cmap, shading='auto', vmin=0, vmax=1)
    ax.set_aspect('equal')
    ax.axis('off')

    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.08, shrink=0.6)
    cbar.set_label("Hillshade (sun altitude 45°, azimuth 315°)", color='#aaaaaa', fontsize=10)
    cbar.ax.xaxis.set_tick_params(color='#888888', labelcolor='#888888')

    ax.set_title("TERRAIN & HILLSHADE\nGDAL-Processed Digital Elevation Model", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    render_terrain()