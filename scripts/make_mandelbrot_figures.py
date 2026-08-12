"""Build the Mandelbrot figures for notebook 047.

Writes into ``figures/mandelbrot/``:

1. ``regions.png``          the whole set and each named region of interest
2. ``zoom_<region>.html``   an interactive, animated zoom
3. ``precision_limit.png``  what double precision looks like when it runs out

The animation stores each frame as a JPEG data URI rather than as an array of numbers. A
600x450 frame is about 95 KB compressed against roughly 1 MB as raw plotly data, which is
the difference between a page that loads and one that does not.

Inspired by https://github.com/tonigineer/mandelbrot-set, a C++/SFML implementation of the
same idea with interactive panning. None of its code is used here.

These are teaching figures rather than publication figures; see the note at the top of
``make_ccs_3d_figures.py`` about in-figure titles.
"""

from pathlib import Path
import base64
import io
import sys

import numpy as np
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.mandelbrot import (  # noqa: E402
    DEEPEST_USEFUL_SPAN,
    REGIONS,
    iterations_for_span,
    region,
    render,
    smallest_reliable_span,
    to_rgb,
    zoom_spans,
)

FIGURE_ROOT = PROJECT_ROOT / "figures" / "mandelbrot"

FRAME_WIDTH, FRAME_HEIGHT = 600, 450
FRAMES = 32
JPEG_QUALITY = 82


def _jpeg_uri(image: np.ndarray, quality: int = JPEG_QUALITY) -> tuple[str, int]:
    """Encode an RGB array as a base64 JPEG data URI, and report its byte count."""
    from PIL import Image

    buffer = io.BytesIO()
    Image.fromarray(image).save(buffer, format="JPEG", quality=quality)
    payload = buffer.getvalue()
    return "data:image/jpeg;base64," + base64.b64encode(payload).decode(), len(payload)


def figure_zoom(
    name: str = "deep_spiral", end_span: float | None = None
) -> tuple[go.Figure, float]:
    """An animated zoom towards a named region; also returns the payload size in MB."""
    spec = region(name)
    spans = zoom_spans(REGIONS["overview"]["span"], end_span or spec["span"], FRAMES)

    sources, total = [], 0
    for span in spans:
        counts = render(
            center=spec["center"], span=float(span),
            width=FRAME_WIDTH, height=FRAME_HEIGHT,
            max_iterations=iterations_for_span(float(span)),
        )
        uri, size = _jpeg_uri(to_rgb(counts))
        sources.append(uri)
        total += size

    def image_trace(index: int) -> go.Image:
        return go.Image(source=sources[index], hoverinfo="skip")

    labels = [f"{REGIONS['overview']['span'] / span:,.0f}x" for span in spans]
    frames = [
        go.Frame(data=[image_trace(k)], name=labels[k]) for k in range(len(spans))
    ]

    figure = go.Figure(data=[image_trace(0)], frames=frames)
    figure.update_layout(
        title=f"Zooming into {name.replace('_', ' ')}: {spec['description']}",
        height=620,
        margin=dict(l=0, r=0, t=48, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x"),
        updatemenus=[
            dict(
                type="buttons", showactive=False, x=0.02, y=0.06, xanchor="left",
                buttons=[
                    dict(label="Play", method="animate",
                         args=[None, dict(frame=dict(duration=220, redraw=True),
                                          mode="immediate")]),
                    dict(label="Pause", method="animate",
                         args=[[None], dict(frame=dict(duration=0, redraw=False),
                                            mode="immediate")]),
                ],
            )
        ],
        sliders=[
            dict(
                active=0, x=0.14, len=0.82, y=0.06,
                currentvalue=dict(prefix="Magnification: "),
                steps=[
                    dict(label=frame.name, method="animate",
                         args=[[frame.name], dict(frame=dict(duration=0, redraw=True),
                                                  mode="immediate")])
                    for frame in frames
                ],
            )
        ],
    )
    return figure, total / 1e6


def save_regions_panel() -> None:
    """One static panel per named region, at print resolution."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = list(REGIONS)
    columns = 3
    rows = int(np.ceil(len(names) / columns))
    figure, axes = plt.subplots(
        rows, columns, figsize=(4.2 * columns, 3.6 * rows), layout="constrained"
    )

    for axis, name in zip(axes.ravel(), names):
        spec = REGIONS[name]
        counts = render(center=spec["center"], span=spec["span"],
                        width=700, height=525,
                        max_iterations=iterations_for_span(spec["span"]))
        axis.imshow(to_rgb(counts), origin="lower")
        axis.set_title(f"{name.replace('_', ' ')}\nspan {spec['span']:g}", fontsize=9)
        axis.set_xticks([])
        axis.set_yticks([])

    for axis in axes.ravel()[len(names):]:
        axis.axis("off")

    destination = FIGURE_ROOT / "regions.png"
    figure.savefig(destination, dpi=140)
    plt.close(figure)
    print(f"  {destination.relative_to(PROJECT_ROOT)}  "
          f"({destination.stat().st_size / 1e6:.1f} MB)")


def save_precision_limit() -> None:
    """Side by side: a view double precision can resolve, and one it cannot."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    center = REGIONS["deep_spiral"]["center"]
    width, height = 600, 450
    limit = smallest_reliable_span(width, center)

    views = [
        ("comfortably resolved", 1e-12),
        ("at the predicted limit", limit),
        ("past it", 1e-14),
    ]

    figure, axes = plt.subplots(1, 3, figsize=(13, 4.2), layout="constrained")
    for axis, (label, span) in zip(axes, views):
        counts = render(center=center, span=float(span), width=width, height=height,
                        max_iterations=iterations_for_span(float(span)))
        finite = counts[np.isfinite(counts)]

        # Contrast, not the count of distinct values, is what says whether anything is
        # visible: neighbouring pixels can differ in the last bit and still look flat.
        contrast = float(np.std(finite)) if finite.size else 0.0
        distinct = len(np.unique(finite)) / max(finite.size, 1)

        axis.imshow(to_rgb(counts), origin="lower")
        axis.set_title(
            f"{label}\nspan {span:.1e} — contrast {contrast:.1f}, "
            f"{distinct:.0%} distinct",
            fontsize=9,
        )
        axis.set_xticks([])
        axis.set_yticks([])

    figure.suptitle(
        f"smallest_reliable_span({width}) predicts breakdown at {limit:.1e}", fontsize=10
    )

    destination = FIGURE_ROOT / "precision_limit.png"
    figure.savefig(destination, dpi=140)
    plt.close(figure)
    print(f"  {destination.relative_to(PROJECT_ROOT)}  "
          f"({destination.stat().st_size / 1e6:.1f} MB)")


def main() -> None:
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    print("Building Mandelbrot figures into figures/mandelbrot/")

    save_regions_panel()
    save_precision_limit()

    figure, payload_mb = figure_zoom("deep_spiral", end_span=DEEPEST_USEFUL_SPAN)
    destination = FIGURE_ROOT / "zoom_deep_spiral.html"
    figure.write_html(destination, include_plotlyjs=True, full_html=True)
    print(f"  {destination.relative_to(PROJECT_ROOT)}  "
          f"({destination.stat().st_size / 1e6:.1f} MB, "
          f"{payload_mb:.1f} MB of that is {FRAMES} JPEG frames)")


if __name__ == "__main__":
    main()
