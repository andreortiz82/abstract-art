---
name: abstract-art
description: >-
  Generates abstract PNG artwork via the abstract-art CLI (kaleidoscope, collage,
  mosaic, spiral). Use when generating generative art, abstract backgrounds,
  kaleidoscope patterns, geometric mosaics, pattern collages, seed-driven PNG art,
  or when the user mentions abstract-art or andreortiz82/abstract-art.
---

# Abstract Art Generator

Generate seed-reproducible abstract PNGs with the [abstract-art](https://github.com/andreortiz82/abstract-art) CLI.

## Tool location

| Context | Path |
| ------- | ---- |
| CURSOR workspace | `projects/abstract-art/` |
| Not cloned yet | `gh repo clone andreortiz82/abstract-art projects/abstract-art` |

## Workflow

1. **Ensure environment** — Python 3.10+ (3.12 recommended):
   ```bash
   cd projects/abstract-art
   source .venv/bin/activate || (python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
   ```

2. **Pick a generator** — match user intent; see [generators.md](generators.md).

3. **Set canvas size** (all generators accept the same flags):
   ```bash
   --size 2400              # square
   --size 1920x1080         # WxH
   --w 1024 --h 768
   --ar 16:9 --size 1920    # aspect ratio from width
   ```

4. **Run**:
   ```bash
   # Random generator + seed → outputs/<timestamp>.png
   python generate.py

   # Specific style + reproducible seed
   python generate.py kaleidoscope --seed 42 --ar 16:9 --size 1920

   # Custom output path
   python generate.py mosaic --seed 7 --ar 1:1 --size 1200 --output outputs/mosaic-7.png
   ```

5. **Report** — share output path plus the CLI line showing `WxH`, `type`, and `seed`.

## Generator quick pick

| Style | Subcommand | Best for |
| ----- | ---------- | -------- |
| Kaleidoscope | `kaleidoscope` | Mirror-symmetric B&W triangles, diamonds, radiating diagonals |
| Collage | `collage` | Few large B&W pattern cells (stripes, dots, bullseyes) |
| Mosaic | `mosaic` | Colorful polygons on black (teal, gold, magenta, peach) |
| Spiral | `spiral` | Nested wavy squares converging to a focal point |

Default random rotation: `kaleidoscope`, `collage`, `mosaic` (not `spiral`).

## When working from another project

Run from `projects/abstract-art/` and copy the PNG to the target project, or write directly:

```bash
python generate.py kaleidoscope --seed 42 --ar 1:1 --size 1200 \
  --output /absolute/path/to/assets/cover.png
```

## Extending

- New generators: `abstract_art/generators/<name>.py` + subcommand in `generate.py`
- Architecture and full flag tables: repo `README.md`
- Reference images: `projects/abstract-art/references/`

## Constraints

- PNG output only (Pillow; no numpy/matplotlib)
- Same `--seed` reproduces identical output — always record seed when user likes a result
- `outputs/` is gitignored; do not commit generated PNGs unless asked

## Do not

- Reimplement generators inline — run `generate.py`
- Use square-only assumptions — pass `--ar` or `--size WxH` for 16:9, 1:1, etc.
- Omit dimensions, type, or seed when reporting results
