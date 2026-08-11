# slides/slide2_migration.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
    from utils.generators import load_natural_earth
    land_gdf = load_natural_earth("land")
    if land_gdf is not None:
        ax.add_geometries(land_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='#020c1b', edgecolor='none')
        ax.add_geometries(land_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='#001f3f', linewidth=0.3)
    else:
        ax.add_feature(cfeature.LAND, facecolor='#020c1b', edgecolor='none')
        ax.add_feature(cfeature.COASTLINE, edgecolor='#001f3f', linewidth=0.3)
    # Generate and plot migration paths
    from utils.generators import load_movebank_migration
    df = load_movebank_migration()
    if df is None:
        df = generate_migration_tracks()
    df = df.sort_values("timestamp")
    for species, group in df.groupby("species"):
        group = group.sort_values("timestamp")
        color = next((c for k, c in SPECIES_COLORS.items() if k in species), "#00b4d8")
        ax.plot(group["longitude"], group["latitude"], transform=ccrs.PlateCarree(),
                color=color, linewidth=3, alpha=0.15)
        ax.plot(group["longitude"], group["latitude"], transform=ccrs.PlateCarree(),
                color=color, linewidth=1, alpha=0.9)
        ax.scatter(group["longitude"].iloc[-1], group["latitude"].iloc[-1],
                   transform=ccrs.PlateCarree(), color=color, s=15, edgecolors='#ffffff', zorder=5, linewidth=0.5)
    ax.set_title("SPECIES MIGRATION\nGlobal Animal Tracking & Migration Paths", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
    
    plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
    plt.close()


def build_migration_globe():
    """Interactive orthographic globe of species migration tracks. Tries real
    Movebank data first, falls back to synthetic — same contract as every
    other loader in utils/generators.py."""
    import plotly.graph_objects as go
    from utils.colors import BG_COLOR, DEEP_OCEAN, SPECIES_COLORS
    from utils.generators import load_movebank_migration, generate_migration_tracks

    df = load_movebank_migration()
    if df is None:
        df = generate_migration_tracks()

    fig = go.Figure()
    for species, group in df.groupby("species"):
        color = SPECIES_COLORS.get(species, "#ffffff")
        label = species.replace("_", " ").title()
        fig.add_trace(go.Scattergeo(
            lon=group["longitude"], lat=group["latitude"],
            mode="lines", line=dict(width=1.5, color=color), opacity=0.85,
            name=label, hoverinfo="name",
        ))
        fig.add_trace(go.Scattergeo(
            lon=[group["longitude"].iloc[-1]], lat=[group["latitude"].iloc[-1]],
            mode="markers", marker=dict(size=7, color=color, line=dict(width=1, color="white")),
            name=label, showlegend=False, hoverinfo="skip",
        ))

    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=0, lat=20, roll=0),
        showland=True, landcolor="#020c1b",
        showocean=True, oceancolor=DEEP_OCEAN,
        showcountries=False,
        showcoastlines=True, coastlinecolor="rgba(0, 31, 63, 0.8)",
        showframe=False, bgcolor=BG_COLOR,
        lataxis_showgrid=False, lonaxis_showgrid=False,
    )
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        legend=dict(font=dict(color="#e0e0e0"), orientation="h", y=-0.05, x=0.5, xanchor="center"),
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(
            text="SPECIES MIGRATION — Global Animal Tracking<br>"
                 "<sub style='color:#888'>drag to rotate · scroll to zoom</sub>",
            font=dict(color="#e0e0e0", size=18), x=0.5,
        ),
        height=700,
    )
    return fig


if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    render_migration()
