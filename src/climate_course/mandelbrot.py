"""Escape-time rendering of the Mandelbrot set, vectorised over the whole image.

The set is every complex number ``c`` for which the sequence ``z -> z^2 + c`` started at
``z = 0`` stays bounded forever. That definition cannot be evaluated, so the picture is
made from its computable shadow: iterate a fixed number of times and record when, if ever,
the sequence escaped a disc it can never return from.

Two things make the result look like the pictures rather than like a contour map:

- **A generous escape radius.** Any radius above 2 is mathematically sufficient, but the
  smooth colouring below is only accurate when the escaping point has travelled well past
  the boundary, so the default is 256.
- **A fractional iteration count.** Plain integer counts produce visible bands. Subtracting
  ``log2(log|z|)`` at the moment of escape interpolates between them and the bands vanish.

Inspired by Toni Ginereus's C++/SFML implementation at
https://github.com/tonigineer/mandelbrot-set — worth a look for an interactive, compiled
version of the same idea. No code from it is used here; that repository carries no licence,
and this course needs something that runs in a notebook without a compiler.
"""

import numpy as np


ESCAPE_RADIUS = 256.0

# Named regions, all classic targets published in many places. ``span`` is the width of
# the view in the complex plane; height follows from the image's aspect ratio.
REGIONS = {
    "overview": {
        "center": (-0.5, 0.0),
        "span": 3.2,
        "description": "The whole set: cardioid, period-2 bulb, and the antenna.",
    },
    "seahorse_valley": {
        "center": (-0.743517833, 0.127094578),
        "span": 0.012,
        "description": "The cleft between cardioid and main bulb, crowded with seahorses.",
    },
    "elephant_valley": {
        "center": (0.2925, 0.0149),
        "span": 0.012,
        "description": "The valley right of the cardioid, lined with elephant-like spirals.",
    },
    "triple_spiral": {
        "center": (-0.088, 0.654),
        "span": 0.015,
        "description": "A three-armed spiral junction on the upper antenna.",
    },
    "spiral": {
        "center": (-0.761574, -0.0847596),
        "span": 0.02,
        "description": "A dense spiral staircase on the lower edge of the main cardioid.",
    },
    "deep_spiral": {
        "center": (-0.77568377, 0.13646737),
        "span": 1e-5,
        "description": (
            "Near a Misiurewicz point; the same spiral recurs over ten decades of zoom."
        ),
    },
}

# ``deep_spiral`` is the zoom target. Its centre is quoted to eight decimals and so is not
# exactly on the boundary, but it is close enough that the neighbourhood keeps producing
# structure down to a span of about 1e-11 — verified by rendering, not assumed. Below that
# the pictures go flat for want of precision rather than for want of detail.
DEEPEST_USEFUL_SPAN = 1e-11

# c = i is a genuine Misiurewicz point: its orbit is pre-periodic rather than merely
# bounded. Starting from zero it reaches -1+i and then cycles between -1+i and -i forever,
# so it lies exactly on the boundary of the set and is exactly representable in binary
# floating point. Coordinates quoted to eight decimals in the literature are not: they sit
# very near the boundary and escape after a few hundred iterations, which is why this
# constant is used for the arithmetic demonstration and not for a picture. It sits on a
# thin filament and renders as mostly empty space.
MISIUREWICZ_POINT = complex(0.0, 1.0)

# Doubles carry about 16 significant decimal digits. Once a single pixel is narrower than
# the gap between representable numbers near the view's centre, neighbouring pixels round
# to the same complex number and the image breaks into flat blocks. Past that point the
# picture is an artefact of the arithmetic, not of the set.
#
# A rough limit for a 1000-pixel-wide view; use ``smallest_reliable_span`` for a specific
# image, and see the notebook for what the failure actually looks like.
DOUBLE_PRECISION_SPAN_LIMIT = 1e-12


def smallest_reliable_span(
    width: int,
    center: tuple[float, float] = (-0.5, 0.0),
    *,
    ulps_per_pixel: float = 4.0,
) -> float:
    """Narrowest view this image size can resolve in double precision.

    Rendering below the returned span does not raise anything: it quietly returns an image
    whose pixels have collapsed onto the same handful of complex numbers. Escaping that
    limit needs arbitrary-precision arithmetic and a different algorithm, which is where
    every deep-zoom video you have seen spends its effort.
    """

    if width < 1:
        raise ValueError(f"width must be positive, got {width}")
    if ulps_per_pixel <= 0:
        raise ValueError(f"ulps_per_pixel must be positive, got {ulps_per_pixel}")

    scale = max(abs(center[0]), abs(center[1]), 1.0)
    return ulps_per_pixel * width * float(np.spacing(scale))


def iterations_for_span(span: float, *, base: int = 200, per_decade: int = 90) -> int:
    """A sensible iteration budget for a given magnification.

    Detail near the boundary needs more iterations to resolve as you zoom in, so a budget
    that is generous at full view starves a deep zoom and the picture fills with solid
    colour. Growing the budget with the log of the magnification keeps detail roughly
    constant and keeps the cost from exploding.
    """

    if span <= 0:
        raise ValueError(f"span must be positive, got {span}")
    magnification = max(REGIONS["overview"]["span"] / span, 1.0)
    return int(base + per_decade * np.log10(magnification))


def render(
    *,
    center: tuple[float, float] = (-0.5, 0.0),
    span: float = 3.2,
    width: int = 800,
    height: int = 600,
    max_iterations: int | None = None,
    escape_radius: float = ESCAPE_RADIUS,
) -> np.ndarray:
    """Fractional escape counts on a ``height`` by ``width`` grid.

    Points that never escape within the budget are NaN, which is how the interior stays
    distinguishable from a point that escaped on the very last iteration.

    Only points still in play are advanced each step. Most of the image escapes within a
    few iterations, so after the first dozen steps the arrays being squared are a small
    fraction of the grid and the render finishes far sooner than the nominal
    ``width * height * max_iterations`` suggests.
    """

    if width < 1 or height < 1:
        raise ValueError(f"width and height must be positive, got {width}x{height}")
    if span <= 0:
        raise ValueError(f"span must be positive, got {span}")
    if escape_radius <= 2:
        raise ValueError(f"escape_radius must exceed 2, got {escape_radius}")

    if max_iterations is None:
        max_iterations = iterations_for_span(span)
    if max_iterations < 1:
        raise ValueError(f"max_iterations must be at least 1, got {max_iterations}")

    center_x, center_y = center
    half_width = span / 2
    half_height = half_width * height / width

    real = np.linspace(center_x - half_width, center_x + half_width, width)
    imaginary = np.linspace(center_y - half_height, center_y + half_height, height)
    c = real[np.newaxis, :] + 1j * imaginary[:, np.newaxis]

    z = np.zeros_like(c)
    counts = np.full(c.shape, np.nan)
    active = np.ones(c.shape, dtype=bool)

    for iteration in range(max_iterations):
        z[active] = z[active] ** 2 + c[active]

        magnitude = np.abs(z)
        escaped = active & (magnitude > escape_radius)
        if escaped.any():
            # The fractional part: how far past the radius the point landed.
            counts[escaped] = (
                iteration + 1 - np.log2(np.log(magnitude[escaped]))
            )
            active &= ~escaped

        if not active.any():
            break

    return counts


def in_set(counts: np.ndarray) -> np.ndarray:
    """Boolean mask of the points that never escaped."""
    return np.isnan(counts)


def to_rgb(
    counts: np.ndarray,
    *,
    cycle: float = 8.0,
    colormap: str = "twilight_shifted",
    interior: tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    """Turn escape counts into an ``(h, w, 3)`` uint8 image.

    Escape counts near the boundary grow without bound, so mapping them linearly onto a
    colour scale washes out everything except the fringe. Two steps fix that: take the
    square root to compress the range, then wrap the result through a *cyclic* colormap
    every ``cycle`` units. The repeating bands are contour lines of escape time, and they
    are what makes the filaments legible.

    The interior has no escape count at all, so it is painted separately.
    """

    from matplotlib import colormaps  # imported lazily; the module is otherwise numpy-only

    if counts.ndim != 2:
        raise ValueError(f"counts must be a 2-D image, got shape {counts.shape}")
    if cycle <= 0:
        raise ValueError(f"cycle must be positive, got {cycle}")

    phase = np.sqrt(np.nan_to_num(counts, nan=0.0))
    rgb = colormaps[colormap]((phase % cycle) / cycle)[..., :3]
    image = (rgb * 255).astype(np.uint8)
    image[in_set(counts)] = interior
    return image


def zoom_spans(start_span: float, end_span: float, frames: int) -> np.ndarray:
    """Geometrically spaced spans from ``start_span`` down to ``end_span``.

    Zooming is multiplicative: each frame should magnify by the same *factor*, not by the
    same amount. Linear spacing would crawl at the start and leap at the end.
    """

    if frames < 2:
        raise ValueError(f"frames must be at least 2, got {frames}")
    if start_span <= 0 or end_span <= 0:
        raise ValueError("spans must be positive")
    return np.geomspace(start_span, end_span, frames)


def region(name: str) -> dict:
    """Look up a named region of interest."""
    if name not in REGIONS:
        raise KeyError(f"unknown region {name!r}; choose from {sorted(REGIONS)}")
    return REGIONS[name]
