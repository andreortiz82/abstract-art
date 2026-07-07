#!/usr/bin/env python3
"""CLI for generating abstract PNG artwork."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from abstract_art.canvas import parse_color
from abstract_art.generators.collage import generate_collage
from abstract_art.generators.kaleidoscope import generate_kaleidoscope
from abstract_art.generators.mosaic import generate_mosaic
from abstract_art.generators.spiral import generate_spiral
from abstract_art.rng import make_rng
from abstract_art.size import add_dimension_args, dimensions_from_args

GENERATORS = ["kaleidoscope", "collage", "mosaic"]


def _timestamp_output() -> Path:
    return Path("outputs") / f"{datetime.now():%Y%m%d-%H%M%S-%f}.png"


def build_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    add_dimension_args(shared)
    shared.add_argument("--seed", type=int, default=argparse.SUPPRESS, help="Random seed for reproducibility")
    shared.add_argument("--output", type=Path, default=argparse.SUPPRESS, help="Output PNG path")

    parser = argparse.ArgumentParser(
        description="Generate abstract PNG artwork. Run with no subcommand for a random generator + seed.",
    )
    add_dimension_args(parser)
    parser.set_defaults(size="2400")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--output", type=Path, default=None, help="Output PNG path")

    subparsers = parser.add_subparsers(dest="command", required=False)

    spiral = subparsers.add_parser("spiral", parents=[shared], help="Nested square spiral")
    spiral.add_argument("--iterations", type=int, default=None, help="Number of nested squares")
    spiral.add_argument("--ratio", type=float, default=None, help="Corner interpolation ratio per step")
    spiral.add_argument("--line-width", type=int, default=None, help="Line width in pixels")
    spiral.add_argument("--margin", type=float, default=None, help="Inset from canvas edge")
    spiral.add_argument("--fg", default=None, help="Foreground line color (hex or name)")
    spiral.add_argument("--bg", default=None, help="Background color (hex or name)")
    spiral.add_argument("--wave", type=float, default=None, help="Wave amplitude as fraction of edge length (0 = straight)")
    spiral.add_argument("--wave-freq", type=int, default=None, help="Number of waves per edge")
    spiral.add_argument("--focus-x", type=float, default=None, help="Focal point X as fraction of width (0-1)")
    spiral.add_argument("--focus-y", type=float, default=None, help="Focal point Y as fraction of height (0-1)")

    collage = subparsers.add_parser("collage", parents=[shared], help="B&W pattern collage grid")
    collage.add_argument("--min-cell", type=float, default=None, help="Minimum cell size in px (default ~22%% of long edge)")
    collage.add_argument("--max-depth", type=int, default=4, help="Maximum recursive split depth")
    collage.add_argument("--jitter", type=float, default=0.05, help="Hand-drawn jitter as fraction of feature size (0-0.3)")
    collage.add_argument("--bg", default="white", help="Background color (hex or name)")

    mosaic = subparsers.add_parser("mosaic", parents=[shared], help="Colorful geometric mosaic grid")
    mosaic.add_argument("--cols", type=int, default=None, help="Grid columns (default random 6-10)")
    mosaic.add_argument("--rows", type=int, default=None, help="Grid rows (default random 6-10)")
    mosaic.add_argument("--gap", type=float, default=None, help="Gap between cells in px (default ~1-2%% of short edge)")
    mosaic.add_argument("--bg", default="black", help="Background color (hex or name)")

    kaleidoscope = subparsers.add_parser("kaleidoscope", parents=[shared], help="Mirror-symmetric half-square triangle grid")
    kaleidoscope.add_argument("--tiles", type=int, default=None, help="Tiles per axis when square (default random 12-20, even)")
    kaleidoscope.add_argument("--tiles-x", type=int, default=None, help="Horizontal tiles (even; default random)")
    kaleidoscope.add_argument("--tiles-y", type=int, default=None, help="Vertical tiles (even; default random)")
    kaleidoscope.add_argument("--fg", default=None, help="Triangle color (hex or name)")
    kaleidoscope.add_argument("--bg", default=None, help="Background color (hex or name)")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    rng, seed = make_rng(args.seed)
    command = args.command or rng.choice(GENERATORS)
    dims = dimensions_from_args(args)
    output = args.output or _timestamp_output()
    output.parent.mkdir(parents=True, exist_ok=True)

    if command == "spiral":
        fg = getattr(args, "fg", None)
        bg = getattr(args, "bg", None)
        canvas = generate_spiral(
            rng=rng,
            width=dims.width,
            height=dims.height,
            iterations=getattr(args, "iterations", None),
            ratio=getattr(args, "ratio", None),
            line_width=getattr(args, "line_width", None),
            margin=getattr(args, "margin", None),
            fg=parse_color(fg) if fg else None,
            bg=parse_color(bg) if bg else None,
            wave=getattr(args, "wave", None),
            wave_freq=getattr(args, "wave_freq", None),
            focus_x=getattr(args, "focus_x", None),
            focus_y=getattr(args, "focus_y", None),
        )
    elif command == "collage":
        bg = getattr(args, "bg", "white") or "white"
        canvas = generate_collage(
            width=dims.width,
            height=dims.height,
            min_cell=getattr(args, "min_cell", None),
            max_depth=getattr(args, "max_depth", 4),
            jitter=getattr(args, "jitter", 0.05),
            bg=parse_color(bg),
            rng=rng,
        )
    elif command == "mosaic":
        bg = getattr(args, "bg", "black") or "black"
        canvas = generate_mosaic(
            width=dims.width,
            height=dims.height,
            cols=getattr(args, "cols", None),
            rows=getattr(args, "rows", None),
            gap=getattr(args, "gap", None),
            bg=parse_color(bg),
            rng=rng,
        )
    elif command == "kaleidoscope":
        fg = getattr(args, "fg", None)
        bg = getattr(args, "bg", None)
        canvas = generate_kaleidoscope(
            width=dims.width,
            height=dims.height,
            tiles=getattr(args, "tiles", None),
            tiles_x=getattr(args, "tiles_x", None),
            tiles_y=getattr(args, "tiles_y", None),
            fg=parse_color(fg) if fg else None,
            bg=parse_color(bg) if bg else None,
            rng=rng,
        )
    else:
        parser.error(f"Unknown command: {command}")

    canvas.save(str(output))
    print(f"Wrote {output} ({dims.width}x{dims.height}, type={command}, seed={seed})")


if __name__ == "__main__":
    main()
