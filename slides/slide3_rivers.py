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
    
    from utils.generators import load_hydrorivers
    gdf = load_hydrorivers()
    if gdf is None:
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
def render_rivers_animated(output_path="outputs/slide3_rivers.gif", frames=12, fps=8):
    import imageio.v2 as imageio
    from utils.generators import load_hydrorivers, generate_river_network

    apply_dark_style()
    gdf = load_hydrorivers()
    if gdf is None:
        gdf = generate_river_network()

    # Simplify geometry ONCE — drastically speeds up repeated plotting
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(0.05, preserve_topology=False)

    temp_dir = "temp_frames_rivers"
    os.makedirs(temp_dir, exist_ok=True)
    frame_paths = []

    for i in range(frames):
        phase = i / frames
        fig, ax = plt.subplots(figsize=(12, 6.75), dpi=80)
        ax.set_facecolor(BG_COLOR)
        fig.patch.set_facecolor(BG_COLOR)

        gdf.plot(ax=ax, color=RIVER_GLOW, linewidth=3, alpha=0.15)
        pulse_alpha = 0.5 + 0.5 * abs(((phase * 2) % 2) - 1)
        gdf.plot(ax=ax, color=RIVER_CORE, linewidth=0.6, alpha=pulse_alpha)

        ax.set_xlim(-110, 110)
        ax.set_ylim(-30, 30)
        ax.axis('off')
        ax.set_title("RIVER VEINS\nGlobal Freshwater Vascular System", fontsize=14, color='#e0e0e0', weight='bold', pad=15)

        frame_path = os.path.join(temp_dir, f"frame_{i:02d}.png")
        plt.savefig(frame_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=80)
        plt.close()
        frame_paths.append(frame_path)

    frames_data = [imageio.imread(p) for p in frame_paths]
    imageio.mimsave(output_path, frames_data, fps=fps, loop=0)

    for p in frame_paths:
        try: os.remove(p)
        except OSError: pass
    try: os.rmdir(temp_dir)
    except OSError: pass
if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_rivers()
