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
# # Reproducible remote data: a CDIP MOP subset
#
# Today you will build a small request to a scientific data service, save its exact NetCDF response, inspect the metadata and quality/model flags with xarray, and make one bounded wave plot.
#
# Monday used a browser to acquire a versioned archive. Today the variable, site, time, and format choices become visible parameters in code. In both cases, analysis begins from a preserved local raw file.

# %%
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlretrieve
import hashlib

import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists(), "Open the course project folder first."

MOP_RAW = PROJECT_ROOT / "data" / "raw" / "mop"
MOP_RAW.mkdir(parents=True, exist_ok=True)
print("MOP raw folder:", MOP_RAW)

# %% [markdown]
# ## 1. Read the source before constructing the request
#
# Open the [CDIP MOP introduction](https://cdip.ucsd.edu/documents/index/product_docs/mops/mop_intro.html) and the [NCSS request page for site D0513](https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/MOP_alongshore/D0513_nowcast.nc/dataset.html).
#
# With your partner, record:
#
# - What is a MOP output, and how does it differ from a direct buoy observation? **TODO**
# - Current time coverage shown on the request page: **TODO**
# - Site latitude/longitude: **TODO**
# - Units and meaning of `waveHs`, `waveTp`, and `waveDp`: **TODO**
# - Meaning of the two flag variables: **TODO**
# - One limitation you should state beside a plot: **TODO**

# %% [markdown]
# ## 2. Make the scientific choices explicit
#
# Choose a seven-day window inside the coverage you just checked. The dates below worked during course development but the rolling nowcast changes, so update them if necessary.

# %%
site = "D0513"
start = "2026-07-01T00:00:00Z"  # TODO: confirm or change
end = "2026-07-07T23:00:00Z"    # TODO: confirm or change
variables = [
    "waveHs",
    "waveTp",
    "waveDp",
    "waveFlagPrimary",
    "waveFlagSecondary",
]

base_url = (
    "https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/"
    f"MOP_alongshore/{site}_nowcast.nc"
)

# %% [markdown]
# ### Why a list of pairs?
#
# The service expects the key `var` to appear once per variable. A normal Python dictionary cannot preserve repeated keys, so we build a list of `(key, value)` pairs. `urlencode` then handles punctuation in the timestamps safely.

# %%
parameters = [("var", variable) for variable in variables]
parameters += [
    ("stns", "all"),
    ("time_start", start),
    ("time_end", end),
    ("timeStride", "1"),
    ("accept", "netcdf4"),
]

request_url = f"{base_url}?{urlencode(parameters)}"
date_label = f"{start[:10]}_{end[:10]}"
destination = MOP_RAW / f"{site}_{date_label}.nc"

print("Request URL:")
print(request_url)
print("\nLocal destination:")
print(destination.relative_to(PROJECT_ROOT))

# %% [markdown]
# ### Request audit
#
# Read the printed URL. Point to the site, every requested variable, start/end time, stride, and output format.
#
# Before running it, predict:
#
# - How many hourly observations should seven complete days contain? **TODO**
# - Which dimensions and coordinates do you expect? **TODO**
# - Roughly how large should a one-site, five-variable file be: KB, MB, or GB? **TODO**

# %% [markdown]
# ## 3. Acquire once and preserve the response
#
# The guard below makes an existing raw file a visible decision rather than silently overwriting it. If you need a different request, change the dates/variables and therefore the filename.

# %%
if destination.exists():
    print("Raw file already exists; reusing it without overwriting.")
else:
    urlretrieve(request_url, destination)
assert destination.stat().st_size > 0
print(f"Local file contains {destination.stat().st_size:,} bytes")

# %% [markdown]
# If the request failed, read the error before changing anything. Check the classroom network, current coverage, variable spelling, printed URL, and destination. After the instructor's troubleshooting checkpoint, copy the provided recovery file into `data/raw/mop/` if necessary and set `destination` to that path. Record the recovery route in your manifest.
#
# If the cell reports that the file already exists because you successfully ran it once, the notebook reuses it without overwriting. Do **not** delete raw data merely to make the download happen again.

# %% [markdown]
# ## 4. Open the local NetCDF and inspect
#
# Notice that `open_dataset` receives `destination`, not `request_url`. Acquisition and analysis are now separable.

# %%
assert destination.exists(), f"Local file not found: {destination}"

with xr.open_dataset(destination) as opened:
    mop = opened.load()

mop

# %%
print("Dimensions:", dict(mop.sizes))
print("Time coverage:", mop.time.min().item(), "to", mop.time.max().item())
print("Latitude:", mop.latitude.values)
print("Longitude:", mop.longitude.values)

for name in variables:
    print(f"\n{name}")
    print("  dimensions:", mop[name].dims)
    print("  units:", mop[name].attrs.get("units", "not stated"))
    print("  long_name:", mop[name].attrs.get("long_name", "not stated"))
    print("  valid range:", mop[name].attrs.get("valid_min"), mop[name].attrs.get("valid_max"))

# %%
summary = mop[["waveHs", "waveTp", "waveDp"]].to_dataframe()
display(summary.head())
display(summary.describe())
display(summary.isna().mean().rename("missing_fraction"))

print("Primary flags:")
display(pd.Series(mop.waveFlagPrimary.values).value_counts(dropna=False).sort_index())
print("Primary flag meanings:", mop.waveFlagPrimary.attrs.get("flag_meanings"))

print("Secondary flags:")
display(pd.Series(mop.waveFlagSecondary.values).value_counts(dropna=False).sort_index())
print("Secondary flag meanings:", mop.waveFlagSecondary.attrs.get("flag_meanings"))

# %% [markdown]
# Answer before plotting:
#
# 1. Does the received time coverage match the request?
# 2. Does the number of observations match your prediction?
# 3. What does the `station` dimension represent, and why do the wave variables use `obs`?
# 4. What are the units and valid ranges?
# 5. Are there missing, questionable, or bad values?
# 6. Which flags, if any, will you exclude? State the rule before applying it.
#
# **Answers and flag decision:** TODO

# %% [markdown]
# ## 5. Make one bounded view
#
# For this first plot, retain all values but show where the primary flag is not `good` if any exist. Do not silently discard a flag category.

# %%
good = mop.waveFlagPrimary == 1
not_good = ~good

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(mop.time, mop.waveHs, color="C0", lw=1.5, label="Significant wave height")
if bool(not_good.any()):
    ax.scatter(
        mop.time.where(not_good),
        mop.waveHs.where(not_good),
        color="C3", marker="x", label="Primary flag not good", zorder=3,
    )
ax.set(
    title=f"CDIP MOP {site}: significant wave height",
    xlabel="Time (UTC)",
    ylabel=f"Wave height ({mop.waveHs.attrs.get('units', 'units not stated')})",
)
ax.grid(alpha=0.25)
ax.legend()
fig.text(0.99, -0.02, "Source: CDIP MOP model output", ha="right", fontsize=8)
fig.tight_layout()


# %% [markdown]
# ### Field note
#
# Complete four boxes in one or two sentences each:
#
# - **What:** quantity, units, and modeled/observed status — TODO
# - **Where/when:** site coordinates and time coverage — TODO
# - **Trustworthy because:** one metadata, flag, or validation check — TODO
# - **Limitation:** one reason not to overinterpret this seven-day subset — TODO

# %% [markdown]
# ## 6. Record the exact response

# %%
def sha256(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

print("Request URL:", request_url)
print("Local file:", destination.relative_to(PROJECT_ROOT))
print("SHA-256:", sha256(destination))

# %% [markdown]
# Add a MOP entry to `data/manifest.yml`, including the exact request URL, access time, site, variables, time window, filename, checksum, and whether the file came from your request or the recovery copy.
#
# ## Exit ticket
#
# What would another researcher need in order to repeat this request next month, after the nowcast coverage has changed?
#
# **Answer:** TODO

# %% [markdown]
# ## Required follow-up: acquire the assignment-sized MOP file
#
# The seven-day request is ideal for learning the workflow but cannot support a comparison between months. Before Friday, repeat the same acquisition with the proposed January–July window below. This was only about 79 KB during course development, but you must recheck that the dates remain inside the rolling coverage.
#
# This is a second raw provider response. Preserve it, record its exact URL/checksum in the manifest, and analyze the local file.

# %%
assignment_start = "2026-01-01T00:00:00Z"
assignment_end = "2026-07-31T23:00:00Z"

assignment_parameters = [("var", variable) for variable in variables]
assignment_parameters += [
    ("stns", "all"),
    ("time_start", assignment_start),
    ("time_end", assignment_end),
    ("timeStride", "1"),
    ("accept", "netcdf4"),
]
assignment_url = f"{base_url}?{urlencode(assignment_parameters)}"
assignment_destination = MOP_RAW / f"{site}_2026-01-01_2026-07-31.nc"

print(assignment_url)
print(assignment_destination.relative_to(PROJECT_ROOT))

# %%
if assignment_destination.exists():
    print("Assignment file already exists; reusing the preserved raw file.")
else:
    urlretrieve(assignment_url, assignment_destination)
    print(f"Saved {assignment_destination.stat().st_size:,} bytes")

with xr.open_dataset(assignment_destination) as opened:
    assignment_mop = opened.load()

assert assignment_mop.sizes["obs"] > mop.sizes["obs"]
print(dict(assignment_mop.sizes))
print(assignment_mop.time.min().item(), assignment_mop.time.max().item())
print("SHA-256:", sha256(assignment_destination))

# %% [markdown]
# Add this second file as its own manifest entry. If January–July is no longer available, choose two well-separated months inside the current coverage, update the filename, and tell the instructor which months you selected.
#
# ## Continuation lane
#
# Choose one:
#
# 1. Turn the acquisition cells into a function that accepts site/start/end/variables, refuses overwrites, and returns the local path.
# 2. Request a second non-overlapping seven-day period and compare `waveHs` or `waveTp`. Keep the same axes.
# 3. Make a peak-direction plot. Explain why 1° and 359° are neighbors and why an ordinary arithmetic mean may fail.
# 4. Inspect the NetCDF response with a command-line metadata tool and compare what it reveals with xarray.
#
# Your extension must include one verification check and a sentence explaining why the additional step is scientifically useful.
