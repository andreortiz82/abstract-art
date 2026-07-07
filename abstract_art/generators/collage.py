from __future__ import annotations

import math
import random
from typing import Callable

from PIL import Image, ImageDraw

from abstract_art.canvas import Canvas, Point, Rect


PatternFn = Callable[[Image.Image, ImageDraw.ImageDraw, Rect, random.Random, float], None]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def _split_grid(rect: Rect, min_cell: float, max_depth: int, depth: int, rng: random.Random) -> list[Rect]:
    if depth >= max_depth or rect.width < min_cell * 2 or rect.height < min_cell * 2:
        return [rect]

    if rect.width < min_cell * 2.5:
        split_horizontal = True
    elif rect.height < min_cell * 2.5:
        split_horizontal = False
    else:
        split_horizontal = rng.random() < 0.5

    split_at = rng.uniform(0.4, 0.6)
    if split_horizontal:
        y = rect.y0 + rect.height * split_at
        return [
            *_split_grid(Rect(rect.x0, rect.y0, rect.x1, y), min_cell, max_depth, depth + 1, rng),
            *_split_grid(Rect(rect.x0, y, rect.x1, rect.y1), min_cell, max_depth, depth + 1, rng),
        ]

    x = rect.x0 + rect.width * split_at
    return [
        *_split_grid(Rect(rect.x0, rect.y0, x, rect.y1), min_cell, max_depth, depth + 1, rng),
        *_split_grid(Rect(x, rect.y0, rect.x1, rect.y1), min_cell, max_depth, depth + 1, rng),
    ]


def _local_rect(cell: Rect) -> Rect:
    return Rect(0, 0, cell.width, cell.height)


def _draw_stripes(
    patch: Image.Image,
    draw: ImageDraw.ImageDraw,
    cell: Rect,
    rng: random.Random,
    jitter: float,
    *,
    vertical: bool,
) -> None:
    local = _local_rect(cell)
    color = BLACK if rng.random() < 0.5 else WHITE
    bg = WHITE if color == BLACK else BLACK
    draw.rectangle(local.as_int_tuple(), fill=bg)

    span = local.width if vertical else local.height
    count = rng.randint(4, 9)
    spacing = span / count
    bar = spacing * rng.uniform(0.4, 0.6)
    jit = spacing * jitter

    pos = 0.0
    while pos < span:
        a = pos + rng.uniform(-jit, jit)
        b = pos + bar + rng.uniform(-jit, jit)
        if vertical:
            draw.rectangle((a, 0, b, local.height), fill=color)
        else:
            draw.rectangle((0, a, local.width, b), fill=color)
        pos += spacing


def _draw_diagonal_stripes(
    patch: Image.Image,
    draw: ImageDraw.ImageDraw,
    cell: Rect,
    rng: random.Random,
    jitter: float,
) -> None:
    local = _local_rect(cell)
    draw.rectangle(local.as_int_tuple(), fill=WHITE)
    diag = local.width + local.height
    count = rng.randint(6, 12)
    spacing = diag / count
    width = max(1, int(spacing * 0.4))
    jit = spacing * jitter

    offset = -local.height
    while offset < diag:
        draw.line(
            [
                (offset + rng.uniform(-jit, jit), 0),
                (offset + local.height + rng.uniform(-jit, jit), local.height),
            ],
            fill=BLACK,
            width=width,
        )
        offset += spacing


def _draw_checker(
    patch: Image.Image,
    draw: ImageDraw.ImageDraw,
    cell: Rect,
    rng: random.Random,
    jitter: float,
) -> None:
    local = _local_rect(cell)
    tiles = rng.randint(3, 7)
    tile = local.width / tiles
    warp = rng.uniform(0.0, 0.15)
    jit = tile * jitter
    for row in range(int(local.height // tile) + 2):
        for col in range(tiles + 2):
            fill = BLACK if (row + col) % 2 == 0 else WHITE
            x0 = col * tile + row * tile * warp
            y0 = row * tile
            draw.rectangle(
                (
                    int(x0 + rng.uniform(-jit, jit)),
                    int(y0 + rng.uniform(-jit, jit)),
                    int(x0 + tile + rng.uniform(-jit, jit)),
                    int(y0 + tile + rng.uniform(-jit, jit)),
                ),
                fill=fill,
            )


def _draw_dots(
    patch: Image.Image,
    draw: ImageDraw.ImageDraw,
    cell: Rect,
    rng: random.Random,
    jitter: float,
) -> None:
    local = _local_rect(cell)
    inverted = rng.random() < 0.35
    bg = BLACK if inverted else WHITE
    dot = WHITE if inverted else BLACK
    draw.rectangle(local.as_int_tuple(), fill=bg)

    cols = rng.randint(3, 7)
    spacing = local.width / cols
    radius = spacing * rng.uniform(0.16, 0.34)
    jit = spacing * jitter

    y = spacing / 2
    while y < local.height:
        x = spacing / 2
        while x < local.width:
            cx = x + rng.uniform(-jit, jit)
            cy = y + rng.uniform(-jit, jit)
            draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=dot)
            x += spacing
        y += spacing


def _draw_bullseye(
    patch: Image.Image,
    draw: ImageDraw.ImageDraw,
    cell: Rect,
    rng: random.Random,
    jitter: float,
) -> None:
    local = _local_rect(cell)
    draw.rectangle(local.as_int_tuple(), fill=WHITE)
    cx, cy = local.width / 2, local.height / 2
    max_r = min(local.width, local.height) / 2 * rng.uniform(0.85, 1.0)
    rings = rng.randint(3, 6)
    ring_w = max_r / rings
    outline_w = max(1, int(ring_w * 0.12))
    jit = ring_w * jitter
    for i in range(rings, 0, -1):
        r = max_r * (i / rings)
        color = BLACK if i % 2 == 0 else WHITE
        draw.ellipse(
            (
                cx - r + rng.uniform(-jit, jit),
                cy - r + rng.uniform(-jit, jit),
                cx + r + rng.uniform(-jit, jit),
                cy + r + rng.uniform(-jit, jit),
            ),
            outline=BLACK,
            fill=color,
            width=outline_w,
        )


def _draw_solid_circle(
    patch: Image.Image,
    draw: ImageDraw.ImageDraw,
    cell: Rect,
    rng: random.Random,
    jitter: float,
) -> None:
    local = _local_rect(cell)
    bg = WHITE if rng.random() < 0.5 else BLACK
    fg = BLACK if bg == WHITE else WHITE
    draw.rectangle(local.as_int_tuple(), fill=bg)
    cx, cy = local.width / 2, local.height / 2
    r = min(local.width, local.height) * rng.uniform(0.3, 0.46)
    jit = r * jitter
    draw.ellipse(
        (
            cx - r + rng.uniform(-jit, jit),
            cy - r + rng.uniform(-jit, jit),
            cx + r + rng.uniform(-jit, jit),
            cy + r + rng.uniform(-jit, jit),
        ),
        fill=fg,
    )


PATTERNS: list[PatternFn] = [
    lambda p, d, c, r, j: _draw_stripes(p, d, c, r, j, vertical=True),
    lambda p, d, c, r, j: _draw_stripes(p, d, c, r, j, vertical=False),
    _draw_diagonal_stripes,
    _draw_checker,
    _draw_dots,
    _draw_bullseye,
    _draw_solid_circle,
]


def _draw_pattern_in_cell(
    canvas: Canvas,
    cell: Rect,
    rng: random.Random,
    jitter: float,
) -> None:
    pattern = rng.choice(PATTERNS)

    def draw_fn(patch: Image.Image, draw: ImageDraw.ImageDraw, bounds: Rect) -> None:
        pattern(patch, draw, bounds, rng, jitter)

    canvas.with_clip(cell, draw_fn)


def _draw_overlays(canvas: Canvas, width: int, height: int, rng: random.Random) -> None:
    scale = max(width, height)
    overlay_count = rng.randint(0, 1)
    for _ in range(overlay_count):
        if rng.random() < 0.5:
            r = scale * rng.uniform(0.16, 0.32)
            cx = rng.uniform(r, width - r)
            cy = rng.uniform(r, height - r)
            fill = BLACK if rng.random() < 0.5 else WHITE
            canvas.draw_ellipse(Rect(cx - r, cy - r, cx + r, cy + r), fill=fill)
        else:
            x0 = rng.uniform(0, width)
            y0 = rng.uniform(0, height)
            angle = rng.uniform(0, math.pi)
            length = scale * 1.4
            canvas.draw_line(
                Point(x0, y0),
                Point(x0 + math.cos(angle) * length, y0 + math.sin(angle) * length),
                BLACK,
                width=max(2, int(scale * 0.005)),
                jitter=scale * 0.002,
                rng=rng,
            )


def generate_collage(
    *,
    width: int = 2400,
    height: int = 2400,
    min_cell: float | None = None,
    max_depth: int = 4,
    jitter: float = 0.05,
    bg: tuple[int, int, int] = (255, 255, 255),
    rng: random.Random,
) -> Canvas:
    scale = max(width, height)
    if min_cell is None:
        min_cell = scale * 0.22

    canvas = Canvas(width, height, bg)
    root = Rect(0, 0, width, height)
    cells = _split_grid(root, min_cell, max_depth, 0, rng)
    rng.shuffle(cells)

    for cell in cells:
        _draw_pattern_in_cell(canvas, cell, rng, jitter)

    _draw_overlays(canvas, width, height, rng)
    return canvas
