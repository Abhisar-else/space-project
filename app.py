# app.py
import streamlit as st
import os

# Import the renderers from our slides package
from slides.slide1_globe import render_globe
from slides.slide2_migration import render_migration
from slides.slide3_rivers import render_rivers
from slides.slide4_ocean import render_ocean_sst
from slides.slide5_seaice import render_sea_ice_gif

# Configure Streamlit page layout and dark aesthetics
st.set_page_config(
    page_title="Water Body: Earth Systems Data Art",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for an art-installation premium look (dark theme, cyan highlights)
st.markdown(
    """
    <style>
    /* Main app background & font color */
    .stApp {
        background-color: #000814;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #001428 !important;
        border-right: 1px solid #00b4ff33;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #aaaaaa;
    }
    
    /* Selectboxes and sidebar elements */
    div[data-baseweb="select"] {
        background-color: #000814 !important;
    }
    
    /* Headers & Title styling */
    h1, h2, h3 {
        color: #7df9ff !important;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 180, 255, 0.4);
    }
    
    /* Divider lines */
    hr {
        border-color: #00b4ff33;
    }
    
    /* Citation box design */
    .citation-box {
        background-color: #001428;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00b4ff;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Water Body: Earth Systems Data Art")
st.write("Inspired by the *Water Body* installation (ARTIS Amsterdam Royal Zoo, 2026). Built using entirely open scientific datasets.")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.write("Choose a scientific dataset slide to visualize:")
slide = st.sidebar.radio(
    "Visualizations:",
    [
        "1. Earth Overview",
        "2. Species Migration",
        "3. River Veins",
        "4. Ocean Currents",
        "5. Sea Ice Cycle"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("### Design Parameters")
st.sidebar.write("• **DPI:** 300 (High-fidelity)")
st.sidebar.write("• **Aesthetics:** Organic Neon Glow")
st.sidebar.write("• **Background:** `#000814` (Deep Space)")

# Create outputs directory if not exists
os.makedirs("outputs", exist_ok=True)

# Render chosen slide
if slide == "1. Earth Overview":
    st.subheader("1. Earth Overview — Natural Earth & NASA EPIC")
    img_path = "outputs/slide1_globe.png"
    
    if not os.path.exists(img_path):
        with st.spinner("Rendering glowing Orthographic globe..."):
            render_globe(img_path)
            
    st.image(img_path, use_column_width=True)
    
    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> Natural Earth Vector boundaries (coastlines/land features) & NASA DSCOVR EPIC Full-Disk Earth camera.</p>
            <p><b>Visual Concept:</b> A suspended planet view highlighting the ocean surface boundaries using a glowing cyan outline against deep space.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif slide == "2. Species Migration":
    st.subheader("2. Species Migration — Movebank & OBIS-SEAMAP")
    img_path = "outputs/slide2_migration.png"
    
    if not os.path.exists(img_path):
        with st.spinner("Plotting marine species tracks on Robinson projection..."):
            render_migration(img_path)
            
    st.image(img_path, use_column_width=True)
    
    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> Movebank Database and Duke University's OBIS-SEAMAP (Spatial Ecological Analysis of Megavertebrate Populations).</p>
            <p><b>Visual Concept:</b> Tracks 4 different indicator species (albatross, blue whale, emperor penguin, loggerhead turtle) using custom color tokens ending with a bright core scatter node, showing their pathways across global currents.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif slide == "3. River Veins":
    st.subheader("3. River Veins — WWF HydroRIVERS")
    img_path = "outputs/slide3_rivers.png"
    
    if not os.path.exists(img_path):
        with st.spinner("Extracting global freshwater vascular structures..."):
            render_rivers(img_path)
            
    st.image(img_path, use_column_width=True)
    
    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> Global river network geometry from the WWF HydroSHEDS / HydroRIVERS database.</p>
            <p><b>Visual Concept:</b> Depicts rivers as neon vascular veins showing flow pathways across major basins. Renders glow borders to emphasize the organic river structure.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif slide == "4. Ocean Currents":
    st.subheader("4. Ocean Currents & Temperature — Copernicus GLORYS & NASA Aqua-MODIS")
    img_path = "outputs/slide4_ocean.png"
    
    if not os.path.exists(img_path):
        with st.spinner("Calculating Sea Surface Temperature contours & current vectors..."):
            render_ocean_sst(img_path)
            
    st.image(img_path, use_column_width=True)
    
    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> Copernicus Marine Service GLORYS12V1 ocean reanalysis and NASA OceanColor Aqua-MODIS satellite observations.</p>
            <p><b>Visual Concept:</b> A thermal color map showing temperature gradient dynamics overlaid with white arrow vectors representing velocity streams of ocean currents.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif slide == "5. Sea Ice Cycle":
    st.subheader("5. Polar Sea Ice Dynamics — NOAA/NSIDC Climate Record")
    gif_path = "outputs/slide5_seaice.gif"
    
    if not os.path.exists(gif_path):
        with st.spinner("Generating and compiling polar freeze-thaw cycle animation..."):
            render_sea_ice_gif(gif_path)
            
    st.image(gif_path, use_column_width=True)
    
    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> NOAA/NSIDC Sea Ice Concentration Climate Data Record (CDR).</p>
            <p><b>Visual Concept:</b> A cyclic polar visual showing the monthly extent of sea ice freeze (full white) and thaw (deep space navy) boundaries around the Arctic circle over a full year.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
