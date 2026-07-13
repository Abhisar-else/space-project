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
def _linestrings_to_geo_arrays(gdf):
    """Flatten LineString/MultiLineString geometry into flat lon/lat lists for
    one Scattergeo trace. None between segments so unrelated rivers aren't
    joined by a stray line — same technique as Plotly's own reference example."""
    import shapely.geometry as geom
    lons, lats = [], []
    for feature in gdf.geometry:
        if feature is None:
            continue
        if isinstance(feature, geom.LineString):
            parts = [feature]
        elif isinstance(feature, geom.MultiLineString):
            parts = list(feature.geoms)
        else:
            continue
        for part in parts:
            x, y = part.xy
            lons.extend(x)
            lats.extend(y)
            lons.append(None)
            lats.append(None)
    return lons, lats


def build_river_globe(max_ord_flow=3, simplify_tolerance=0.03):
    """Interactive orthographic-globe river network. Drag to rotate, scroll to
    zoom — renders live in-browser, no fixed rotation, no GIF frames.

    max_ord_flow / simplify_tolerance only matter once real HydroRIVERS data is
    in play (the synthetic fallback is already small): tighten toward 1-2 /
    raise the tolerance if a full real dataset feels heavy — Plotly renders
    every point client-side, so point count matters more here than for a
    static matplotlib PNG.
    """
    import plotly.graph_objects as go
    from utils.colors import BG_COLOR, DEEP_OCEAN, RIVER_GLOW, RIVER_CORE
    from utils.generators import load_hydrorivers, generate_river_network

    gdf = load_hydrorivers(max_ord_flow=max_ord_flow)
    if gdf is None:
        gdf = generate_river_network()
    else:
        gdf = gdf.copy()
        gdf["geometry"] = gdf.geometry.simplify(simplify_tolerance, preserve_topology=False)

    lons, lats = _linestrings_to_geo_arrays(gdf)

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, mode="lines",
        line=dict(width=3, color=RIVER_GLOW), opacity=0.25, hoverinfo="skip",
    ))
    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, mode="lines",
        line=dict(width=1, color=RIVER_CORE), opacity=0.9, hoverinfo="skip",
    ))
    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=0, lat=20, roll=0),
        showland=True, landcolor="#0d1b2a",
        showocean=True, oceancolor=DEEP_OCEAN,
        showcountries=False,
        showcoastlines=True, coastlinecolor="rgba(0, 180, 255, 0.35)",
        showframe=False,
        bgcolor=BG_COLOR,
        lataxis_showgrid=False, lonaxis_showgrid=False,
    )
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(
            text="RIVER VEINS — Global Freshwater Network<br>"
                 "<sub style='color:#888'>drag to rotate · scroll to zoom</sub>",
            font=dict(color="#e0e0e0", size=18), x=0.5,
        ),
        height=700,
    )
    return fig
if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_rivers()

