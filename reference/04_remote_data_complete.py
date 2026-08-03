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
# # Reference: reproducible remote data—CDIP MOP
#
# This reference constructs a bounded CDIP THREDDS NCSS request, preserves the exact local response, checks its xarray structure/metadata/flags, and acquires the longer assignment file.
#
# Scientific context: [CDIP MOP introduction](https://cdip.ucsd.edu/documents/index/product_docs/mops/mop_intro.html). Request interface: [D0513 NCSS](https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/MOP_alongshore/D0513_nowcast.nc/dataset.html). Recheck rolling coverage before reusing the dates.

# %%
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlretrieve
import hashlib

import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent
MOP_RAW = PROJECT_ROOT / "data" / "raw" / "mop"
MOP_RAW.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Make request choices visible
#
# D0513 is a near-Pier model-output point. `waveHs` is significant wave height (meters), `waveTp` is peak period (seconds), and `waveDp` is wave-from direction (degrees true). The file attributes—not this prose—are authoritative for a received response. Primary flags classify overall validity; secondary flags describe additional model/input conditions.

# %%
site = "D0513"
variables = ["waveHs", "waveTp", "waveDp", "waveFlagPrimary", "waveFlagSecondary"]
base_url = (
    "https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/"
    f"MOP_alongshore/{site}_nowcast.nc"
)

def build_request(start, end):
    """Return a D0513 NCSS URL for the course variables and date bounds."""
    parameters = [("var", variable) for variable in variables]
    parameters += [
        ("stns", "all"),
        ("time_start", start),
        ("time_end", end),
        ("timeStride", "1"),
        ("accept", "netcdf4"),
    ]
    return f"{base_url}?{urlencode(parameters)}"

def acquire_once(url, destination):
    """Download only when the raw destination is absent; return the local path."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print("Reusing without overwrite:", destination.name)
    else:
        urlretrieve(url, destination)
        print("Downloaded:", destination.name)
    if destination.stat().st_size == 0:
        raise ValueError("Received an empty file")
    return destination


# %% [markdown]
# A list of `(key, value)` pairs preserves repeated `var` keys; a dictionary would collapse them. Encoding the parameters prevents punctuation in timestamps from being interpreted incorrectly.

# %% [markdown]
# ## Seven-day teaching request

# %%
start = "2026-07-01T00:00:00Z"
end = "2026-07-07T23:00:00Z"
request_url = build_request(start, end)
destination = MOP_RAW / f"{site}_2026-07-01_2026-07-07.nc"
print(request_url)
destination = acquire_once(request_url, destination)
print(f"{destination.stat().st_size:,} bytes")

# %%
with xr.open_dataset(destination) as opened:
    mop = opened.load()
mop

# %%
assert mop.sizes["station"] == 1
assert mop.sizes["obs"] == 168
assert set(variables).issubset(mop.data_vars)
print("coverage:", mop.time.min().item(), "to", mop.time.max().item())
print("location:", mop.latitude.values, mop.longitude.values)
for name in variables:
    print("\n", name, mop[name].attrs)

# %%
summary = mop[["waveHs", "waveTp", "waveDp"]].to_dataframe()
display(summary.describe())
display(summary.isna().mean().rename("missing_fraction"))
print("primary flags:", pd.Series(mop.waveFlagPrimary.values).value_counts().sort_index().to_dict())
print("primary meanings:", mop.waveFlagPrimary.attrs.get("flag_meanings"))
print("secondary flags:", pd.Series(mop.waveFlagSecondary.values).value_counts().sort_index().to_dict())
print("secondary meanings:", mop.waveFlagSecondary.attrs.get("flag_meanings"))

# %% [markdown]
# For the development response, all 168 primary flags were `good`; secondary flags were `unspecified`. MOP values are model-derived nearshore output rather than a direct buoy record. A seven-day window is useful for inspecting a wave event, not estimating climate or seasonal behavior.

# %%
good = mop.waveFlagPrimary == 1
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(mop.time, mop.waveHs, label="Significant wave height", lw=1.5)
if bool((~good).any()):
    ax.scatter(mop.time.where(~good), mop.waveHs.where(~good), color="C3", marker="x", label="not good")
ax.set(title=f"CDIP MOP {site}: significant wave height", xlabel="Time (UTC)", ylabel="Wave height (m)")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# ## Assignment-sized request

# %%
assignment_start = "2026-01-01T00:00:00Z"
assignment_end = "2026-07-31T23:00:00Z"
assignment_url = build_request(assignment_start, assignment_end)
assignment_path = acquire_once(
    assignment_url,
    MOP_RAW / f"{site}_2026-01-01_2026-07-31.nc",
)
with xr.open_dataset(assignment_path) as opened:
    assignment_mop = opened.load()
assert assignment_mop.sizes["obs"] == 5088
print(dict(assignment_mop.sizes), assignment_mop.time.min().item(), assignment_mop.time.max().item())

# %%
assignment_frame = assignment_mop[["waveHs", "waveTp"]].to_dataframe().reset_index()
assignment_frame["month"] = assignment_frame["time"].dt.month
jan_jul = assignment_frame.loc[assignment_frame["month"].isin([1, 7])]
display(jan_jul.groupby("month")[["waveHs", "waveTp"]].agg(["count", "mean", "std"]))


# %% [markdown]
# This descriptive January/July summary is a scope check, not the final analysis. A student must still visualize distributions/time behavior, state flag handling and missingness, use the statistical method taught later, and avoid interpreting a single modeled year as a general seasonal climatology.

# %% [markdown]
# ## Exact-byte record and direction warning

# %%
def sha256(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

print("teaching URL:", request_url)
print("teaching SHA-256:", sha256(destination))
print("assignment URL:", assignment_url)
print("assignment SHA-256:", sha256(assignment_path))

# %% [markdown]
# `waveDp` is circular: 1° and 359° are neighbors. An ordinary arithmetic mean can place their average near 180°, the opposite direction. Use a time series, directional bins/polar display, or circular statistics with the file's wave-from convention stated.
#
# The manifest should contain each exact request URL, access timestamp, site/window/variables, local filename, acquisition/recovery method, license/terms, and checksum.
