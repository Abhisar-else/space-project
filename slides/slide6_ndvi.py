# slides/slide6_ndvi.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from utils.colors import BG_COLOR, NDVI_LOW, NDVI_MID, NDVI_HIGH, apply_dark_style
from utils.generators import load_ndvi_data


def render_ndvi(output_path="outputs/slide6_ndvi.png"):
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)

    lons, lats, ndvi = load_ndvi_data()
    cmap = LinearSegmentedColormap.from_list("custom_ndvi", [NDVI_LOW, NDVI_MID, NDVI_HIGH])
    im = ax.pcolormesh(lons, lats, ndvi, cmap=cmap, shading='auto', vmin=-1, vmax=1)

    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, shrink=0.6)
    cbar.set_label("NDVI (vegetation index)", color='#aaaaaa', fontsize=10)
    cbar.ax.xaxis.set_tick_params(color='#888888', labelcolor='#888888')

    ax.set_title("VEGETATION INDEX\nRasterio-Derived NDVI Field", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    render_ndvi()