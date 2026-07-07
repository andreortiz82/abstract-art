# Generator reference

Use this when the user describes a visual style or shares a reference image.

## kaleidoscope

- **Look:** Cream/black half-square triangles in a grid; 4-fold mirror symmetry; diamonds, chevrons, radiating diagonals
- **Reference:** `references/kaleidoscope.png`
- **Flags:** `--tiles` (even), `--tiles-x`, `--tiles-y`, `--fg`, `--bg`
- **Example:** `python generate.py kaleidoscope --seed 42 --ar 16:9 --size 1920 --tiles 16`

## collage

- **Look:** High-contrast B&W; few large irregular cells; bold stripes, checkerboard, dots, bullseyes, solid circles
- **Reference:** `references/pattern-collage.png`
- **Flags:** `--min-cell` (larger = fewer elements), `--max-depth`, `--jitter`
- **Example:** `python generate.py collage --seed 7 --ar 1:1 --size 1200 --min-cell 300`

## mosaic

- **Look:** Colorful solid polygons on black; teal, gold, magenta, peach; grid of triangles, trapezoids, pentagons
- **Reference:** `references/geo-mosaic.png`
- **Flags:** `--cols`, `--rows`, `--gap`, `--bg`
- **Example:** `python generate.py mosaic --seed 42 --cols 8 --rows 8 --size 1920x1080`

## spiral

- **Look:** Nested squares spiraling to a focal point; optional wavy edges; varied stroke weight and palette
- **Reference:** `references/nested-spiral.png`
- **Flags:** `--iterations`, `--ratio`, `--line-width`, `--wave`, `--wave-freq`, `--focus-x`, `--focus-y`
- **Example:** `python generate.py spiral --seed 15 --wave 0.05 --focus-x 0.3 --focus-y 0.65`

## Phase 2 (not built)

| Style | Reference | Planned name |
| ----- | --------- | ------------ |
| Faceted hatching mesh | `references/faceted-hatching.png` | `facets` |
| Organic contour bands | `references/contour-bands.png` | `contours` |

## Size cheat sheet

| Intent | Command fragment |
| ------ | ---------------- |
| Instagram square | `--ar 1:1 --size 1080` |
| Twitter/X header | `--ar 16:9 --size 1920` |
| Portrait story | `--ar 9:16 --h 1920` |
| Custom | `--size 1024x768` or `--w 1024 --h 768` |
