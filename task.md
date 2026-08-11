# task.md — Water Body: Earth Systems Data Art

Read `plan.md` in this same directory first. Work top to bottom — later tasks
assume earlier ones are done. After each task, run the relevant verification
command from `plan.md` before moving on; don't just eyeball the diff.

---

## Task 0 — Fix two known regressions (do this first, exactly as given)

These have already been implemented and verified working twice before being
lost. Apply the code below as-is rather than re-deriving it — that's what
caused the regression the first time.

### 0a. Restore the interactive globe for Slide 1

**Verify the bug first:**
```bash
grep -n "^def build_earth_globe" slides/slide1_globe.py   # currently: no match
grep -n "from slides.slide1_globe import render_globe$" app.py   # currently: matches
```

**`slides/slide1_globe.py`** — add these two functions at the end of the file
(the existing `render_globe`, `render_globe_animation` functions can stay,
they're just no longer called from `app.py`):

```python
def render_epic_thumbnail(epic_output_path="outputs/slide1_epic.png"):
    """Fetch and render just the NASA EPIC companion photo, without rendering
    the full matplotlib globe (build_earth_globe() replaces that)."""
    from utils.generators import load_epic_image, download_epic_image
    entries = load_epic_image()
    if not entries:
        return False
    img_path = download_epic_image(entries[-1])
    if not img_path:
        return False
    apply_dark_style()
    fig2, ax2 = plt.subplots(figsize=(6, 6), dpi=200)
    fig2.patch.set_facecolor(BG_COLOR)
    img = plt.imread(img_path)
    ax2.imshow(img)
    ax2.axis('off')
    ax2.set_title("NASA EPIC — Live Reference Photo", fontsize=11, color='#7df9ff', pad=10)
    plt.savefig(epic_output_path, bbox_inches='tight', facecolor=BG_COLOR, dpi=200)
    plt.close()
    return True


def build_earth_globe():
    """Interactive orthographic globe. Drag to rotate, scroll to zoom — replaces
    the fixed 24-frame GIF. Uses Plotly's built-in world-boundary layer (itself
    Natural-Earth-derived), so no local shapefile is needed for this layer."""
    import plotly.graph_objects as go
    from utils.colors import BG_COLOR, DEEP_OCEAN

    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=0, lat=20, roll=0),
        showland=True, landcolor="#0d1b2a",
        showocean=True, oceancolor=DEEP_OCEAN,
        showcountries=False,
        showcoastlines=True, coastlinecolor="rgba(0, 180, 255, 0.6)", coastlinewidth=1,
        showframe=False, bgcolor=BG_COLOR,
        lataxis_showgrid=True, lonaxis_showgrid=True,
        lataxis_gridcolor="rgba(0, 180, 255, 0.15)", lonaxis_gridcolor="rgba(0, 180, 255, 0.15)",
    )
    fig.update_layout(
        paper_bgcolor=BG_COLOR, showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(
            text="EARTH OVERVIEW — Deep Planet Oceans & Continents<br>"
                 "<sub style='color:#888'>drag to rotate · scroll to zoom</sub>",
            font=dict(color="#e0e0e0", size=18), x=0.5,
        ),
        height=700,
    )
    return fig
```

**`app.py`** — change the import on line 6:
```python
from slides.slide1_globe import build_earth_globe, render_epic_thumbnail
```
Add a cached wrapper near the other `@st.cache_data` wrappers:
```python
@st.cache_data(show_spinner=False)
def _cached_earth_globe():
    return build_earth_globe()
```
Replace the entire `if slide == "1. Earth Overview":` branch with:
```python
if slide == "1. Earth Overview":
    st.subheader("1. Earth Overview — Natural Earth & NASA EPIC")
    earth_fig = _cached_earth_globe()

    epic_path = "outputs/slide1_epic.png"
    if not os.path.exists(epic_path):
        with st.spinner("Fetching NASA EPIC reference photo..."):
            render_epic_thumbnail(epic_path)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(earth_fig, width='stretch')
        st.caption("Drag to rotate · scroll or pinch to zoom — no auto-rotation.")
    with col2:
        if os.path.exists(epic_path):
            st.image(epic_path, width='stretch')

    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> Natural Earth boundary data (via Plotly's built-in world atlas) & NASA DSCOVR EPIC Full-Disk Earth camera.</p>
            <p><b>Visual Concept:</b> An interactive planet view highlighting ocean surface boundaries using a glowing cyan outline against deep space.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
```
Remove the now-unused `_cached_render_globe_animation` helper and its call site if present.

### 0b. Restore the interactive globe for Slide 2

**Verify the bug first:**
```bash
grep -n "^def build_migration_globe" slides/slide2_migration.py   # currently: no match
```

**`slides/slide2_migration.py`** — add at the end of the file:
```python
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
```

**`app.py`** — change the import on line 7:
```python
from slides.slide2_migration import build_migration_globe
```
Add a cached wrapper:
```python
@st.cache_data(show_spinner=False)
def _cached_migration_globe():
    return build_migration_globe()
```
Replace the entire `elif slide == "2. Species Migration":` branch with:
```python
elif slide == "2. Species Migration":
    st.subheader("2. Species Migration — Movebank & OBIS-SEAMAP")
    migration_fig = _cached_migration_globe()
    st.plotly_chart(migration_fig, width='stretch')
    st.caption("Drag to rotate · scroll or pinch to zoom — no auto-rotation.")

    st.markdown(
        """
        <div class="citation-box">
            <h4>Data Attribution & Source Details</h4>
            <p><b>Data Sources:</b> Movebank Database and Duke University's OBIS-SEAMAP (Spatial Ecological Analysis of Megavertebrate Populations).</p>
            <p><b>Visual Concept:</b> Tracks indicator species on an interactive globe, using custom color tokens ending with a bright core scatter node, showing their pathways across global currents.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
```
Remove the now-unused `_cached_render_migration` helper and its call site if present.

### 0c. Re-fix the Copernicus Marine downloader

**Verify the bug first:**
```bash
grep -n "COPERNICUS_USERNAME\|subprocess" utils/generators.py
# currently matches — this is the old broken version (wrong CLI flags,
# wrong env var names — copernicusmarine actually reads
# COPERNICUSMARINE_SERVICE_USERNAME/_PASSWORD, not COPERNICUS_USERNAME/_PASSWORD,
# and --north/--start-date are not real CLI flags in the current toolbox)
```

**`utils/generators.py`** — inside `load_ocean_sst_data()`, find the `try:` block
that starts with `import os, subprocess` (near the end of the function, after
the local-file-search loop) and replace the entire `try:`/`except:` block with:

```python
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        username = os.getenv("COPERNICUS_USERNAME")
        password = os.getenv("COPERNICUS_PASSWORD")
        if username and password:
            import copernicusmarine
            output_filename = "glorys_sst.nc"
            copernicusmarine.subset(
                dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
                variables=["thetao"],
                minimum_longitude=-180, maximum_longitude=180,
                minimum_latitude=-60, maximum_latitude=60,
                start_datetime="2023-01-01", end_datetime="2023-01-02",
                minimum_depth=0, maximum_depth=0,
                username=username, password=password,
                output_directory=str(search_dir),
                output_filename=output_filename,
                overwrite=True,
            )
            output_path = search_dir / output_filename
            if output_path.exists():
                result = _read_sst(output_path)
                if result:
                    return result
    except Exception as exc:
        print(f"Copernicus SST download failed: {exc}")

    return generate_sst_grid()
```

This calls the `copernicusmarine` Python API directly instead of shelling out
to the CLI — credentials go in as plain arguments, so there's no dependency on
exact environment-variable naming to get wrong again.

**`requirements.txt`** — confirm `copernicusmarine` is listed (it should be
from the earlier fix — if it's missing, add it).

### Task 0 done when:
```bash
grep -c "^def build_earth_globe\|^def build_migration_globe" slides/slide1_globe.py slides/slide2_migration.py  # expect 1 each
grep -c "COPERNICUS_USERNAME" utils/generators.py   # expect 2 (username + password lines only — no "subprocess" nearby)
python3 -m pytest tests/ -q   # 5 passed
# then the full AppTest loop from plan.md — all 8 slides OK, no exceptions
```

---

## Task 1 — Repo hygiene

- [ ] `git rm -r --cached outputs/` — 5 files (`slide1_globe.png`, `slide2_migration.png`,
      `slide3_rivers.png`, `slide4_ocean.png`, `slide5_seaice.gif`) are tracked
      despite `outputs/` being in `.gitignore` (they were added before the
      ignore rule existed). Untrack without deleting locally.
- [ ] `requirements.txt` — the `rasterio` line has a trailing space
      (`"rasterio "`). Harmless to pip but clean it up.
- [ ] `DATA_SOURCES.md` — CelesTrak is currently listed as two loose bullets
      under `## Notes` instead of its own section. Give it a proper entry
      matching every other slide's format, and remove the two bullets from Notes:
      ```markdown
      ## Slide 8 — Satellite tracking

      | Source | Type | Access |
      |---|---|---|
      | CelesTrak | Live orbital element sets (TLE) | Free, no account — celestrak.org/NORAD/elements/gp.php |
      ```
- [ ] `PROGRESS.md` — fix inconsistent indentation on the last few checklist
      lines (some have a leading space before `- [x]`, most don't).

---

## Task 2 — Real data, per slide (all currently running on synthetic fallback except where noted)

| Slide | Needs | Account | .env vars | File location |
|---|---|---|---|---|
| 2. Migration | Movebank whale study access | movebank.org **+ permission request to the study owner** — apply early, this is the slow one | `MOVEBANK_USERNAME`, `MOVEBANK_PASSWORD` | fetched live, cached to `data/movebank/` |
| 3. Rivers | HydroRIVERS v10 geodatabase | none — direct download | — | `data/hydrorivers/HydroRIVERS_v10.gdb` (hydrosheds.org/products/hydrorivers) |
| 4. Ocean SST | Copernicus Marine GLORYS12V1 | marine.copernicus.eu account | `COPERNICUS_USERNAME`, `COPERNICUS_PASSWORD` | auto-downloads to `data/glorys_sst.nc` once Task 0c is applied |
| 5. Sea Ice | Copernicus Marine `siconc` | same Copernicus Marine account as #4 | same vars | `data/*seaice*.nc` |
| 6. NDVI | Sentinel-2 L2A red/NIR bands | **Copernicus Data Space** (dataspace.copernicus.eu) — a different service/account from Copernicus *Marine*, don't conflate them | — | `data/rasterio/*.tif` |
| 7. Terrain | DEM raster | none (Copernicus GLO-30, registry.opendata.aws/copernicus-dem) or a free USGS/OpenTopography account for SRTM | — | `data/gdal/*.tif`; also needs `gdaldem` installed locally (`conda install -c conda-forge gdal`) |
| 8. Satellites | none — works as-is once the repo has network access | none | — | auto-fetched, cached to `data/satellites/` |

- [ ] Create a `.env.example` at repo root listing every var above (no real
      values), so this doesn't have to be reconstructed from docs each time:
      ```
      NASA_API_KEY=
      MOVEBANK_USERNAME=
      MOVEBANK_PASSWORD=
      COPERNICUS_USERNAME=
      COPERNICUS_PASSWORD=
      ```

---

## Notes on scope (why some things aren't tasks here)

Three external reference projects came up as "should we add this": a
satellite-tracking + collision-detection system, a natural-language
satellite-imagery search tool, and an AI weather-forecast viewer. Only
satellite tracking (Task — already built as Slide 8) was judged feasible for
this repo: it needed only free data (CelesTrak) and a free library (Skyfield),
and reused the existing interactive-globe pattern. The other two need a
trained GeoAI foundation model with paid commercial imagery access, and
proprietary weather-forecast ML models, respectively — neither is portable
into a single-developer open-data portfolio project, so they're intentionally
not tasks here. Don't re-propose them without new information (e.g. a free
equivalent model/API appearing).