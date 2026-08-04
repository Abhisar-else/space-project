# slides/slide3_rivers.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import os

import matplotlib.pyplot as plt
from utils.colors import BG_COLOR, RIVER_GLOW, RIVER_CORE, apply_dark_style
from utils.generators import generate_river_network
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
    # Keep interactive build available; legacy static renderers removed
    os.makedirs("outputs", exist_ok=True)
    fig = build_river_globe()
    # Save a static snapshot for CI/demo purposes
    try:
        import plotly.io as pio
        pio.write_image(fig, "outputs/slide3_rivers_snapshot.png", width=1600, height=900)
    except Exception:
        pass

