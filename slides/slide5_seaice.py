# slides/slide5_seaice.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import imageio.v2 as imageio
import numpy as np
from utils.colors import BG_COLOR, ICE_NONE, ICE_PARTIAL, ICE_FULL, apply_dark_style
from utils.generators import generate_sea_ice_cycle, load_sea_ice_data

def render_sea_ice_gif(output_path="outputs/slide5_seaice.gif"):
    apply_dark_style()
    lons, lats, cycles = load_sea_ice_data()
    if isinstance(cycles, np.ndarray):
        cycles = [cycles]
    cmap = LinearSegmentedColormap.from_list("custom_ice", [ICE_NONE, ICE_PARTIAL, ICE_FULL])
    
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    frames = []
    
    # 12 monthly cycles
    for idx, grid in enumerate(cycles):
        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.set_facecolor(BG_COLOR)
        fig.patch.set_facecolor(BG_COLOR)
        
        # Grid plot of Arctic circle focus
        ax.pcolormesh(lons, lats, grid, cmap=cmap, shading='auto')
        ax.set_ylim(60, 90)
        ax.axis('off')
        
        # Adding month title label
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        month_name = months[idx % 12]
        ax.set_title(f"SEA ICE DYNAMICS\nAnnual Polar Freeze Cycle - {month_name}", fontsize=10, color='#e0e0e0', weight='bold', pad=10)
        
        frame_path = os.path.join(temp_dir, f"frame_{idx:02d}.png")
        plt.savefig(frame_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=120)  # Moderate resolution for compact GIF size
        plt.close()
        
        frames.append(imageio.imread(frame_path))
    
    # Save GIF
    imageio.mimsave(output_path, frames, fps=3, loop=0)
    
    # Clean up temp frames
    for idx in range(len(cycles)):
        frame_path = os.path.join(temp_dir, f"frame_{idx:02d}.png")
        try:
            os.remove(frame_path)
        except OSError:
            pass
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_sea_ice_gif()
