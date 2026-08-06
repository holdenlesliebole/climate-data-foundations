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
# # Final analysis: one small climate-data story
#
# Use one course dataset to answer one small question with a transparent chain from source and inspection to a figure, numerical summary, interpretation, and limitation. A careful small prompt can receive full credit.
#
# **Minimum viable takeaway:** reproducible and honest beats ambitious and unfinished.
#
# Plan for 35–60 minutes. You may consult course notes, references, documentation, classmates, instructors, and Copilot, but submit your own notebook and interpretation.

# %% [markdown]
# ## Before you begin: choose the smallest useful question
#
# Recommended small directions:
#
# - **Pier:** compare surface and near-bottom temperature for one month/season; calculate paired surface minus bottom and describe its center/spread.
# - **Pier + global temperature:** compare annual Pier surface SST with NASA global temperature anomaly; show time, report a slope/correlation, and check levels versus changes.
# - **MOP:** compare January/July (or two available months) `waveHs` or `waveTp` with a distribution/time view and summaries.
# - **ERA5:** compare one prepared field or regional mean between two seasons using the same units and scale.
#
# Ask an instructor before using a new dataset or expanding beyond one main figure.

# %% [markdown]
# ## 1. Question and source
#
# **Question (one sentence):** TODO
#
# **Why this small question interests me (one sentence):** TODO
#
# **Dataset record:**
#
# - Provider and dataset title: TODO
# - Landing page or exact request URL: TODO
# - Access date: TODO
# - Local raw filename: TODO
# - Acquired from provider or instructor recovery: TODO
# - Variables, units, and modeled/observed status: TODO

# %%
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists(), "Open the course project folder first."

SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.climate_series import annual_pier_surface, load_gistemp_annual
from climate_course.pier import load_pier_temperature, surface_bottom_difference
from climate_course.statistics import bootstrap_mean_interval

# %% [markdown]
# ## 2. Choose and load one preserved local file
#
# Change `DATASET_CHOICE` to `"pier"`, `"pier_global"`, `"mop"`, or `"era5"`. The cell inventories the expected folder and loads preserved local files; adjust the displayed choice if you have several. Do not point the analysis repeatedly at a live URL.

# %%
DATASET_CHOICE = "pier"  # change to "pier_global", "mop", or "era5"

if DATASET_CHOICE == "pier":
    candidates = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
    assert candidates, "No Pier temperature CSV found."
    source_path = candidates[-1]
    data = load_pier_temperature(source_path)
    source_paths = [source_path]
elif DATASET_CHOICE == "pier_global":
    pier_candidates = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
    gistemp_path = PROJECT_ROOT / "data" / "raw" / "climate" / "NASA_GISTEMP_global.csv"
    assert pier_candidates, "No Pier temperature CSV found."
    assert gistemp_path.exists(), "No preserved NASA GISTEMP CSV found; revisit Friday acquisition."
    pier_path = pier_candidates[-1]
    pier = load_pier_temperature(pier_path)
    annual_pier = annual_pier_surface(pier, min_days=180)
    gistemp = load_gistemp_annual(gistemp_path)
    data = annual_pier.merge(gistemp, on="year", how="inner", validate="one_to_one")
    source_paths = [pier_path, gistemp_path]
elif DATASET_CHOICE == "mop":
    candidates = sorted((PROJECT_ROOT / "data" / "raw" / "mop").glob("*.nc"))
    assert candidates, "No MOP NetCDF found."
    source_path = max(candidates, key=lambda path: path.stat().st_size)
    with xr.open_dataset(source_path) as opened:
        data = opened.load()
    source_paths = [source_path]
elif DATASET_CHOICE == "era5":
    candidates = sorted((PROJECT_ROOT / "data" / "raw" / "era5").glob("*.nc"))
    assert candidates, "No prepared ERA5 NetCDF found; ask the instructor for the course subset."
    source_path = candidates[-1]
    with xr.open_dataset(source_path) as opened:
        data = opened.load()
    source_paths = [source_path]
else:
    raise ValueError("DATASET_CHOICE must be 'pier', 'pier_global', 'mop', or 'era5'.")

print("Analyzing preserved source(s):")
for path in source_paths:
    print(" -", path.relative_to(PROJECT_ROOT))
display(data)

# %% [markdown]
# ## 3. Load and inspect
#
# Show evidence for structure, time coverage, units, flags, and missingness. Reuse a small inspected pattern from notebooks 02, 04, 07, or 09 instead of inventing a new loader.

# %%
# TODO: print/display columns or dimensions, time coverage, units, flags, and missingness.
# Keep this code small and specific to your selected dataset.

# %% [markdown]
# **Inspection note (two to four sentences):** TODO—state what one row/grid cell represents, time/location coverage, relevant units/flags, missingness, and one issue you checked before analysis.

# %% [markdown]
# ## 4. Make one personal scientific choice
#
# Choose a time window, month/season, location, comparison, variable, quality rule, or derived quantity. State the choice before implementing it.
#
# **Choice and reason:** TODO

# %%
# TODO: create a clearly named selected/derived object.
# Examples to adapt, not copy blindly:
# pier_selected = surface_bottom_difference(data, "2020-06-01", "2025-08-31", good_only=True)
# pier_global_selected = data.loc[data.year.between(1960, 2020)].copy()
# mop_frame = data[["waveHs"]].to_dataframe().reset_index()
# era5_selected = data[VARIABLE_NAME].sel(time=slice(START, END))

# %% [markdown]
# **Checks:** What are the selected shape/count, coverage, units, and one known or plausible range? **TODO**

# %% [markdown]
# ## 5. Make one relevant figure
#
# The title should state the quantity/comparison, and every axis/colorbar should include a variable and unit. Show flags or exclusions when they matter. One strong figure is enough.

# %%
fig, ax = plt.subplots(figsize=(8, 4.5))

# TODO: replace this comment with your plot using ax.plot, ax.scatter, ax.hist, ax.boxplot, etc.
# Do not leave an empty figure in the submitted notebook.

ax.set(title="TODO: descriptive title", xlabel="TODO: variable (unit)", ylabel="TODO: variable (unit)")
ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# **Figure observation:** Describe one visible pattern without claiming its cause. **TODO**

# %% [markdown]
# ## 6. Calculate one appropriate numerical summary
#
# Choose one method that matches the question:
#
# | Question type | Possible summary |
# |---|---|
# | Typical value and spread | count, mean/median, SD/IQR |
# | Paired surface–bottom difference | mean/median difference and spread |
# | Difference between groups | group summaries plus Thursday interval/sensitivity |
# | Pier/global-temperature relationship | correlation, slope with units, residual/time or levels/changes view |
# | Peak direction | directional bins/polar plot; avoid ordinary mean near 0°/360° |
#
# Name the method and its units before calculating.
#
# **Chosen summary and why:** TODO

# %%
# TODO: calculate and display one numerical summary.
# Give intermediate objects scientific names and add at least one assertion/plausibility check.

# %% [markdown]
# **Numerical result:** TODO—report the value(s), units, selected sample, and method.

# %% [markdown]
# ## 7. Interpret in four to eight sentences
#
# Include:
#
# 1. the dataset/window/selection;
# 2. the main visual and numerical result with units;
# 3. one assumption behind the comparison/statistic;
# 4. one limitation the result does not resolve; and
# 5. one bounded conclusion—no unsupported cause or generalization.
#
# **Interpretation:** TODO

# %% [markdown]
# ## 8. Peer check and revision
#
# Give your notebook to a partner. The partner should inspect or run it and leave:
#
# - **One question:** TODO
# - **One required fix:** TODO
# - **Partner initials/name:** TODO
#
# **Revision I attempted:** TODO

# %% [markdown]
# ## 9. Collaboration/Copilot note
#
# In one sentence, say how Copilot or another person helped, or that you completed the work without that help. This is context, not a penalty.
#
# **Note:** TODO

# %% [markdown]
# ## 10. Final self-check and submission
#
# - [ ] My question is small enough for one main figure.
# - [ ] I recorded provider/URL/access date/local file/acquisition method.
# - [ ] I showed structure, units, flags, coverage, and missingness.
# - [ ] I made one personal subset/comparison/derived-variable choice.
# - [ ] My figure has a descriptive title, labels, and units.
# - [ ] I named and interpreted one numerical summary.
# - [ ] I stated one assumption and one limitation.
# - [ ] A peer left a question/fix and I attempted a revision.
# - [ ] I included my collaboration/Copilot note.
# - [ ] I restarted the kernel and ran all cells from top to bottom.
# - [ ] I made a final Git commit.
#
# If something still fails, leave a Markdown note with the exact failure, what you tried, and your next diagnostic step. Honest visible evidence receives substantial credit.

# %% [markdown]
# From the terminal at the repository root, inspect before committing:
#
# ```bash
# git status
# git diff
# git add notebooks/10_final_analysis.ipynb
# git diff --cached
# git commit -m "Complete small climate-data analysis"
# ```
#
# Follow the instructor's written submission route. Do not push student work directly into the shared upstream course repository.

# %% [markdown]
# ## Continuation lane—only after the core is complete
#
# Add one small robustness check: alternate season/window, mean versus median, levels versus changes, alternate coverage threshold, daily versus grouped resampling, or another physically motivated view. Report whether the main conclusion changes. Extensions do not earn more base credit than a well-executed small prompt.
