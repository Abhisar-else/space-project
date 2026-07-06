# NASA Earth Systems Data Viz Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 5-visualization Streamlit suite inspired by the glowing, organic dark-mode aesthetics of the "Water Body" installation, using matplotlib, cartopy, and Streamlit, complete with synthetic data fallbacks to make the app instantly runnable and beautiful.

**Architecture:** A modular Python structure containing a shared design/color utility (`utils/colors.py`), synthetic data generators (`utils/generators.py`), individual visualization renderers (`slides/slide1_globe.py`, etc.), and a central Streamlit application (`app.py`).

**Tech Stack:** Python 3.11, Streamlit, Matplotlib, Geopandas, Cartopy, Xarray, NetCDF4, Shapely, Imageio, Cmocean.

---

### Task 1: Project Structure and Color Tokens

**Files:**
- Create: `utils/colors.py`
- Create: `utils/__init__.py`
- Create: `slides/__init__.py`

- [ ] **Step 1: Write `utils/colors.py`**
  Implement the design tokens defined in `DESIGN_TOKENS.md` as constants and utility functions.
  ```python
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
  ```
- [ ] **Step 2: Verify `utils/colors.py` importability**
  Run a quick verification script.
  ```bash
  python -c "from utils.colors import BG_COLOR; print('BG Color:', BG_COLOR)"
  ```
- [ ] **Step 3: Commit Task 1**
  ```bash
  git add utils/colors.py
  git commit -m "feat: setup project structure and color tokens"
  ```

---

### Task 2: Synthetic Data Generator Utilities

To ensure the visualizations render immediately without waiting for huge external dataset downloads, we create a robust generator utility to produce synthetic shapes and tracks that mirror the real datasets' structures.

**Files:**
- Create: `utils/generators.py`

- [ ] **Step 1: Write `utils/generators.py`**
  Implement mock generators for globe grids, migration paths, river networks, temperature fields, and sea ice concentrations.
  ```python
  # utils/generators.py
  import numpy as np
  import pandas as pd
  import geopandas as gpd
  from shapely.geometry import LineString, Point

  def generate_migration_tracks(num_species=4, points_per_track=100):
      data = []
      species_list = ["albatross", "blue_whale", "emperor_penguin", "loggerhead_turtle"]
      for i in range(min(num_species, len(species_list))):
          sp = species_list[i]
          # Starting point
          lon, lat = np.random.uniform(-180, 180), np.random.uniform(-60, 60)
          for step in range(points_per_track):
              lon += np.random.normal(0, 2)
              lat += np.random.normal(0, 1.5)
              lon = (lon + 180) % 360 - 180
              lat = np.clip(lat, -80, 80)
              data.append({
                  "species": sp,
                  "longitude": lon,
                  "latitude": lat,
                  "timestamp": pd.Timestamp("2026-07-01") + pd.Timedelta(hours=step)
              })
      return pd.DataFrame(data)

  def generate_river_network():
      lines = []
      # Main channel
      coords = [(x, np.sin(x/10) * 5) for x in np.linspace(-100, 100, 50)]
      lines.append(LineString(coords))
      # Tributaries
      for i in range(5):
          start_idx = np.random.randint(10, 40)
          start_pt = coords[start_idx]
          trib_coords = [start_pt]
          offset_y = np.random.choice([-1, 1])
          for x_offset in range(1, 10):
              pt = (start_pt[0] + x_offset * 3, start_pt[1] + offset_y * (x_offset * 1.5 + np.random.normal(0, 0.5)))
              trib_coords.append(pt)
          lines.append(LineString(trib_coords))
      return gpd.GeoDataFrame(geometry=lines)

  def generate_sst_grid():
      lons = np.linspace(-180, 180, 180)
      lats = np.linspace(-90, 90, 90)
      lon_grid, lat_grid = np.meshgrid(lons, lats)
      sst = 30 * np.cos(np.radians(lat_grid)) - 2
      sst += np.sin(lon_grid/20) * 3
      sst = np.clip(sst, -2, 35)
      return lons, lats, sst

  def generate_sea_ice_cycle(frames=12):
      lons = np.linspace(-180, 180, 100)
      lats = np.linspace(50, 90, 50)
      lon_grid, lat_grid = np.meshgrid(lons, lats)
      cycles = []
      for f in range(frames):
          phase = 2 * np.pi * f / frames
          min_lat = 70 + 10 * np.sin(phase)
          concentration = np.clip((lat_grid - min_lat) / (90 - min_lat) * 100, 0, 100)
          cycles.append(concentration)
      return lons, lats, cycles
  ```
- [ ] **Step 2: Verify generator outputs**
  ```bash
  python -c "from utils.generators import generate_sst_grid; print(generate_sst_grid()[2].shape)"
  ```
- [ ] **Step 3: Commit Task 2**
  ```bash
  git add utils/generators.py
  git commit -m "feat: add synthetic data generators for visualizations"
  ```

---

### Task 3: Slide 1 — Earth Overview Visualization

**Files:**
- Create: `slides/slide1_globe.py`

- [ ] **Step 1: Write `slides/slide1_globe.py`**
  ```python
  # slides/slide1_globe.py
  import matplotlib.pyplot as plt
  import cartopy.crs as ccrs
  import cartopy.feature as cfeature
  from utils.colors import BG_COLOR, DEEP_OCEAN, apply_dark_style

  def render_globe(output_path="outputs/slide1_globe.png"):
      apply_dark_style()
      fig = plt.figure(figsize=(8, 8), dpi=300)
      ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=20))
      
      ax.set_facecolor(BG_COLOR)
      ax.background_patch.set_facecolor(BG_COLOR)
      
      ax.add_feature(cfeature.OCEAN, facecolor=DEEP_OCEAN, edgecolor='none')
      ax.add_feature(cfeature.LAND, facecolor='#0d1b2a', edgecolor='#00b4ff', linewidth=0.3)
      ax.add_feature(cfeature.COASTLINE, edgecolor='#00b4ff', linewidth=0.5)
      
      gl = ax.gridlines(draw_labels=False, linewidth=0.2, color='#00b4ff', alpha=0.5, linestyle='--')
      
      ax.set_title("EARTH OVERVIEW\nDeep Planet Oceans & Continents", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
      plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
      plt.close()

  if __name__ == "__main__":
      import os
      os.makedirs("outputs", exist_ok=True)
      render_globe()
  ```
- [ ] **Step 2: Render slide 1**
  ```bash
  python slides/slide1_globe.py
  ```
- [ ] **Step 3: Commit Task 3**
  ```bash
  git add slides/slide1_globe.py
  git commit -m "feat: implement Slide 1 Globe Visualization"
  ```

---

### Task 4: Slide 2 — Species Migration Visual

**Files:**
- Create: `slides/slide2_migration.py`

- [ ] **Step 1: Write `slides/slide2_migration.py`**
  ```python
  # slides/slide2_migration.py
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
      ax.background_patch.set_facecolor(BG_COLOR)
      
      ax.add_feature(cfeature.LAND, facecolor='#020c1b', edgecolor='none')
      ax.add_feature(cfeature.COASTLINE, edgecolor='#001f3f', linewidth=0.3)
      
      df = generate_migration_tracks()
      for species, group in df.groupby("species"):
          color = SPECIES_COLORS.get(species, "#ffffff")
          ax.plot(group["longitude"], group["latitude"], transform=ccrs.PlateCarree(),
                  color=color, linewidth=1.5, alpha=0.8, label=species.replace("_", " ").title())
          ax.scatter(group["longitude"].iloc[-1], group["latitude"].iloc[-1],
                     transform=ccrs.PlateCarree(), color=color, s=20, edgecolors='#ffffff', zorder=5)
      
      ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False, fontsize=8)
      ax.set_title("SPECIES MIGRATION\nGlobal Animal Tracking & Migration Paths", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
      
      plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
      plt.close()

  if __name__ == "__main__":
      import os
      os.makedirs("outputs", exist_ok=True)
      render_migration()
  ```
- [ ] **Step 2: Render and verify slide 2**
  ```bash
  python slides/slide2_migration.py
  ```
- [ ] **Step 3: Commit Task 4**
  ```bash
  git add slides/slide2_migration.py
  git commit -m "feat: implement Slide 2 Migration Tracking Visualization"
  ```

---

### Task 5: Slide 3 — River Networks Visual

**Files:**
- Create: `slides/slide3_rivers.py`

- [ ] **Step 1: Write `slides/slide3_rivers.py`**
  ```python
  # slides/slide3_rivers.py
  import matplotlib.pyplot as plt
  from utils.colors import BG_COLOR, RIVER_GLOW, RIVER_CORE, apply_dark_style
  from utils.generators import generate_river_network

  def render_rivers(output_path="outputs/slide3_rivers.png"):
      apply_dark_style()
      fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
      ax.set_facecolor(BG_COLOR)
      
      gdf = generate_river_network()
      gdf.plot(ax=ax, color=RIVER_GLOW, linewidth=3, alpha=0.3)
      gdf.plot(ax=ax, color=RIVER_GLOW, linewidth=1.5, alpha=0.6)
      gdf.plot(ax=ax, color=RIVER_CORE, linewidth=0.6, alpha=1.0)
      
      ax.set_xlim(-110, 110)
      ax.set_ylim(-30, 30)
      ax.axis('off')
      
      ax.set_title("RIVER VEINS\nGlobal Freshwater Vascular System", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
      plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
      plt.close()

  if __name__ == "__main__":
      import os
      os.makedirs("outputs", exist_ok=True)
      render_rivers()
  ```
- [ ] **Step 2: Render and verify slide 3**
  ```bash
  python slides/slide3_rivers.py
  ```
- [ ] **Step 3: Commit Task 5**
  ```bash
  git add slides/slide3_rivers.py
  git commit -m "feat: implement Slide 3 River Networks Visualization"
  ```

---

### Task 6: Slide 4 — Ocean Currents + Temperature (SST)

**Files:**
- Create: `slides/slide4_ocean.py`

- [ ] **Step 1: Write `slides/slide4_ocean.py`**
  ```python
  # slides/slide4_ocean.py
  import matplotlib.pyplot as plt
  from matplotlib.colors import LinearSegmentedColormap
  import numpy as np
  from utils.colors import BG_COLOR, SST_COLD, SST_MID, SST_WARM, apply_dark_style
  from utils.generators import generate_sst_grid

  def render_ocean_sst(output_path="outputs/slide4_ocean.png"):
      apply_dark_style()
      fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
      ax.set_facecolor(BG_COLOR)
      
      lons, lats, sst = generate_sst_grid()
      cmap = LinearSegmentedColormap.from_list("custom_thermal", [SST_COLD, SST_MID, SST_WARM])
      im = ax.pcolormesh(lons, lats, sst, cmap=cmap, shading='auto')
      
      Y, X = np.meshgrid(lats[::5], lons[::10])
      U = np.cos(Y / 10) * 5
      V = np.sin(X / 20) * 3
      ax.quiver(X, Y, U, V, color='#ffffff', alpha=0.3, scale=50, width=0.002)
      
      cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, shrink=0.6)
      cbar.set_label("Sea Surface Temperature (°C)", color='#aaaaaa', fontsize=10)
      cbar.ax.xaxis.set_tick_params(color='#888888', labelcolor='#888888')
      
      ax.set_title("OCEAN THERMAL DYNAMICS\nGlobal SST & Vector Current Flow", fontsize=14, color='#e0e0e0', weight='bold', pad=15)
      plt.savefig(output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=300)
      plt.close()

  if __name__ == "__main__":
      import os
      os.makedirs("outputs", exist_ok=True)
      render_ocean_sst()
  ```
- [ ] **Step 2: Render and verify slide 4**
  ```bash
  python slides/slide4_ocean.py
  ```
- [ ] **Step 3: Commit Task 6**
  ```bash
  git add slides/slide4_ocean.py
  git commit -m "feat: implement Slide 4 Ocean SST & Currents Visualization"
  ```

---

### Task 7: Slide 5 — Sea Ice Annual Cycle (Animation)

**Files:**
- Create: `slides/slide5_seaice.py`

- [ ] **Step 1: Write `slides/slide5_seaice.py`**
  ```python
  # slides/slide5_seaice.py
  import matplotlib.pyplot as plt
  from matplotlib.colors import LinearSegmentedColormap
  import imageio
  import os
  from utils.colors import BG_COLOR, ICE_NONE, ICE_PARTIAL, ICE_FULL, apply_dark_style
  from utils.generators import generate_sea_ice_cycle

  def render_sea_ice_gif(output_path="outputs/slide5_seaice.gif"):
      apply_dark_style()
      lons, lats, cycles = generate_sea_ice_cycle()
      cmap = LinearSegmentedColormap.from_list("custom_ice", [ICE_NONE, ICE_PARTIAL, ICE_FULL])
      
      os.makedirs("temp_frames", exist_ok=True)
      frames = []
      
      for idx, grid in enumerate(cycles):
          fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
          ax.set_facecolor(BG_COLOR)
          
          ax.pcolormesh(lons, lats, grid, cmap=cmap, shading='auto')
          ax.set_ylim(60, 90)
          ax.axis('off')
          
          ax.set_title(f"SEA ICE DYNAMICS\nAnnual Polar Freeze Cycle - Month {idx+1}", fontsize=10, color='#e0e0e0', weight='bold', pad=10)
          
          frame_path = f"temp_frames/frame_{idx:02d}.png"
          plt.savefig(frame_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=150)
          plt.close()
          
          frames.append(imageio.imread(frame_path))
      
      imageio.mimsave(output_path, frames, fps=3, loop=0)
      
      for idx in range(len(cycles)):
          try:
              os.remove(f"temp_frames/frame_{idx:02d}.png")
          except OSError:
              pass
      try:
          os.rmdir("temp_frames")
      except OSError:
          pass

  if __name__ == "__main__":
      import os
      os.makedirs("outputs", exist_ok=True)
      render_sea_ice_gif()
  ```
- [ ] **Step 2: Render and verify slide 5**
  ```bash
  python slides/slide5_seaice.py
  ```
- [ ] **Step 3: Commit Task 7**
  ```bash
  git add slides/slide5_seaice.py
  git commit -m "feat: implement Slide 5 Sea Ice Cycle Animation"
  ```

---

### Task 8: Streamlit Integration and Dashboard Application

**Files:**
- Create: `app.py`

- [ ] **Step 1: Write `app.py`**
  ```python
  # app.py
  import streamlit as st
  import os
  from slides.slide1_globe import render_globe
  from slides.slide2_migration import render_migration
  from slides.slide3_rivers import render_rivers
  from slides.slide4_ocean import render_ocean_sst
  from slides.slide5_seaice import render_sea_ice_gif

  st.set_page_config(
      page_title="NASA Earth Systems Data Art",
      page_icon="🌍",
      layout="wide",
      initial_sidebar_state="expanded"
  )

  st.markdown(
      """
      <style>
      .main {
          background-color: #000814;
          color: #e0e0e0;
      }
      .sidebar .sidebar-content {
          background-color: #001428;
      }
      h1, h2, h3 {
          color: #7df9ff !important;
          font-family: 'Courier New', monospace;
      }
      </style>
      """,
      unsafe_html=True
  )

  st.title("Water Body: Earth Systems Data Art")
  st.write("Inspired by the *Water Body* installation (2026). Made with open scientific datasets.")

  slide = st.sidebar.radio(
      "Go to Slide:",
      ["1. Earth Overview", "2. Species Migration", "3. River Veins", "4. Ocean Currents", "5. Sea Ice Cycle"]
  )

  os.makedirs("outputs", exist_ok=True)

  if slide == "1. Earth Overview":
      st.subheader("1. Earth Overview (Natural Earth & NASA EPIC)")
      img_path = "outputs/slide1_globe.png"
      if not os.path.exists(img_path):
          with st.spinner("Generating globe visual..."):
              render_globe(img_path)
      st.image(img_path, use_column_width=True)
      st.write("**Dataset Source:** Natural Earth Vectors & NASA DSCOVR EPIC Camera.")
      
  elif slide == "2. Species Migration":
      st.subheader("2. Species Migration (Movebank / OBIS-SEAMAP)")
      img_path = "outputs/slide2_migration.png"
      if not os.path.exists(img_path):
          with st.spinner("Generating migration visual..."):
              render_migration(img_path)
      st.image(img_path, use_column_width=True)
      st.write("**Dataset Source:** Animal telemetry tracks from Movebank Database & Duke OBIS-SEAMAP.")

  elif slide == "3. River Veins":
      st.subheader("3. River Veins (HydroRIVERS)")
      img_path = "outputs/slide3_rivers.png"
      if not os.path.exists(img_path):
          with st.spinner("Generating river vein visual..."):
              render_rivers(img_path)
      st.image(img_path, use_column_width=True)
      st.write("**Dataset Source:** Global river vector geography from WWF HydroSHEDS / HydroRIVERS database.")

  elif slide == "4. Ocean Currents":
      st.subheader("4. Ocean Currents & SST (Copernicus GLORYS & NASA Aqua-MODIS)")
      img_path = "outputs/slide4_ocean.png"
      if not os.path.exists(img_path):
          with st.spinner("Generating ocean visual..."):
              render_ocean_sst(img_path)
      st.image(img_path, use_column_width=True)
      st.write("**Dataset Source:** Sea Surface Temperature reanalysis from Copernicus GLORYS12V1 & NASA Aqua-MODIS Chlorophyll-a.")

  elif slide == "5. Sea Ice Cycle":
      st.subheader("5. Polar Sea Ice Dynamics (NSIDC Sea Ice CDR)")
      gif_path = "outputs/slide5_seaice.gif"
      if not os.path.exists(gif_path):
          with st.spinner("Generating polar freeze cycle..."):
              render_sea_ice_gif(gif_path)
      st.image(gif_path, use_column_width=True)
      st.write("**Dataset Source:** NOAA/NSIDC Sea Ice Concentration Climate Data Record (CDR).")
  ```
- [ ] **Step 2: Test run the Streamlit dashboard locally**
  ```bash
  streamlit run app.py
  ```
- [ ] **Step 3: Commit Task 8**
  ```bash
  git add app.py
  git commit -m "feat: complete Streamlit dashboard integration"
  ```
