"""Build the interactive Lorenz figures for notebook 046.

Writes standalone HTML into ``figures/lorenz/``. Each file embeds its own copy of
plotly.js, so it opens in any browser and can be dropped into the Jupyter Book without a
network connection.

Three figures:

1. ``attractor``            the trajectory itself, coloured by time
2. ``sensitive_dependence`` two runs a billionth apart, with their separation
3. ``ensemble``             a small ball of initial states, stretched and folded

These are teaching figures rather than publication figures, so each carries a title; see
the note at the top of ``make_ccs_3d_figures.py`` for why that departs from
``conventions/figure-conventions.md``.
"""

from pathlib import Path
import sys

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.lorenz import (  # noqa: E402
    integrate,
    largest_lyapunov,
    perturbed_pair,
    separation,
)

FIGURE_ROOT = PROJECT_ROOT / "figures" / "lorenz"

START = np.array([1.0, 1.0, 1.0])
DT = 0.005
STEPS = 12000
SETTLE = 2000  # steps discarded so the picture shows the attractor, not the approach


def _scene() -> dict:
    return dict(
        xaxis=dict(title="x  (overturning)"),
        yaxis=dict(title="y  (temperature contrast)"),
        zaxis=dict(title="z  (profile distortion)"),
        aspectmode="cube",
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.6)),
    )


def figure_attractor() -> go.Figure:
    """The trajectory, coloured by time so the direction of travel is visible."""
    path = integrate(START, dt=DT, steps=STEPS)[SETTLE:]
    time = np.arange(path.shape[0]) * DT

    figure = go.Figure(
        go.Scatter3d(
            x=path[:, 0], y=path[:, 1], z=path[:, 2],
            mode="lines",
            line=dict(color=time, colorscale="Viridis", width=2,
                      colorbar=dict(title="Time<br>(dimensionless)")),
            hovertemplate="x %{x:.2f}<br>y %{y:.2f}<br>z %{z:.2f}<extra></extra>",
        )
    )
    figure.update_layout(
        title="The Lorenz attractor, σ=10, ρ=28, β=8/3",
        scene=_scene(),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
    )
    return figure


def figure_sensitive_dependence(offset: float = 1e-9, stride: int = 60) -> go.Figure:
    """Two runs whose starting points differ by ``offset``, and the gap between them."""
    first, second = perturbed_pair(START, offset=offset, dt=DT, steps=STEPS)
    gap = separation(first, second)
    time = np.arange(first.shape[0]) * DT
    frame_steps = range(0, first.shape[0], stride)

    figure = make_subplots(
        rows=1, cols=2, column_widths=[0.62, 0.38],
        specs=[[{"type": "scene"}, {"type": "xy"}]],
        subplot_titles=("Two trajectories", "Distance between them"),
    )

    for path, name, colour in ((first, "original", "#1f77b4"), (second, "perturbed", "#d62728")):
        figure.add_trace(
            go.Scatter3d(x=path[:, 0], y=path[:, 1], z=path[:, 2], mode="lines",
                         line=dict(color=colour, width=1), opacity=0.25,
                         name=name, showlegend=True, hoverinfo="skip"),
            row=1, col=1,
        )
    for path, name, colour in ((first, "original", "#1f77b4"), (second, "perturbed", "#d62728")):
        figure.add_trace(
            go.Scatter3d(x=[path[0, 0]], y=[path[0, 1]], z=[path[0, 2]], mode="markers",
                         marker=dict(size=6, color=colour), name=f"{name} (now)",
                         showlegend=False),
            row=1, col=1,
        )

    figure.add_trace(
        go.Scatter(x=time, y=gap, mode="lines", line=dict(color="#444", width=1.5),
                   name="separation", showlegend=False,
                   hovertemplate="t %{x:.1f}<br>gap %{y:.2e}<extra></extra>"),
        row=1, col=2,
    )
    figure.add_trace(
        go.Scatter(x=[time[0]], y=[gap[0]], mode="markers",
                   marker=dict(size=9, color="#d62728"), showlegend=False),
        row=1, col=2,
    )

    frames = [
        go.Frame(
            name=f"{time[k]:.1f}",
            data=[
                go.Scatter3d(x=[first[k, 0]], y=[first[k, 1]], z=[first[k, 2]]),
                go.Scatter3d(x=[second[k, 0]], y=[second[k, 1]], z=[second[k, 2]]),
                go.Scatter(x=[time[k]], y=[gap[k]]),
            ],
            traces=[2, 3, 5],
        )
        for k in frame_steps
    ]
    figure.frames = frames

    figure.update_layout(
        title=(
            f"A difference of {offset:.0e} in one coordinate, "
            "amplified until nothing is shared"
        ),
        scene=_scene(),
        margin=dict(l=0, r=0, t=70, b=0),
        height=680,
        legend=dict(x=0.02, y=0.98),
        updatemenus=[_play_controls(60)],
        sliders=[_slider(frames, prefix="t = ")],
    )
    figure.update_xaxes(title_text="Time (dimensionless)", row=1, col=2)
    figure.update_yaxes(title_text="Separation", type="log", row=1, col=2)
    return figure


def figure_ensemble(
    members: int = 300, spread: float = 1e-3, stride: int = 25, steps: int = 3000
) -> go.Figure:
    """A tiny ball of initial states, advanced together.

    This is the picture behind ensemble forecasting: the cloud stays compact for a while,
    then shears along the attractor and finally spreads over both wings. Once it has, the
    only honest forecast left is a probability.
    """

    generator = np.random.default_rng(1963)
    settled = integrate(START, dt=DT, steps=SETTLE)[-1]
    cloud = settled + spread * generator.standard_normal((members, 3))

    paths = integrate(cloud, dt=DT, steps=steps)
    time = np.arange(paths.shape[0]) * DT
    shading = cloud[:, 0] - cloud[:, 0].mean()
    limit = float(np.abs(shading).max())
    frame_steps = range(0, paths.shape[0], stride)

    def scatter(index: int) -> go.Scatter3d:
        return go.Scatter3d(
            x=paths[index, :, 0], y=paths[index, :, 1], z=paths[index, :, 2],
            mode="markers",
            marker=dict(size=2.5, color=shading, colorscale="RdBu",
                        cmin=-limit, cmax=limit,
                        colorbar=dict(title="Start<br>offset in x")),
            hoverinfo="skip",
        )

    frames = [go.Frame(data=[scatter(k)], name=f"{time[k]:.1f}") for k in frame_steps]
    figure = go.Figure(data=[scatter(0)], frames=frames)
    figure.update_layout(
        title=(
            f"{members} states starting within {spread:g} of each other, "
            "advanced together"
        ),
        scene=_scene(),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
        updatemenus=[_play_controls(70)],
        sliders=[_slider(frames, prefix="t = ")],
    )
    return figure


def _play_controls(frame_ms: int) -> dict:
    step = dict(frame=dict(duration=frame_ms, redraw=True), mode="immediate")
    return dict(
        type="buttons", showactive=False, x=0.02, y=0.05, xanchor="left",
        buttons=[
            dict(label="Play", method="animate", args=[None, step]),
            dict(label="Pause", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode="immediate")]),
        ],
    )


def _slider(frames, prefix: str) -> dict:
    return dict(
        active=0, x=0.14, len=0.82, y=0.05,
        currentvalue=dict(prefix=prefix),
        steps=[
            dict(label=frame.name, method="animate",
                 args=[[frame.name], dict(frame=dict(duration=0, redraw=True),
                                          mode="immediate")])
            for frame in frames
        ],
    )


def _save(figure: go.Figure, name: str) -> None:
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    destination = FIGURE_ROOT / f"{name}.html"
    figure.write_html(destination, include_plotlyjs=True, full_html=True)
    print(f"  {destination.relative_to(PROJECT_ROOT)}  "
          f"({destination.stat().st_size / 1e6:.1f} MB)")


def main() -> None:
    print("Building Lorenz figures into figures/lorenz/")
    _save(figure_attractor(), "attractor")
    _save(figure_sensitive_dependence(), "sensitive_dependence")
    _save(figure_ensemble(), "ensemble")

    exponent = largest_lyapunov(renormalisations=2000, discard=200)
    doubling = np.log(2) / exponent
    print(f"\nLargest Lyapunov exponent: {exponent:.3f} per time unit")
    print(f"An error doubles every {doubling:.2f} time units.")


if __name__ == "__main__":
    main()
