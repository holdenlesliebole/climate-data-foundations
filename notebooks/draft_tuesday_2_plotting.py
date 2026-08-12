# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Making figures that say something
#
# **DRAFT — not yet promoted to the course sequence.**
#
# Four datasets, four decisions. The plot type follows the question, the axes carry units, and the colormap is chosen from the kind of quantity, not from taste.
#
# | Minutes | Activity | Decision |
# |---|---|---|
# | 0–12 | Anatomy of a figure | what belongs on an Axes |
# | 12–26 | Pier temperature | how to draw a record with gaps |
# | 26–43 | Keeling curve | what the x-range decides |
# | 43–48 | Break | |
# | 48–62 | MOP waves | which plot type answers which question |
# | 62–78 | Sea surface temperature | sequential vs diverging colour |
# | 78–85 | Exploratory vs publication; exit ticket | who the figure is for |

# %% [markdown]
# ## Preflight
#
# Run this first. It names the fix if anything is missing. This notebook does not depend on any other notebook having been run.

# %%
import sys

print("Python:", sys.version.split()[0])
print("Interpreter:", sys.executable)

required = ["numpy", "pandas", "matplotlib", "xarray"]
netcdf_engines = ["netCDF4", "h5netcdf"]

missing = [p for p in required if not __import__("importlib").util.find_spec(p)]
engines = [p for p in netcdf_engines if __import__("importlib").util.find_spec(p)]

if missing:
    print("\nMISSING:", ", ".join(missing))
    print("Fix: conda activate climate-data-foundations   (then re-select the kernel)")
elif not engines:
    print("\nNo NetCDF engine found. The wave and map sections need one:")
    print("  conda install -c conda-forge netcdf4")
else:
    print(f"\nPASS — all packages present. NetCDF engine(s): {', '.join(engines)}")

# %% [markdown]
# ## Self-containment layer
#
# You do not need to read this cell. Every dataset loads in three tiers — local copy, then download, then a labelled synthetic stand-in — and nothing raises. A dead network costs you real data, never the session. Stand-ins stamp `[SYNTHETIC]` into the figure title; do not write a field note about them.

# %%
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr


def find_project_root(start=None):
    """Walk upward for a course marker; fall back to the current folder rather than failing."""
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "environment.yml").exists() or (candidate / "myst.yml").exists():
            return candidate
    return here.parent if here.name in {"notebooks", "reference"} else here


def find_data_file(patterns, roots):
    """Return the first file matching any pattern, searched recursively across several roots."""
    for root in roots:
        if not root.exists():
            continue
        for pattern in patterns:
            hits = sorted(p for p in root.rglob(pattern) if p.is_file())
            if hits:
                return hits[0]
    return None


def fetch_once(url, destination, timeout=90):
    """Download unless a non-empty local copy exists. Never raises; returns True on success."""
    if destination.exists() and destination.stat().st_size > 0:
        print(f"  using local copy: {destination.name}")
        return True
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    try:
        with urlopen(url, timeout=timeout) as response, partial.open("wb") as stream:
            stream.write(response.read())
        if partial.stat().st_size == 0:
            raise ValueError("empty response")
        partial.replace(destination)
        print(f"  downloaded {destination.stat().st_size:,} bytes -> {destination.name}")
        return True
    except Exception as error:
        partial.unlink(missing_ok=True)
        print(f"  network fetch failed ({type(error).__name__}: {error})")
        return False


PROJECT_ROOT = find_project_root()
RAW = PROJECT_ROOT / "data" / "raw"
PROVENANCE = {}


def note(key, is_real, detail):
    """Record where a dataset came from and say so out loud."""
    PROVENANCE[key] = (is_real, detail)
    print(f"  {'REAL' if is_real else 'SYNTHETIC'}: {detail}")


def title_for(key, text):
    """Stamp synthetic figures so nobody mistakes a stand-in for a measurement."""
    is_real, _ = PROVENANCE.get(key, (True, ""))
    return text if is_real else f"{text}   [SYNTHETIC — not real data]"


print("Project root:", PROJECT_ROOT)

# %% [markdown]
# **Instructors:** run every loader once on a good connection before class. Each dataset then caches under `data/raw/` and the session runs offline.

# %% [markdown]
# ## 1. The anatomy of a figure
#
# ```python
# fig, ax = plt.subplots()
# ```
#
# The **Figure** (`fig`) is the sheet of paper: size, layout, saving. The **Axes** (`ax`) is one panel on it: data, labels, ticks, legend, title. Almost everything you want to change is a method on `ax`.
#
# Start with a deliberately bad figure.

# %%
days = np.arange(1, 15)
temperature_c = np.array(
    [16.1, 16.3, 16.2, 16.5, 16.9, 17.2, 17.0, 17.4, 16.6, 16.4, 16.2, 16.0, 15.9, 16.1]
)

fig, ax = plt.subplots()
ax.plot(temperature_c)

# %% [markdown]
# **What can a reader not determine from that?** TODO
#
# At minimum: x is an array position, not a day; no units; no quantity; no source. Drawn correctly, communicates nothing.
#
# Now add one thing at a time — run the next cell, then comment out lines to see what each contributes.

# %%
fig, ax = plt.subplots(figsize=(7, 3.5))

ax.plot(days, temperature_c, marker="o", markersize=4)
ax.set_xlabel("Day of January 2026")
ax.set_ylabel("Surface temperature (°C)")
ax.set_title("Example surface temperature record (invented values)")
ax.grid(alpha=0.25)

fig.tight_layout()

# %% [markdown]
# - **`figsize` is a decision.** The default is square-ish; a time series wants to be wide.
# - **Every axis label carries a unit.** `Surface temperature (°C)`, never `temp`.
# - **`fig.tight_layout()`** stops clipped labels. `plt.subplots(layout="constrained")` does it automatically and handles multi-panel better.
#
# **Your turn:** redraw the same data as a bar chart.

# %%
# Your bar chart:


# %% [markdown]
# **Line or bars, and why?** TODO
#
# A line claims the quantity exists between the points. Bars imply separate countable things. Sampled temperature justifies a line; daily rainfall totals would justify bars.

# %% [markdown]
# ## 2. A real record has gaps

# %%
def load_pier_temperature():
    """Find the Pier record wherever it lives in this project; fall back to a stand-in."""
    # Different authors have put this file in different places, so search rather than assume.
    path = find_data_file(
        patterns=["*TEMP*.csv", "*temp*.csv", "*Temp*.csv"],
        roots=[RAW / "pier", RAW, PROJECT_ROOT / "data", PROJECT_ROOT],
    )

    if path is not None:
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
            header_row = next(
                i for i, line in enumerate(lines) if line.upper().lstrip('" ').startswith("YEAR")
            )
            frame = pd.read_csv(path, skiprows=header_row, low_memory=False)
            frame.columns = [str(c).strip().lower() for c in frame.columns]
            frame["date"] = pd.to_datetime(
                frame[["year", "month", "day"]], errors="coerce"
            )
            frame = frame.dropna(subset=["date"])
            note("pier", True, f"{path.relative_to(PROJECT_ROOT)} (header line {header_row + 1})")
            return frame
        except Exception as error:
            print(f"  found {path.name} but could not parse it ({type(error).__name__}: {error})")

    rng = np.random.default_rng(20260807)
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    seasonal = 16.5 + 3.0 * np.sin(2 * np.pi * (dates.dayofyear.to_numpy() - 100) / 365.25)
    surface = seasonal + rng.normal(0, 0.6, len(dates))
    bottom = seasonal - 1.2 + rng.normal(0, 0.5, len(dates))
    surface[(dates >= "2024-06-10") & (dates <= "2024-07-05")] = np.nan
    note("pier", False, "generated stand-in — do not interpret these values")
    return pd.DataFrame({"date": dates, "surface_temp": surface, "bottom_temp": bottom})


pier = load_pier_temperature()
pier.head()

# %%
# Identify the surface and bottom columns in whichever version you loaded.
surface_col = next(c for c in pier.columns if "surf" in c.lower())
bottom_col = next(c for c in pier.columns if "bot" in c.lower())
print("surface column:", surface_col)
print("bottom column: ", bottom_col)
print("missing surface values:", int(pier[surface_col].isna().sum()))

# %% [markdown]
# Surface and bottom share a unit, so they belong on one Axes. Two series means you need a legend — and vary the linestyle too, so the figure survives greyscale printing and colour vision deficiency.

# %%
window = pier[(pier["date"] >= "2024-05-01") & (pier["date"] <= "2024-09-30")]

fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")

ax.plot(window["date"], window[surface_col], lw=1.5, ls="-", label="Surface")
ax.plot(window["date"], window[bottom_col], lw=1.5, ls="--", label="Bottom")

ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title(title_for("pier", "Scripps Pier temperature, summer 2024"))
ax.legend()
ax.grid(alpha=0.25)

# %% [markdown]
# ### The gap
#
# Matplotlib breaks a line at `NaN`, so a missing stretch shows as a gap rather than a straight segment bridging it. That default is doing you a favour: a filled gap looks exactly as confident as measurement.

# %%
filled = window[surface_col].interpolate()

fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
ax.plot(window["date"], filled, lw=2.5, color="0.75", label="Interpolated across the gap")
ax.plot(window["date"], window[surface_col], lw=1.5, color="C0", label="Measured")
ax.set_xlabel("Date")
ax.set_ylabel("Surface temperature (°C)")
ax.set_title(title_for("pier", "What interpolation invents"))
ax.legend()
ax.grid(alpha=0.25)

# %% [markdown]
# - **Without the blue line on top, could a reader tell the grey section was not measured?** TODO
# - **When is filling the gap right, and what must the caption say?** TODO

# %% [markdown]
# ## 3. The Keeling curve, and what the x-range decides
#
# Atmospheric CO₂ at Mauna Loa, begun by Charles David Keeling in 1958 and continued by the Scripps CO₂ Program. The file has ~60 lines of citation and methods before the data, a three-row header, and `-99.99` for missing — the Monday structure, a different provider.

# %%
keeling_url = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"
keeling_path = RAW / "keeling" / "monthly_in_situ_co2_mlo.csv"

keeling_is_real = fetch_once(keeling_url, keeling_path)

# %% [markdown]
# The preamble is not clutter — citation, the station move to Maunakea, the calibration scale, and the meaning of every column.

# %%
if keeling_is_real:
    lines = keeling_path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines[:5] + ["   ..."] + lines[40:68]:
        print(line[:110])
else:
    lines = []
    print("No local Keeling file. The preamble inspection needs the real file — read it at:")
    print(" ", keeling_url)

# %% [markdown]
# Find the first data row rather than hard-coding it — the file grows and providers reformat.

# %%
column_names = [
    "year", "month", "excel_date", "decimal_date",
    "co2_ppm", "co2_seasonally_adjusted_ppm",
    "co2_fit_ppm", "co2_fit_seasonally_adjusted_ppm",
    "co2_filled_ppm", "co2_filled_seasonally_adjusted_ppm",
    "station",
]


def load_keeling():
    """Parse the local Scripps file, or return a labelled stand-in with the same columns."""
    if keeling_is_real:
        try:
            first_data_row = next(
                i for i, line in enumerate(lines) if line.strip().startswith(("1957", "1958"))
            )
            print("Data start on line:", first_data_row + 1)
            frame = pd.read_csv(
                keeling_path,
                skiprows=first_data_row,
                names=column_names,
                na_values=[-99.99],
                skipinitialspace=True,
            )
            frame["date"] = pd.to_datetime(
                dict(year=frame["year"], month=frame["month"], day=15)
            )
            frame = frame.dropna(subset=["co2_ppm"])
            note("keeling", True, f"{keeling_path.relative_to(PROJECT_ROOT)}, {len(frame)} months")
            return frame
        except Exception as error:
            print(f"  parse failed ({type(error).__name__}: {error})")

    # Stand-in: an exponential-ish rise plus a seasonal cycle. The shape is right; the values are not.
    months = pd.date_range("1958-03-15", "2026-05-15", freq="MS") + pd.Timedelta(days=14)
    years_elapsed = (months.year - 1958) + (months.month - 1) / 12
    trend = 315 + 0.85 * years_elapsed + 0.012 * years_elapsed**2
    seasonal = 3.0 * np.sin(2 * np.pi * (months.month - 5) / 12)
    frame = pd.DataFrame(
        {
            "date": months,
            "year": months.year,
            "month": months.month,
            "co2_ppm": trend + seasonal,
            "co2_seasonally_adjusted_ppm": trend,
            "station": "SYNTHETIC",
        }
    )
    note("keeling", False, "generated stand-in — the shape is right, the values are not")
    return frame


co2 = load_keeling()
print("Coverage:", co2["date"].min().date(), "to", co2["date"].max().date())
co2[["date", "co2_ppm", "co2_seasonally_adjusted_ppm"]].tail()

# %% [markdown]
# > Without `na_values=[-99.99]`, every missing month becomes a number ~400 ppm below the truth and the plot still looks like a plot.

# %%
fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
ax.plot(co2["date"], co2["co2_ppm"], lw=1.0)
ax.set_xlabel("Year")
ax.set_ylabel("CO₂ concentration (ppm)")
ax.set_title(title_for("keeling", "Atmospheric CO₂ at Mauna Loa (Scripps CO₂ Program)"))
ax.grid(alpha=0.25)

# %% [markdown]
# ### The same data, three ranges
#
# Nothing changes but `set_xlim`.

# %%
ranges = [
    ("1958-01-01", "2026-12-31", "The whole record"),
    ("2016-01-01", "2026-12-31", "The last decade"),
    ("2023-01-01", "2026-12-31", "The last three years"),
]

fig, axes = plt.subplots(3, 1, figsize=(9, 8), layout="constrained")

for ax, (start, end, label) in zip(axes, ranges):
    ax.plot(co2["date"], co2["co2_ppm"], lw=1.2)
    ax.set_xlim(pd.Timestamp(start), pd.Timestamp(end))
    shown = co2[(co2["date"] >= start) & (co2["date"] <= end)]["co2_ppm"]
    ax.set_ylim(shown.min() - 2, shown.max() + 2)
    ax.set_ylabel("CO₂ (ppm)")
    ax.set_title(label, fontsize=10, loc="left")
    ax.grid(alpha=0.25)

axes[-1].set_xlabel("Year")

# %% [markdown]
# - **Which panel makes the seasonal cycle the story? Which makes the trend the story?** TODO
# - **A reader who saw only the third panel would conclude what?** TODO
# - **Is any panel dishonest?** TODO
#
# None of them is, which is the uncomfortable part. The axis range is an argument, and you have to make one — there is no neutral choice. What you owe the reader is a caption saying which range you chose.

# %% [markdown]
# ### What seasonal adjustment removes

# %%
recent = co2[co2["date"] >= "2015-01-01"]

fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
ax.plot(recent["date"], recent["co2_ppm"], lw=1.2, ls="-", label="Monthly mean")
ax.plot(
    recent["date"], recent["co2_seasonally_adjusted_ppm"],
    lw=1.8, ls="--", label="Seasonally adjusted",
)
ax.set_xlabel("Year")
ax.set_ylabel("CO₂ concentration (ppm)")
ax.set_title(title_for("keeling", "What seasonal adjustment removes"))
ax.legend()
ax.grid(alpha=0.25)

# %% [markdown]
# **Why does CO₂ dip every northern summer?** TODO
#
# **One rule, stated once:** never put two different units on two y-axes. A second y-axis lets you slide two scales until the curves appear to agree, and that agreement is manufactured by the axis limits. Use two stacked panels with `sharex=True`, or index both to a common baseline.

# %% [markdown]
# ## Break
#
# Five minutes. Switch driver and navigator.

# %% [markdown]
# ## 4. When a line is the wrong plot
#
# Wave data from the CDIP MOP model point nearest the Pier. One dataset, three questions, three plot types.

# %%
site = "D0513"
start, end = "2026-07-01T00:00:00Z", "2026-07-07T23:00:00Z"   # confirm inside current coverage
variables = ["waveHs", "waveTp", "waveDp", "waveFlagPrimary"]

parameters = [("var", v) for v in variables] + [
    ("stns", "all"), ("time_start", start), ("time_end", end),
    ("timeStride", "1"), ("accept", "netcdf4"),
]
mop_url = (
    "https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/"
    f"MOP_alongshore/{site}_nowcast.nc?{urlencode(parameters)}"
)
mop_path = RAW / "mop" / f"{site}_{start[:10]}_{end[:10]}.nc"


def load_mop():
    """Open the local MOP response, or return a labelled stand-in with the same variables."""
    if fetch_once(mop_url, mop_path):
        try:
            with xr.open_dataset(mop_path) as opened:
                dataset = opened.load()
            note("mop", True, f"{mop_path.relative_to(PROJECT_ROOT)}, {dataset.sizes['obs']} hours")
            return dataset
        except Exception as error:
            print(f"  could not open the NetCDF ({type(error).__name__}: {error})")

    rng = np.random.default_rng(513)
    hours = pd.date_range(start[:19], periods=168, freq="h")
    swell = 0.55 + 0.25 * np.sin(2 * np.pi * np.arange(168) / 62)
    dataset = xr.Dataset(
        {
            "waveHs": ("obs", np.clip(swell + rng.normal(0, 0.05, 168), 0.05, None)),
            "waveTp": ("obs", np.round(6.5 + 2.0 * np.sin(2 * np.pi * np.arange(168) / 71)
                                       + rng.normal(0, 0.4, 168), 1)),
            "waveDp": ("obs", (270 + 25 * np.sin(2 * np.pi * np.arange(168) / 47)) % 360),
            "waveFlagPrimary": ("obs", np.ones(168)),
        },
        coords={"time": ("obs", hours)},
    )
    dataset["waveHs"].attrs = {"units": "meter", "long_name": "significant wave height"}
    dataset["waveTp"].attrs = {"units": "second", "long_name": "peak wave period"}
    dataset["waveDp"].attrs = {"units": "degreeT", "long_name": "peak wave direction"}
    note("mop", False, "generated stand-in — plausible wave statistics, not a real forecast")
    return dataset


mop = load_mop()
print(dict(mop.sizes))
print("waveHs units:", mop["waveHs"].attrs.get("units"))
print("waveTp units:", mop["waveTp"].attrs.get("units"))

# %% [markdown]
# **How did wave height change over the week?** Change over time — a line.

# %%
fig, ax = plt.subplots(figsize=(10, 3.5), layout="constrained")
ax.plot(mop["time"], mop["waveHs"], lw=1.5)
ax.set_xlabel("Time (UTC)")
ax.set_ylabel(f"Significant wave height ({mop['waveHs'].attrs.get('units', 'units not stated')})")
ax.set_title(title_for("mop", f"CDIP MOP {site}: significant wave height"))
ax.grid(alpha=0.25)

# %% [markdown]
# **What heights are typical?** A distribution. Time is not part of the answer, so discard it.

# %%
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
ax.hist(mop["waveHs"].values.ravel(), bins=20, edgecolor="white")
ax.set_xlabel("Significant wave height (m)")
ax.set_ylabel("Number of hours")
ax.set_title(title_for("mop", f"Distribution of hourly wave height, {start[:10]} to {end[:10]}"))
ax.grid(alpha=0.25, axis="y")

# %% [markdown]
# Set `bins` to 5, then 60, and rerun.
#
# - **What does 5 bins hide?** TODO
# - **What does 60 bins invent?** TODO
#
# Bin count is a modelling choice with no right default — which is why a histogram should never be your only view of a distribution.

# %% [markdown]
# **Do longer waves tend to be bigger?** Two quantities at the same times — a scatter. Friday supplies the statistics; today, just draw it well.

# %%
hs = mop["waveHs"].values.ravel()
tp = mop["waveTp"].values.ravel()

fig, ax = plt.subplots(figsize=(5.5, 5), layout="constrained")
ax.scatter(tp, hs, s=18, alpha=0.5, edgecolor="none")
ax.set_xlabel(f"Peak period ({mop['waveTp'].attrs.get('units', 'units not stated')})")
ax.set_ylabel(f"Significant wave height ({mop['waveHs'].attrs.get('units', 'units not stated')})")
ax.set_title(title_for("mop", f"CDIP MOP {site}: height against period"))
ax.grid(alpha=0.25)

# %% [markdown]
# Set `alpha=1.0` and rerun. With opaque markers, forty stacked points look like one, so dense regions read the same as sparse ones.
#
# - **One sentence on what the scatter shows. Resist "causes".** TODO
#
# **Your turn** — one more figure, plot type chosen from the question:
#
# 1. Does the height–period relationship change through the week? Colour the scatter by day and add a labelled colorbar.
# 2. Does wave height have a daily cycle?
# 3. Does peak period change smoothly or in steps?
#
# First check `np.unique(mop["waveFlagPrimary"].values)`. For a calm week they may all be `1` (good) — "nothing to see here" is a real result, and finding that out before building a figure around it is the point.

# %%
# Your figure:


# %% [markdown]
# - **My question:** TODO
# - **Why this plot type:** TODO

# %% [markdown]
# ## 5. A map, and the one colour decision that matters
#
# Gridded data has a value at every lat–lon point, so it needs a coloured cell plus a colorbar. NOAA ERSSTv5: monthly 2° global SST since 1854, served over OPeNDAP so xarray transfers only the slices we ask for.

# %%
ersst_url = "https://psl.noaa.gov/thredds/dodsC/Datasets/noaa.ersst.v5/sst.mnmean.nc"
ersst_cache = RAW / "ersst" / "ersst_v5_july_fields.nc"


def load_sst_fields():
    """Return (latest July, 1991-2020 July mean, label). Caches the two subsets for offline reuse."""
    if ersst_cache.exists():
        try:
            with xr.open_dataset(ersst_cache) as opened:
                cached = opened.load()
            note("sst", True, f"{ersst_cache.relative_to(PROJECT_ROOT)} (cached subset)")
            return (cached["latest_july"], cached["baseline_july"],
                    f"ERSSTv5, July {cached.attrs['label']}")
        except Exception as error:
            print(f"  cache unreadable ({type(error).__name__}); refetching")

    try:
        print("  opening ERSSTv5 over OPeNDAP (only the requested slices transfer)...")
        source = xr.open_dataset(ersst_url)
        july = source["sst"].isel(time=(source["time"].dt.month == 7))
        baseline_window = july.sel(time=slice("1991-01-01", "2020-12-31"))

        latest = july.isel(time=-1).load()
        label = str(latest["time"].values)[:7]
        baseline = baseline_window.mean("time").load()
        print(f"  most recent July: {label}; baseline is the mean of "
              f"{baseline_window.sizes['time']} Julys")

        # Preserve the exact subset analysed, so this section runs offline from now on.
        try:
            ersst_cache.parent.mkdir(parents=True, exist_ok=True)
            snapshot = xr.Dataset(
                {
                    "latest_july": latest.reset_coords(drop=True),
                    "baseline_july": baseline.reset_coords(drop=True),
                }
            )
            snapshot.attrs = {"label": label, "source": ersst_url}
            snapshot.to_netcdf(ersst_cache)
            print(f"  cached subset -> {ersst_cache.relative_to(PROJECT_ROOT)}")
        except Exception as error:
            print(f"  (could not write the cache: {type(error).__name__}) — continuing")

        note("sst", True, f"NOAA ERSSTv5 via OPeNDAP, July {label}")
        return latest, baseline, f"ERSSTv5, July {label}"
    except Exception as error:
        print(f"  OPeNDAP unavailable ({type(error).__name__}: {error})")

    # Stand-in: an idealised aquaplanet. Right shape and units, no continents, invented values.
    lat = xr.DataArray(np.arange(-88, 89, 2.0), dims="lat", name="lat")
    lon = xr.DataArray(np.arange(0, 360, 2.0), dims="lon", name="lon")
    lat2d, lon2d = np.meshgrid(lat, lon, indexing="ij")
    zonal = 30.0 * np.cos(np.deg2rad(lat2d)) ** 2 - 2.0
    warm_pool = 3.0 * np.exp(-(((lon2d - 150) / 45) ** 2 + ((lat2d - 0) / 22) ** 2))
    baseline = xr.DataArray(zonal + warm_pool, coords={"lat": lat, "lon": lon}, dims=("lat", "lon"))
    anomaly = (
        2.4 * np.exp(-(((lon2d - 250) / 38) ** 2 + ((lat2d + 3) / 14) ** 2))
        - 1.5 * np.exp(-(((lon2d - 40) / 30) ** 2 + ((lat2d - 40) / 16) ** 2))
    )
    latest = baseline + anomaly
    note("sst", False, "idealised aquaplanet stand-in — no continents, invented values")
    return latest, baseline, "idealised aquaplanet"


latest_july, baseline_july, sst_label = load_sst_fields()
print("Grid:", dict(latest_july.sizes))
print("Units: degC (ERSSTv5 reports degC; the stand-in uses the same units)")

# %% [markdown]
# ### A magnitude gets sequential colour
#
# SST runs cold to warm with no meaningful middle. Use a perceptually uniform sequential map (`viridis`, `cividis`, `magma`) so equal steps in the data look like equal steps in colour, and "darker means more" is all a reader must learn.

# %%
fig, ax = plt.subplots(figsize=(10, 4.5), layout="constrained")

mesh = ax.pcolormesh(
    latest_july["lon"], latest_july["lat"], latest_july,
    cmap="viridis", shading="auto",
)
bar = fig.colorbar(mesh, ax=ax, extend="both")
bar.set_label("Sea surface temperature (°C)")

ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Latitude (°N)")
ax.set_title(title_for("sst", f"Sea surface temperature — {sst_label}"))

# %% [markdown]
# White is land, where the variable has no value. A colorbar without a label is unreadable.

# %% [markdown]
# ### A departure gets diverging colour
#
# Subtract the baseline and the quantity becomes an **anomaly**: zero is meaningful and the sign matters. A sequential map would put zero at some arbitrary green. Use two hues meeting at a neutral midpoint, with **symmetric limits** so zero lands exactly on neutral — without `vmin=-vmax` the neutral colour sits somewhere else and every reader misreads the sign.

# %%
anomaly = latest_july - baseline_july
limit = float(np.nanpercentile(np.abs(anomaly.values), 99))

fig, ax = plt.subplots(figsize=(10, 4.5), layout="constrained")

mesh = ax.pcolormesh(
    anomaly["lon"], anomaly["lat"], anomaly,
    cmap="RdBu_r", vmin=-limit, vmax=limit, shading="auto",
)
bar = fig.colorbar(mesh, ax=ax, extend="both")
bar.set_label("SST anomaly (°C)")

ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Latitude (°N)")
ax.set_title(
    title_for("sst", f"SST anomaly from the 1991–2020 July mean — {sst_label}")
)

# %% [markdown]
# Rerun the anomaly map with `cmap="viridis"`, then `cmap="jet"`.
#
# - **With `viridis`, where does a reader think zero is?** TODO
# - **With `jet`, what structure appears that is not in the data?** TODO
#
# `jet` and `rainbow` compress some ranges and stretch others, inventing sharp boundaries where the data change smoothly. They also collapse in greyscale and for colour vision deficiency. Do not use them.
#
# | Quantity | Colormap | Requirement |
# |---|---|---|
# | magnitude (SST, wave height) | sequential — `viridis`, `cividis` | — |
# | departure (anomaly, difference, residual) | diverging — `RdBu_r`, `coolwarm` | symmetric limits, `vmin=-vmax` |
# | named categories | qualitative, ≤ 8 colours | vary marker or linestyle too |

# %% [markdown]
# ## 6. Who is the figure for?
#
# Everything above is an **exploratory** figure — made for you, to find out what is in the data. Over-label those: in six months every label you skipped is a question you cannot answer.
#
# A **publication** figure travels with a caption, so the caption carries the title, source, and interpretation, and the figure drops them.
#
# | | Exploratory | Publication |
# |---|---|---|
# | Title | yes | no — the caption is the title |
# | Source line | yes | no — goes in the caption |
# | Axis labels with units | yes | yes |
# | Colorbar label | yes | yes |
# | Panel labels `(a)`, `(b)` | optional | yes, multi-panel |
#
# Build the exploratory habit. Stripping labels for a journal is a two-minute edit; reconstructing an unlabelled figure sometimes is not possible.

# %% [markdown]
# ### Save one figure
#
# Redraw your best figure and save it. Vector PDF keeps text sharp at any size; PNG is for when a dense raster layer dominates.

# %%
PROCESSED = PROJECT_ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# Your figure, then:
# fig.savefig(PROCESSED / "tuesday_figure.pdf", bbox_inches="tight")
# fig.savefig(PROCESSED / "tuesday_figure.png", dpi=300, bbox_inches="tight")


# %% [markdown]
# ## Exit ticket
#
# 1. **You are shown a temperature map drawn in `jet`. Name one thing you cannot trust about it.** TODO
# 2. **Name a figure you made today and one thing a reader could wrongly conclude from it.** TODO

# %% [markdown]
# ## Continuation lane
#
# 1. Put CO₂ and Pier temperature in two stacked panels sharing an x-axis over their overlapping years. Write the caption you would need to claim they are related — then the sentence explaining why the figure does not establish it.
# 2. Plot `waveDp` over the week. Explain the jumps between 1° and 359°, why an arithmetic mean of this variable can point the wrong way, and what plot type suits a circular quantity.
# 3. Small multiples: July SST anomaly for four decades on a shared colour scale. Say what goes wrong if each panel gets its own.
# 4. Rebuild the seasonal cycle yourself — subtract the adjusted series from the monthly mean and plot by calendar month. Compare with the file's description of the adjustment.
