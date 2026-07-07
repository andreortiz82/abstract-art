<img width="200" height="200" alt="20260707-163726-480345" src="https://github.com/user-attachments/assets/08f9e326-d731-4aee-9073-ea1ec9ee0ed2" />
<img width="200" height="200" alt="20260707-163726-432926" src="https://github.com/user-attachments/assets/96279865-56c1-448d-a72e-1ddc52ce6b35" />
<img width="200" height="200" alt="20260707-163726-380023" src="https://github.com/user-attachments/assets/fb11d1cf-8860-4df7-906b-9b3e4a80bdc8" />

# Abstract Art Generator

Python CLI for generating abstract PNG artwork with reproducible seeds.

**Repo:** https://github.com/andreortiz82/abstract-art

## Setup

Requires **Python 3.10+** (3.12 recommended).

```bash
cd projects/abstract-art
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Canvas size

Every generator accepts the same dimension flags:

```bash
# Square (default 2400×2400)
python generate.py kaleidoscope --size 2400

# Explicit width × height
python generate.py mosaic --size 1920x1080
python generate.py collage --w 1024 --h 768

# Aspect ratio (uses --size or --w as the width basis)
python generate.py kaleidoscope --ar 16:9 --size 1920    # → 1920×1080
python generate.py mosaic --ar 9:16 --h 1080           # → 608×1080
python generate.py collage --ar 1:1 --size 1200        # → 1200×1200
```

| Flag | Example | Result |
|------|---------|--------|
| `--size N` | `--size 2400` | N×N square |
| `--size WxH` | `--size 1920x1080` | Explicit dimensions |
| `--w` / `--h` | `--w 1024 --h 768` | Width and height |
| `--ar W:H` | `--ar 16:9 --size 1920` | Aspect ratio from width |

Precedence: `--w` + `--h` → `--size WxH` → `--ar` (with `--size` or `--w` as width) → `--size N` (square).

### Random (default)

Run with no subcommand to get a **random generator** and a **random seed**. Output is written to `outputs/<timestamp>.png`.

```bash
python generate.py
```

The default random rotation picks from `kaleidoscope`, `collage`, and `mosaic`. Every run prints the chosen type and seed so you can reproduce a favorite:

```
Wrote outputs/20260707-153411-359258.png (type=kaleidoscope, seed=427896676)
```

### Kaleidoscope

A mirror-symmetric grid of half-square triangle tiles (cream + near-black). One quadrant is generated at random, then mirrored across both axes for 4-fold kaleidoscope symmetry — producing diamonds, arrows, and radiating diagonals.

```bash
python generate.py kaleidoscope --seed 42 --output outputs/kaleido-42.png
python generate.py kaleidoscope --seed 7 --tiles 16   # denser grid
```

| Flag | Default | Description |
|------|---------|-------------|
| `--size` | 2400 | Square, or `WxH` (e.g. `1920x1080`) |
| `--w` / `--h` | — | Explicit width and height |
| `--ar` | — | Aspect ratio `W:H` with `--size` or `--w` |
| `--seed` | random | Reproducibility seed |
| `--tiles` | random (12–20, even) | Tiles per side (forced even for clean mirroring) |
| `--fg` | random palette | Triangle color |
| `--bg` | random palette | Background color |
| `--output` | `outputs/<timestamp>.png` | Output path |

### Nested square spiral

Nested squares that converge toward a focal point — inspired by pursuit-curve / logarithmic spiral art. Edges can be straight or wavy, the focal point lands anywhere on the canvas, and strokes vary in weight. When a flag is omitted, its value is chosen randomly from the seed, so each seed yields a distinct spiral.

```bash
# Fully random spiral
python generate.py spiral --seed 42 --size 2400 --output outputs/spiral-42.png

# Wavy edges, off-center focal point
python generate.py spiral --seed 15 --wave 0.05 --wave-freq 3 --focus-x 0.3 --focus-y 0.65
```

| Flag | Default | Description |
|------|---------|-------------|
| `--size` | 2400 | Square, or `WxH` (e.g. `1920x1080`) |
| `--w` / `--h` | — | Explicit width and height |
| `--ar` | — | Aspect ratio `W:H` with `--size` or `--w` |
| `--seed` | random | Reproducibility seed |
| `--iterations` | random (180–420) | Number of nested squares |
| `--ratio` | random (0.02–0.055) | Corner shift per iteration |
| `--line-width` | random (1–5) | Stroke width |
| `--margin` | random | Inset from canvas edge |
| `--fg` | random palette | Line color |
| `--bg` | random palette | Background color |
| `--wave` | random (~60% wavy) | Wave amplitude as fraction of edge length (0 = straight) |
| `--wave-freq` | random (1–3) | Number of waves per edge |
| `--focus-x` | random (0.28–0.72) | Focal point X as fraction of size |
| `--focus-y` | random (0.28–0.72) | Focal point Y as fraction of size |
| `--output` | `outputs/<timestamp>.png` | Output path |

### Pattern collage

High-contrast black-and-white grid of a **few large cells**, each filled with a bold, detailed pattern — stripes, checkerboard, dots, bullseyes, or solid circles. Cells are large and pattern features scale to the cell, so you see fewer elements in more detail (works well cropped to 16:9 or 1:1).

```bash
python generate.py collage --seed 7 --size 2400 --output outputs/collage-7.png
```

| Flag | Default | Description |
|------|---------|-------------|
| `--size` | 2400 | Square, or `WxH` (e.g. `1920x1080`) |
| `--w` / `--h` | — | Explicit width and height |
| `--ar` | — | Aspect ratio `W:H` with `--size` or `--w` |
| `--seed` | random | Reproducibility seed |
| `--min-cell` | ~22% of size | Minimum cell size before split stops (larger = fewer, bigger elements) |
| `--max-depth` | 4 | Max recursive grid depth |
| `--jitter` | 0.05 | Hand-drawn jitter as a fraction of feature size (0–0.3) |
| `--bg` | white | Background color |
| `--output` | `outputs/<timestamp>.png` | Output path |

Want even fewer, bigger shapes? Raise `--min-cell` (e.g. `--min-cell 900`). Want more? Lower it (e.g. `--min-cell 300`).

### Geometric mosaic

Colorful grid of random polygons — triangles, trapezoids, pentagons, and quads in teal, gold, magenta, and peach on black. Matches the retro grid-collage reference style.

```bash
python generate.py mosaic --seed 42 --cols 8 --rows 8 --output outputs/mosaic-42.png
python generate.py mosaic --seed 7   # random grid size and palette
```

| Flag | Default | Description |
|------|---------|-------------|
| `--size` | 2400 | Square, or `WxH` (e.g. `1920x1080`) |
| `--w` / `--h` | — | Explicit width and height |
| `--ar` | — | Aspect ratio `W:H` with `--size` or `--w` |
| `--seed` | random | Reproducibility seed |
| `--cols` | random (6–10) | Grid columns |
| `--rows` | random (6–10) | Grid rows |
| `--gap` | random (~1–2% of size) | Black gap between cells |
| `--bg` | black | Background color |
| `--output` | `outputs/<timestamp>.png` | Output path |

## Reference images

Inspiration targets live in [`references/`](references/). Phase 2 will add:

- `facets` — faceted hatching mesh (noise-displaced triangulation)
- `contours` — organic contour bands with vertical color stripes

## Project layout

```
abstract_art/
  canvas.py       # Pillow drawing helpers
  size.py         # Canvas dimension parsing (--size, --w/--h, --ar)
  rng.py          # Seeded random
  generators/
    kaleidoscope.py
    spiral.py
    collage.py
    mosaic.py
generate.py       # CLI entry point
outputs/          # Generated PNGs (gitignored)
```
