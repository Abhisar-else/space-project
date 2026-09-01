# slides/slide9_meteors.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import plotly.express as px
from utils.colors import BG_COLOR, METEOR_TRAIL, METEOR_GLOW
from utils.generators import load_meteor_showers, generate_meteor_showers


def build_meteor_calendar(year=None):
    """Annual meteor shower calendar from the IAU Meteor Data Center.

    Deliberately not rendered on the Earth globes the other slides use — a
    shower's radiant is a direction in the sky, not a point on Earth.
    """
    df = load_meteor_showers(year=year)
    if df is None or df.empty:
        df = generate_meteor_showers(year=year)

    hover_cols = ["parent_body"]
    for optional in ("ra", "dec", "member_count"):
        if optional in df.columns:
            hover_cols.append(optional)

    fig = px.timeline(
        df, x_start="peak_date", x_end="end_date", y="name",
        color="velocity_km_s", color_continuous_scale=[METEOR_GLOW, METEOR_TRAIL],
        hover_data=hover_cols,
    )
    fig.update_yaxes(autorange="reversed", title=None, gridcolor="rgba(255,255,255,0.08)")
    fig.update_xaxes(title=None, gridcolor="rgba(255,255,255,0.08)", tickformat="%b %d")
    fig.update_traces(marker=dict(line=dict(width=1, color=METEOR_TRAIL)), width=0.5)
    fig.update_coloraxes(colorbar=dict(title="km/s", tickfont=dict(color="#aaaaaa"),
                                        title_font=dict(color="#aaaaaa")))
    fig.update_layout(
        paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, font=dict(color="#e0e0e0"),
        margin=dict(l=10, r=10, t=50, b=10),
        title=dict(
            text="METEOR SHOWERS — Annual Radiant Calendar<br>"
                 "<sub style='color:#888'>peak dates · color = geocentric velocity (km/s)</sub>",
            font=dict(color="#e0e0e0", size=18), x=0.5,
        ),
        height=500,
    )
    return fig