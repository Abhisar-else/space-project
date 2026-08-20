import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import plotly.graph_objects as go
from utils.colors import BG_COLOR, DEEP_OCEAN, SATELLITE_MARKER, ORBIT_TRACE
from utils.generators import load_satellite_positions, generate_satellite_positions, fetch_tle_satellites, propagate_satellites


def build_satellite_globe():
    """Interactive orthographic globe of live satellite positions and ground tracks.

    Tries real CelesTrak TLE data first, then falls back to a synthetic LEO
    satellite field when offline or when the TLE fetch is unavailable.
    """
    df = load_satellite_positions()
    if df is None or df.empty:
        df = generate_satellite_positions()

    track_lons, track_lats = [], []
    for track in df["track"]:
        for lon, lat in track:
            track_lons.append(lon)
            track_lats.append(lat)
        track_lons.append(None)
        track_lats.append(None)

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=track_lons,
        lat=track_lats,
        mode="lines",
        line=dict(width=1.5, color=ORBIT_TRACE),
        opacity=0.45,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        marker=dict(
            size=8,
            color=SATELLITE_MARKER,
            symbol="circle",
            line=dict(width=1, color="white"),
        ),
        text=[f"{name}<br>{alt:.0f} km" for name, alt in zip(df["name"], df["alt_km"])],
        hoverinfo="text",
    ))

    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=0, lat=20, roll=0),
        showland=True,
        landcolor="#0d1b2a",
        showocean=True,
        oceancolor=DEEP_OCEAN,
        showcountries=False,
        showcoastlines=True,
        coastlinecolor="rgba(0, 180, 255, 0.35)",
        showframe=False,
        bgcolor=BG_COLOR,
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
    )
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(
            text="SATELLITE TRACKING — Live Orbital Positions<br>"
                 "<sub style='color:#888'>drag to rotate · scroll to zoom</sub>",
            font=dict(color="#e0e0e0", size=18),
            x=0.5,
        ),
        height=700,
    )
    return fig


def build_satellite_globe_live(satellites, ts, track_minutes=30, step_minutes=3):
    """Build satellite globe from pre-propagated satellite data.
    
    This is used by the live-refresh fragment in app.py — accepts already-loaded
    satellites and timescale to avoid refetching TLEs on every rerun.
    """
    df = propagate_satellites(satellites, ts, track_minutes, step_minutes)
    if df is None or df.empty:
        df = generate_satellite_positions()

    track_lons, track_lats = [], []
    for track in df["track"]:
        for lon, lat in track:
            track_lons.append(lon)
            track_lats.append(lat)
        track_lons.append(None)
        track_lats.append(None)

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=track_lons,
        lat=track_lats,
        mode="lines",
        line=dict(width=1.5, color=ORBIT_TRACE),
        opacity=0.45,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        marker=dict(
            size=8,
            color=SATELLITE_MARKER,
            symbol="circle",
            line=dict(width=1, color="white"),
        ),
        text=[f"{name}<br>{alt:.0f} km" for name, alt in zip(df["name"], df["alt_km"])],
        hoverinfo="text",
    ))

    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=0, lat=20, roll=0),
        showland=True,
        landcolor="#0d1b2a",
        showocean=True,
        oceancolor=DEEP_OCEAN,
        showcountries=False,
        showcoastlines=True,
        coastlinecolor="rgba(0, 180, 255, 0.35)",
        showframe=False,
        bgcolor=BG_COLOR,
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
    )
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(
            text="SATELLITE TRACKING — Live Orbital Positions<br>"
                 "<sub style='color:#888'>updating every 5 seconds · drag to rotate · scroll to zoom</sub>",
            font=dict(color="#e0e0e0", size=18),
            x=0.5,
        ),
        height=700,
    )
    return fig


def fetch_satellites_for_display(group="stations", max_age_days=14):
    """Wrapper to fetch TLE satellites for app.py display.
    
    This is re-exported so app.py can import only from slides.* and not
    reach directly into utils.generators.
    """
    return fetch_tle_satellites(group=group, max_age_days=max_age_days)


if __name__ == "__main__":
    fig = build_satellite_globe()
    fig.write_image("outputs/slide8_satellites.png")
