from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Dimensions:
    width: int
    height: int

    @property
    def size(self) -> int:
        """Longer edge — used for proportional scaling in generators."""
        return max(self.width, self.height)

    @property
    def min_dim(self) -> int:
        return min(self.width, self.height)


_SIZE_RE = re.compile(r"^(\d+)[xX](\d+)$")
_AR_RE = re.compile(r"^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$")


def parse_size(value: str) -> Dimensions | int:
    """Parse --size: integer (square) or WxH string."""
    if value.isdigit():
        n = int(value)
        return n
    match = _SIZE_RE.match(value.strip())
    if match:
        return Dimensions(int(match.group(1)), int(match.group(2)))
    raise argparse.ArgumentTypeError(
        f"Invalid --size {value!r}. Use an integer (2400) or WxH (1920x1080)."
    )


def parse_ar(value: str) -> tuple[float, float]:
    match = _AR_RE.match(value.strip())
    if not match:
        raise argparse.ArgumentTypeError(
            f"Invalid --ar {value!r}. Use W:H (16:9, 1:1, 9:16)."
        )
    return float(match.group(1)), float(match.group(2))


def resolve_dimensions(
    *,
    size: str | int | Dimensions | None = 2400,
    width: int | None = None,
    height: int | None = None,
    ar: str | None = None,
) -> Dimensions:
    """Resolve final width×height from CLI flags.

    Precedence: --w + --h > --size WxH > --ar (with --size or --w as width) > --size int (square).
    """
    if width is not None and height is not None:
        return Dimensions(width, height)

    if width is not None and height is None and ar is None:
        raise argparse.ArgumentTypeError("--w requires --h (or use --ar to derive height).")
    if height is not None and width is None and ar is None:
        raise argparse.ArgumentTypeError("--h requires --w (or use --ar to derive width).")

    # Parse --size
    parsed_size: int | Dimensions | None = None
    if size is not None:
        if isinstance(size, Dimensions):
            parsed_size = size
        elif isinstance(size, int):
            parsed_size = size
        else:
            parsed_size = parse_size(str(size))

    if ar is not None:
        ar_w, ar_h = parse_ar(ar)
        if ar_w <= 0 or ar_h <= 0:
            raise argparse.ArgumentTypeError("--ar values must be positive.")

        base_w: int
        if width is not None:
            base_w = width
        elif isinstance(parsed_size, Dimensions):
            base_w = parsed_size.width
        elif isinstance(parsed_size, int):
            base_w = parsed_size
        else:
            base_w = 2400

        base_h = max(1, round(base_w * ar_h / ar_w))
        if height is not None:
            # --h wins as the target height; recompute width from aspect ratio.
            base_h = height
            base_w = max(1, round(base_h * ar_w / ar_h))
        return Dimensions(base_w, base_h)

    if isinstance(parsed_size, Dimensions):
        if width is not None:
            return Dimensions(width, parsed_size.height)
        if height is not None:
            return Dimensions(parsed_size.width, height)
        return parsed_size

    if isinstance(parsed_size, int):
        if width is not None:
            return Dimensions(width, parsed_size)
        if height is not None:
            return Dimensions(parsed_size, height)
        return Dimensions(parsed_size, parsed_size)

    if width is not None or height is not None:
        raise argparse.ArgumentTypeError("Partial dimensions need --size, --w+--h, or --ar.")

    return Dimensions(2400, 2400)


def add_dimension_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--size",
        default=argparse.SUPPRESS,
        help="Canvas size: integer for square (2400) or WxH (1920x1080)",
    )
    parser.add_argument("--w", type=int, default=argparse.SUPPRESS, help="Canvas width in px")
    parser.add_argument("--h", type=int, default=argparse.SUPPRESS, help="Canvas height in px")
    parser.add_argument("--ar", default=argparse.SUPPRESS, help="Aspect ratio W:H (16:9, 1:1, 9:16)")


def dimensions_from_args(args: argparse.Namespace) -> Dimensions:
    size = getattr(args, "size", 2400)
    return resolve_dimensions(
        size=size,
        width=getattr(args, "w", None),
        height=getattr(args, "h", None),
        ar=getattr(args, "ar", None),
    )
