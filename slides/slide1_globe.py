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

def render_globe(output_path="outputs/slide1_globe.png", epic_output_path="outputs/slide1_epic.png"):
    apply_dark_style()
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=20))

    ax.set_facecolor(BG_COLOR)
    try:
        ax.background_patch.set_facecolor(BG_COLOR)
    except AttributeError:
        ax.patch.set_facecolor(BG_COLOR)

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

    ax.gridlines(draw_labels=False, linewidth=0.2, color='#00b4ff', alpha=0.5, linestyle='--')
    ax.set_title("EARTH OVERVIEW\nDeep Planet Oceans & Continents", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()

    # Companion EPIC reference thumbnail
    from utils.generators import load_epic_image, download_epic_image
    entries = load_epic_image()
    if entries:
        img_path = download_epic_image(entries[-1])
        if img_path:
            fig2, ax2 = plt.subplots(figsize=(6, 6), dpi=200)
            fig2.patch.set_facecolor(BG_COLOR)
            img = plt.imread(img_path)
            ax2.imshow(img)
            ax2.axis('off')
            ax2.set_title("NASA EPIC — Live Reference Photo", fontsize=11, color='#7df9ff', pad=10)
            plt.savefig(epic_output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=200)
            plt.close()
def render_globe_animation(output_path="outputs/slide1_globe_rotation.gif", frames=24, fps=12):
    import imageio.v2 as imageio
    from utils.generators import load_natural_earth

    apply_dark_style()
    ocean_gdf = load_natural_earth("ocean")
    land_gdf = load_natural_earth("land")

    temp_dir = "temp_frames_globe"
    os.makedirs(temp_dir, exist_ok=True)
    frame_paths = []

    for i in range(frames):
        lon = (360 / frames) * i
        fig = plt.figure(figsize=(6, 6), dpi=120)
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=lon, central_latitude=20))
        ax.set_facecolor(BG_COLOR)
        try:
            ax.background_patch.set_facecolor(BG_COLOR)
        except AttributeError:
            ax.patch.set_facecolor(BG_COLOR)

        if ocean_gdf is not None and land_gdf is not None:
            ax.add_geometries(ocean_gdf.geometry, crs=ccrs.PlateCarree(), facecolor=DEEP_OCEAN, edgecolor='none')
            ax.add_geometries(land_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='#0d1b2a', edgecolor='#00b4ff', linewidth=0.3)
        else:
            ax.add_feature(cfeature.OCEAN, facecolor=DEEP_OCEAN, edgecolor='none')
            ax.add_feature(cfeature.LAND, facecolor='#0d1b2a', edgecolor='#00b4ff', linewidth=0.3)
        ax.add_feature(cfeature.COASTLINE, edgecolor='#00b4ff', linewidth=0.5)
        ax.gridlines(draw_labels=False, linewidth=0.2, color='#00b4ff', alpha=0.5, linestyle='--')

        frame_path = os.path.join(temp_dir, f"frame_{i:02d}.png")
        plt.savefig(frame_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=120)
        plt.close()
        frame_paths.append(frame_path)

    frames_data = [imageio.imread(p) for p in frame_paths]
    imageio.mimsave(output_path, frames_data, fps=fps, loop=0)

    for p in frame_paths:
        try:
            os.remove(p)
        except OSError:
            pass
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    render_globe()