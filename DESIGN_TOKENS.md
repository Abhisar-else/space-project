# Design tokens

Single source of truth for colors, typography, and export specs.
Mirror these values in `utils/colors.py` — don't hardcode hex in slide scripts.

## Colors

### Ocean / rivers
- Background: `#000814`
- Deep ocean: `#001428`
- River glow (outer): `#00b4ff`
- River core (bright): `#7df9ff`

### Species tracks
- Albatross: `#ff6b9d`
- Blue whale: `#00b4d8`
- Emperor penguin: `#7209b7`
- Loggerhead turtle: `#06d6a0`

### Ocean temperature (cmocean.cm.thermal)
- Cold (-2°C): `#03071e`
- Mid (15°C): `#6a040f`
- Warm (32°C): `#ffba08`

### Sea ice (Blues_r)
- No ice (0%): `#000814`
- Partial (50%): `#c6def1`
- Full ice (100%): `#ffffff`

## Typography

| Use | Font | Size | Color | Weight |
|---|---|---|---|---|
| Figure titles | DejaVu Sans | 14pt | `#e0e0e0` | bold |
| Captions | DejaVu Sans | 9pt | `#aaaaaa` | regular |

## Export specs

| Property | Value |
|---|---|
| DPI | 300 |
| Format | PNG (GIF for slide 5 animation) |
| facecolor | black |
| bbox_inches | tight |

## Aspect ratios

| Slide | Ratio | Figsize |
|---|---|---|
| 1 — Globe | 1:1 | (8, 8) |
| 2 — Migration | ~1:1 | (10, 10) |
| 3 — Rivers | 16:9 | (16, 9) |
| 4 — Ocean SST | 2:1 | (14, 7) |
| 5 — Sea ice | 1:1 | (6, 6) |
### Vegetation index (NDVI)
- Bare/sparse (-1): `#40260a`
- Transitional (0): `#c9a227`
- Dense canopy (+1): `#1b8a3c`

### Terrain / hillshade
- Shadow: `#04070d`
- Mid-slope: `#3d6a7d`
- Sunlit: `#d6f3ff`