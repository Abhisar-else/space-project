# slides/slide3_rivers.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from utils.colors import BG_COLOR, RIVER_GLOW, RIVER_CORE, apply_dark_style
from utils.generators import generate_river_network

def render_rivers(output_path="outputs/slide3_rivers.png"):
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)
    
    gdf = generate_river_network()
    # Draw outer glow
    gdf.plot(ax=ax, color=RIVER_GLOW, linewidth=4, alpha=0.2)
    # Draw mid glow
    gdf.plot(ax=ax, color=RIVER_GLOW, linewidth=2, alpha=0.5)
    # Draw bright core
    gdf.plot(ax=ax, color=RIVER_CORE, linewidth=0.6, alpha=1.0)
    
    ax.set_xlim(-110, 110)
    ax.set_ylim(-30, 30)
    ax.axis('off')
    
    ax.set_title("RIVER VEINS\nGlobal Freshwater Vascular System", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_rivers()
