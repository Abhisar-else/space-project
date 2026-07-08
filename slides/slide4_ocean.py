# slides/slide4_ocean.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from utils.colors import BG_COLOR, SST_COLD, SST_MID, SST_WARM, apply_dark_style
from utils.generators import load_ocean_sst_data

def render_ocean_sst(output_path="outputs/slide4_ocean.png"):
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)
    
    lons, lats, sst = load_ocean_sst_data()
    
    # Custom thermal color scale matching design guidelines
    cmap = LinearSegmentedColormap.from_list("custom_thermal", [SST_COLD, SST_MID, SST_WARM])
    
    im = ax.pcolormesh(lons, lats, sst, cmap=cmap, shading='auto')
    
    # Overlay vector currents
    Y, X = np.meshgrid(lats[::5], lons[::10])
    U = np.cos(Y / 10) * 5
    V = np.sin(X / 20) * 3
    ax.quiver(X, Y, U, V, color='#ffffff', alpha=0.25, scale=50, width=0.0015)
    
    # Custom colorbar styling
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, shrink=0.6)
    cbar.set_label("Sea Surface Temperature (°C)", color='#aaaaaa', fontsize=10)
    cbar.ax.xaxis.set_tick_params(color='#888888', labelcolor='#888888')
    
    ax.set_title("OCEAN THERMAL DYNAMICS\nGlobal SST & Vector Current Flow", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_ocean_sst()
