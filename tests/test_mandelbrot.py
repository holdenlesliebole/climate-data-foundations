import numpy as np
import pytest

from climate_course.mandelbrot import (
    DOUBLE_PRECISION_SPAN_LIMIT,
    MISIUREWICZ_POINT,
    REGIONS,
    in_set,
    iterations_for_span,
    region,
    render,
    smallest_reliable_span,
    to_rgb,
    zoom_spans,
)


def single_point(x: float, y: float, max_iterations: int = 400) -> float:
    """Escape count at exactly one complex number.

    A 3x3 grid is used rather than 1x1 because ``np.linspace(a, b, 1)`` returns the left
    edge, not the midpoint, which would sample half a span away from the requested point.
    With three samples the middle one lands on the centre exactly, which matters for
    points sitting on the boundary of the set.
    """

    return render(
        center=(x, y), span=1e-9, width=3, height=3, max_iterations=max_iterations
    )[1, 1]


@pytest.mark.parametrize("x,y", [(0.0, 0.0), (-1.0, 0.0), (-0.5, 0.0), (0.25, 0.0),
                                 (-0.1, 0.7), (-1.75, 0.0)])
def test_points_known_to_be_inside_never_escape(x: float, y: float) -> None:
    assert np.isnan(single_point(x, y))


@pytest.mark.parametrize("x,y", [(1.0, 0.0), (2.0, 0.0), (-2.5, 0.0), (0.0, 1.5),
                                 (0.5, 0.5), (-1.0, 1.0)])
def test_points_known_to_be_outside_escape(x: float, y: float) -> None:
    assert np.isfinite(single_point(x, y))


def test_the_set_is_symmetric_about_the_real_axis() -> None:
    counts = render(center=(-0.5, 0.0), span=3.2, width=120, height=120,
                    max_iterations=120)
    # A grid centred on y = 0 with an even pixel count mirrors row-for-row.
    top, bottom = counts[: 120 // 2], counts[120 // 2:][::-1]
    assert np.allclose(top, bottom, equal_nan=True)


def test_interior_is_nan_and_exterior_is_finite() -> None:
    counts = render(center=(-0.5, 0.0), span=3.2, width=200, height=150,
                    max_iterations=200)
    inside = in_set(counts)
    assert inside.any() and not inside.all()
    assert np.isfinite(counts[~inside]).all()


def test_escape_counts_are_fractional_not_banded() -> None:
    counts = render(center=(-0.5, 0.0), span=3.2, width=200, height=150,
                    max_iterations=200)
    escaped = counts[np.isfinite(counts)]
    # Smooth colouring must produce values that are not whole numbers.
    assert not np.allclose(escaped, np.round(escaped))


def test_counts_rise_towards_the_boundary() -> None:
    # Walking in from outside towards the cardioid, escape should take longer.
    far = single_point(-2.4, 0.0)
    near = single_point(-2.01, 0.0)
    assert far < near


def test_render_shape_matches_requested_size() -> None:
    assert render(width=64, height=48, max_iterations=50).shape == (48, 64)


def test_aspect_ratio_is_preserved() -> None:
    # A square view of a square grid and a wide view of a wide grid should agree on
    # the vertical extent per pixel; check the set is not stretched.
    square = render(center=(-0.5, 0.0), span=3.2, width=100, height=100,
                    max_iterations=100)
    wide = render(center=(-0.5, 0.0), span=3.2, width=200, height=100,
                  max_iterations=100)
    # The middle row spans the same real interval in both, so the count of interior
    # pixels along it should be proportional to the width.
    square_row = in_set(square)[50].sum()
    wide_row = in_set(wide)[50].sum()
    assert wide_row == pytest.approx(2 * square_row, rel=0.05)


def test_a_bigger_budget_only_ever_removes_points_from_the_interior() -> None:
    small = render(center=(-0.75, 0.1), span=0.05, width=80, height=60,
                   max_iterations=60)
    large = render(center=(-0.75, 0.1), span=0.05, width=80, height=60,
                   max_iterations=600)
    # Anything that escaped with the small budget escaped identically with the large one.
    escaped_small = np.isfinite(small)
    assert np.allclose(small[escaped_small], large[escaped_small])
    # And the apparent interior can only shrink.
    assert in_set(large).sum() <= in_set(small).sum()


def test_iteration_budget_grows_with_magnification() -> None:
    assert iterations_for_span(3.2) < iterations_for_span(0.01)
    assert iterations_for_span(0.01) < iterations_for_span(1e-6)


def test_zoom_spans_are_geometric_and_bracket_the_request() -> None:
    spans = zoom_spans(3.2, 0.008, 25)
    assert len(spans) == 25
    assert spans[0] == pytest.approx(3.2)
    assert spans[-1] == pytest.approx(0.008)
    ratios = spans[:-1] / spans[1:]
    assert np.allclose(ratios, ratios[0])  # constant magnification per frame


def test_every_named_region_renders_something_interesting() -> None:
    for name, spec in REGIONS.items():
        counts = render(center=spec["center"], span=spec["span"],
                        width=60, height=45, max_iterations=300)
        inside = in_set(counts)
        assert inside.any(), f"{name} shows no interior"
        assert (~inside).any(), f"{name} shows no exterior"


def test_region_lookup_rejects_unknown_names() -> None:
    assert region("seahorse_valley")["span"] == pytest.approx(0.012)
    with pytest.raises(KeyError):
        region("not_a_region")


def test_misiurewicz_point_is_preperiodic_and_therefore_in_the_set() -> None:
    """The orbit of c = i must fall into a cycle rather than escape or converge."""
    c = MISIUREWICZ_POINT
    z = 0j
    orbit = []
    for _ in range(200):
        z = z * z + c
        orbit.append(z)

    assert abs(z) == pytest.approx(np.sqrt(2))          # still bounded
    assert orbit[-1] == pytest.approx(orbit[-3])        # period 2
    assert orbit[-1] != pytest.approx(orbit[-2])        # and genuinely alternating
    assert np.isnan(single_point(c.real, c.imag, max_iterations=2000))


def test_literature_coordinates_are_only_approximately_on_the_boundary() -> None:
    """A boundary point quoted to eight decimals is not actually on the boundary.

    This is why the module keeps an exact point for arithmetic and separate, purely
    visual coordinates for the pictures.
    """
    approximate = single_point(-0.77568377, 0.13646737, max_iterations=2000)
    assert np.isfinite(approximate)   # it escapes
    assert approximate > 200          # but only after a long time near the boundary


def test_documented_limit_still_resolves_distinct_doubles() -> None:
    # At the documented limit a 1000-pixel view keeps several representable numbers
    # per pixel, so the grid is not yet quantised.
    pixel = DOUBLE_PRECISION_SPAN_LIMIT / 1000
    assert pixel > 4 * np.spacing(1.0)
    assert DOUBLE_PRECISION_SPAN_LIMIT >= smallest_reliable_span(1000)


def test_smallest_reliable_span_scales_with_image_width() -> None:
    assert smallest_reliable_span(2000) == pytest.approx(2 * smallest_reliable_span(1000))
    with pytest.raises(ValueError):
        smallest_reliable_span(0)


def test_pixels_actually_collapse_below_the_limit() -> None:
    """The documented failure mode has to be real, not just asserted in a docstring."""
    center = (-0.77568377, 0.13646737)
    width, height = 100, 75

    safe = render(center=center, span=1e-9, width=width, height=height,
                  max_iterations=400)
    starved = render(center=center, span=1e-16, width=width, height=height,
                     max_iterations=400)

    def distinct_fraction(counts: np.ndarray) -> float:
        finite = counts[np.isfinite(counts)]
        return len(np.unique(finite)) / max(finite.size, 1)

    assert distinct_fraction(safe) > 0.9
    assert distinct_fraction(starved) < 0.5


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(width=0),
        dict(height=0),
        dict(span=0.0),
        dict(span=-1.0),
        dict(escape_radius=2.0),
        dict(max_iterations=0),
    ],
)
def test_render_rejects_impossible_settings(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        render(**kwargs)


def test_colouring_paints_the_interior_separately() -> None:
    counts = render(center=(-0.5, 0.0), span=3.2, width=80, height=60,
                    max_iterations=200)
    image = to_rgb(counts, interior=(0, 0, 0))

    assert image.shape == (60, 80, 3)
    assert image.dtype == np.uint8
    assert (image[in_set(counts)] == 0).all()
    assert image[~in_set(counts)].any()


def test_colouring_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        to_rgb(np.zeros((4, 4, 4)))
    with pytest.raises(ValueError):
        to_rgb(np.zeros((4, 4)), cycle=0)


def test_zoom_spans_rejects_degenerate_requests() -> None:
    with pytest.raises(ValueError):
        zoom_spans(3.2, 0.01, 1)
    with pytest.raises(ValueError):
        zoom_spans(0.0, 0.01, 10)
