# utils/colors.py
import matplotlib.pyplot as plt

BG_COLOR = "#000814"
DEEP_OCEAN = "#001428"
RIVER_GLOW = "#00b4ff"
RIVER_CORE = "#7df9ff"

SPECIES_COLORS = {
    "albatross": "#ff6b9d",
    "blue_whale": "#00b4d8",
    "emperor_penguin": "#7209b7",
    "loggerhead_turtle": "#06d6a0",
}

SST_COLD = "#03071e"
SST_MID = "#6a040f"
SST_WARM = "#ffba08"

ICE_NONE = "#000814"
ICE_PARTIAL = "#c6def1"
ICE_FULL = "#ffffff"

NDVI_LOW = "#40260a"
NDVI_MID = "#c9a227"
NDVI_HIGH = "#1b8a3c"

TERRAIN_SHADOW = "#04070d"
TERRAIN_MID = "#3d6a7d"
TERRAIN_LIT = "#d6f3ff"

def apply_dark_style():
    plt.rcParams.update({
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': BG_COLOR,
        'savefig.facecolor': BG_COLOR,
        'text.color': '#e0e0e0',
        'axes.labelcolor': '#aaaaaa',
        'xtick.color': '#888888',
        'ytick.color': '#888888',
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica']
    })
