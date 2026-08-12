"""Build the interactive 3D figures for the California Current System lesson.

Run ``scripts/fetch_cms_ccs.py`` first. This script reads the preserved responses in
``data/raw/cms_ccs/`` and writes standalone HTML into ``figures/ccs_3d/``. Each file
embeds its own copy of plotly.js, so it opens in any browser and can be dropped into the
Jupyter Book without a network connection.

Five figures:

1. ``hypoxic_boundary``   depth of the O2 = 0.06 mol/m3 surface, as a 3D surface
2. ``depth_sweep_O2``     one horizontal oxygen plane descending through the water column
3. ``depth_sweep_pH``     the same sweep for pH
4. ``nutrient_curtains``  vertical nitrate sections hung at several latitudes
5. ``seasonal_boundary``  the hypoxic boundary across twelve months of 2010

These are teaching figures, not publication figures. Each carries a title because a
standalone HTML file is read without a caption beside it, whereas
``conventions/figure-conventions.md`` assumes a caption always accompanies the image.
That is a deliberate local exception, recorded here and in the lesson notebook.
"""

from pathlib import Path
import sys
import warnings

import numpy as np
import plotly.graph_objects as go
import xarray as xr

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.ccs import (  # noqa: E402
    DEFAULT_HYPOXIC_THRESHOLD,
    hypoxic_boundary_depth,
    load_ccs_subset,
)

RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "cms_ccs"
FIGURE_ROOT = PROJECT_ROOT / "figures" / "ccs_3d"

VOLUME_MONTH = "2010-07"
VOLUME_VARIABLES = ("O2", "NO3", "pH")
SEASONAL_FILE = RAW_ROOT / "ccs_2010_O2_monthly.nc4"

# Longitude spans ~15 degrees, latitude ~10.6, depth ~1 km. Without a manual aspect
# ratio plotly renders a cube and the vertical structure disappears.
SCENE_ASPECT = dict(x=1.5, y=1.1, z=0.7)
DEPTH_TICKS = [0, 200, 400, 600, 800, 1000]

UNITS = {"O2": "mol m⁻³", "NO3": "mol m⁻³", "pH": "total scale"}


def volume_path(variable: str) -> Path:
    return RAW_ROOT / f"ccs_{VOLUME_MONTH}_{variable}.nc4"


def load_volume() -> xr.Dataset:
    """Merge the three single-month responses into one dataset on a shared grid."""
    merged = xr.merge(
        [load_ccs_subset(volume_path(name))[[name]] for name in VOLUME_VARIABLES]
    )
    return merged.squeeze("time", drop=False)


def _scene(zrange: tuple | None = None) -> dict:
    axis = dict(
        title="Depth (m)",
        tickvals=[-d for d in DEPTH_TICKS],
        ticktext=[str(d) for d in DEPTH_TICKS],
    )
    if zrange is not None:
        axis["range"] = list(zrange)
    return dict(
        xaxis=dict(title="Longitude (°E)"),
        yaxis=dict(title="Latitude (°N)"),
        zaxis=axis,
        aspectmode="manual",
        aspectratio=SCENE_ASPECT,
        camera=dict(eye=dict(x=-1.6, y=-1.5, z=0.9)),
    )


def _decimate(data, stride: int):
    if stride <= 1:
        return data
    return data.isel(lat=slice(None, None, stride), lon=slice(None, None, stride))


def figure_hypoxic_boundary(volume: xr.Dataset, stride: int = 2) -> go.Figure:
    """The hero figure: how deep you must go before the water turns hypoxic."""
    boundary = _decimate(hypoxic_boundary_depth(volume["O2"]), stride)
    surface = boundary.values

    figure = go.Figure(
        go.Surface(
            x=boundary["lon"].values,
            y=boundary["lat"].values,
            z=-surface,
            surfacecolor=surface,
            colorscale="Viridis",
            reversescale=True,
            colorbar=dict(title="Depth of<br>O₂ = 0.06<br>mol m⁻³ (m)"),
            hovertemplate=(
                "Longitude %{x:.2f}°E<br>Latitude %{y:.2f}°N"
                "<br>Hypoxic at %{surfacecolor:.0f} m<extra></extra>"
            ),
        )
    )
    figure.update_layout(
        title="Depth of the hypoxic boundary, California Current System, July 2010",
        scene=_scene(zrange=(-1050, 0)),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
    )
    return figure


def figure_depth_sweep(
    volume: xr.Dataset, variable: str = "O2", stride: int = 3
) -> go.Figure:
    """A single horizontal plane animated downward through the water column."""
    data = _decimate(volume[variable], stride)
    field = data.transpose("depth", "lat", "lon").values
    depth = data["depth"].values
    lon, lat = data["lon"].values, data["lat"].values

    finite = field[np.isfinite(field)]
    cmin, cmax = np.percentile(finite, [1, 99])
    units = UNITS[variable]
    scale = "Viridis" if variable != "pH" else "Plasma"

    def plane(index: int) -> go.Surface:
        return go.Surface(
            x=lon,
            y=lat,
            z=np.full((lat.size, lon.size), -depth[index]),
            surfacecolor=field[index],
            colorscale=scale,
            cmin=cmin,
            cmax=cmax,
            colorbar=dict(title=f"{variable}<br>({units})"),
            hovertemplate=(
                "Longitude %{x:.2f}°E<br>Latitude %{y:.2f}°N"
                f"<br>{variable} %{{surfacecolor:.4f}} {units}<extra></extra>"
            ),
        )

    frames = [go.Frame(data=[plane(k)], name=f"{depth[k]:.0f}") for k in range(depth.size)]
    figure = go.Figure(data=[plane(0)], frames=frames)
    figure.update_layout(
        title=f"{variable} on a plane descending through the water column, July 2010",
        scene=_scene(zrange=(-1050, 0)),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
        updatemenus=[_play_controls(frame_ms=180)],
        sliders=[_slider(frames, prefix="Depth: ", suffix=" m")],
    )
    return figure


def figure_nutrient_curtains(
    volume: xr.Dataset, latitudes=(30.0, 32.87, 34.5, 36.5, 38.0)
) -> go.Figure:
    """Vertical nitrate sections hung in 3D, one per latitude line."""
    nitrate = volume["NO3"].transpose("depth", "lat", "lon")
    lon, depth = nitrate["lon"].values, nitrate["depth"].values
    finite = nitrate.values[np.isfinite(nitrate.values)]
    cmin, cmax = np.percentile(finite, [1, 99])

    mesh_lon, mesh_depth = np.meshgrid(lon, -depth)
    figure = go.Figure()
    for position, target in enumerate(latitudes):
        section = nitrate.sel(lat=target, method="nearest")
        actual = float(section["lat"])
        figure.add_trace(
            go.Surface(
                x=mesh_lon,
                y=np.full_like(mesh_lon, actual),
                z=mesh_depth,
                surfacecolor=section.values,
                colorscale="Viridis",
                cmin=cmin,
                cmax=cmax,
                showscale=position == 0,
                colorbar=dict(title="Nitrate<br>(mol m⁻³)"),
                name=f"{actual:.1f}°N",
                hovertemplate=(
                    f"{actual:.2f}°N<br>Longitude %{{x:.2f}}°E"
                    "<br>Nitrate %{surfacecolor:.4f} mol m⁻³<extra></extra>"
                ),
            )
        )

    figure.update_layout(
        title="Nitrate sections across the California Current System, July 2010",
        scene=_scene(zrange=(-1050, 0)),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
    )
    return figure


def figure_seasonal_boundary(seasonal: xr.Dataset, stride: int = 2) -> go.Figure:
    """The hypoxic boundary through the 2010 upwelling season.

    The surface sits at its true depth but is coloured by each cell's departure from its
    own annual mean. Absolute depth varies by hundreds of metres across the domain while
    the seasonal signal is a few tens of metres, so a depth-coloured animation looks
    frozen. The anomaly is the part that moves, and negative means shallower than usual,
    which is what upwelling does.
    """

    oxygen = seasonal["O2"]
    months = [str(value)[:7] for value in oxygen["time"].values]
    surfaces = np.array(
        [
            _decimate(hypoxic_boundary_depth(oxygen.isel(time=k)), stride).values
            for k in range(oxygen.sizes["time"])
        ]
    )
    sample = _decimate(hypoxic_boundary_depth(oxygen.isel(time=0)), stride)
    lon, lat = sample["lon"].values, sample["lat"].values

    # Cells that are land in every month are all-NaN columns; nanmean warns on them.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        annual_mean = np.nanmean(surfaces, axis=0)
    anomaly = surfaces - annual_mean

    finite = anomaly[np.isfinite(anomaly)]
    limit = float(np.percentile(np.abs(finite), 98))

    def layer(index: int) -> go.Surface:
        return go.Surface(
            x=lon,
            y=lat,
            z=-surfaces[index],
            surfacecolor=anomaly[index],
            colorscale="RdBu",
            cmin=-limit,
            cmax=limit,
            colorbar=dict(title="Boundary depth<br>anomaly (m)"),
            hovertemplate=(
                "Longitude %{x:.2f}°E<br>Latitude %{y:.2f}°N"
                "<br>Anomaly %{surfacecolor:+.0f} m<extra></extra>"
            ),
        )

    frames = [go.Frame(data=[layer(k)], name=months[k]) for k in range(len(months))]
    figure = go.Figure(data=[layer(0)], frames=frames)
    figure.update_layout(
        title=(
            "Hypoxic boundary through 2010: depth as shape, "
            "seasonal anomaly as colour (red = shallower than usual)"
        ),
        scene=_scene(zrange=(-700, 0)),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
        updatemenus=[_play_controls(frame_ms=520)],
        sliders=[_slider(frames, prefix="Month: ")],
    )
    return figure


def _play_controls(frame_ms: int) -> dict:
    step = dict(frame=dict(duration=frame_ms, redraw=True), mode="immediate")
    return dict(
        type="buttons",
        showactive=False,
        x=0.02,
        y=0.05,
        xanchor="left",
        buttons=[
            dict(label="Play", method="animate", args=[None, step]),
            dict(
                label="Pause",
                method="animate",
                args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")],
            ),
        ],
    )


def _slider(frames, prefix: str, suffix: str = "") -> dict:
    return dict(
        active=0,
        x=0.14,
        len=0.82,
        y=0.05,
        currentvalue=dict(prefix=prefix, suffix=suffix),
        steps=[
            dict(
                label=frame.name,
                method="animate",
                args=[
                    [frame.name],
                    dict(frame=dict(duration=0, redraw=True), mode="immediate"),
                ],
            )
            for frame in frames
        ],
    )


def _save(figure: go.Figure, name: str) -> None:
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    destination = FIGURE_ROOT / f"{name}.html"
    figure.write_html(destination, include_plotlyjs=True, full_html=True)
    size = destination.stat().st_size / 1e6
    print(f"  {destination.relative_to(PROJECT_ROOT)}  ({size:.1f} MB)")


def main() -> None:
    required = [volume_path(name) for name in VOLUME_VARIABLES] + [SEASONAL_FILE]
    missing = [path for path in required if not path.exists()]
    if missing:
        raise SystemExit(
            "Missing raw subsets:\n  "
            + "\n  ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
            + "\nRun scripts/fetch_cms_ccs.py first."
        )

    print(f"Hypoxia threshold: {DEFAULT_HYPOXIC_THRESHOLD} mol/m3")
    print("Building interactive figures into figures/ccs_3d/")
    volume = load_volume()
    seasonal = load_ccs_subset(SEASONAL_FILE)

    _save(figure_hypoxic_boundary(volume), "hypoxic_boundary")
    _save(figure_depth_sweep(volume, "O2"), "depth_sweep_O2")
    _save(figure_depth_sweep(volume, "pH"), "depth_sweep_pH")
    _save(figure_nutrient_curtains(volume), "nutrient_curtains")
    _save(figure_seasonal_boundary(seasonal), "seasonal_boundary")
    print("Open any file in a browser, or embed it in the Jupyter Book.")


if __name__ == "__main__":
    main()
