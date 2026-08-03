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
# # Reference: code you can trust
#
# This reference separates reusable Pier loading/selection logic from the notebook's scientific narrative, demonstrates failure messages, and runs small fixed tests.

# %%
from pathlib import Path
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from climate_course.pier import load_pier_temperature, surface_bottom_difference

# %% [markdown]
# ## Reusable mechanism versus notebook narrative
#
# `src/climate_course/pier.py` owns repeatable mechanisms: discover exactly one header, load expected columns, construct dates, validate inputs, apply an explicit flag policy, require paired values, and calculate surface minus bottom. This notebook owns the period/question, plot, and interpretation. The helper exposes scientific policy through `good_only`; it does not establish that good-flagged observations are independent, unbiased, or representative.

# %%
temperature_files = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
assert temperature_files, "Acquire/extract the Pier archive first."
pier = load_pier_temperature(temperature_files[-1])
paired = surface_bottom_difference(pier, "2025-01-01", "2025-06-30", good_only=True)
print(pier.shape, paired.shape)
display(paired.head())

# %%
assert paired.date.between("2025-01-01", "2025-06-30").all()
assert paired[["SURF_TEMP_C", "BOT_TEMP_C"]].notna().all().all()
assert paired[["SURF_FLAG", "BOT_FLAG"]].eq(0).all().all()
np.testing.assert_allclose(
    paired.surface_minus_bottom_c,
    paired.SURF_TEMP_C - paired.BOT_TEMP_C,
)
print("selection/calculation checks passed")

# %% [markdown]
# ## Failure messages reduce diagnostic distance

# %%
for start, end in [("2025-06-30", "2025-01-01"), ("1900-01-01", "1900-01-02")]:
    try:
        surface_bottom_difference(pier, start, end)
    except ValueError as error:
        print("expected:", error)
    else:
        raise AssertionError("invalid selection should fail")


# %% [markdown]
# A `KeyError: 'SURFACE_TEMP_C'` is first investigated by comparing the requested string with `pier.columns`; the provider column is `SURF_TEMP_C`. Read the traceback's final exception line first, then find the first frame in course code and make the smallest diagnostic example. Reinstalling pandas is unrelated to evidence of a missing key.

# %% [markdown]
# ## A narrow summary function and known values

# %%
def summarize_difference(frame):
    """Return count, mean, and sample standard deviation of surface-minus-bottom °C."""
    column = "surface_minus_bottom_c"
    if column not in frame.columns:
        raise ValueError(f"Missing required column: {column}")
    values = frame[column].dropna()
    if len(values) < 2:
        raise ValueError("At least two differences are required.")
    return {
        "count": int(values.count()),
        "mean_c": float(values.mean()),
        "std_c": float(values.std(ddof=1)),
    }

known = summarize_difference(pd.DataFrame({"surface_minus_bottom_c": [1.0, 2.0, 3.0]}))
assert known["count"] == 3
assert np.isclose(known["mean_c"], 2.0)
assert np.isclose(known["std_c"], 1.0)
print(known, summarize_difference(paired))

# %% [markdown]
# The function explicitly drops missing differences. That is documented behavior, not evidence that missingness is ignorable. A caller should inspect missingness before selecting/summarizing.

# %% [markdown]
# ## Repository tests

# %%
completed = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", "tests/test_pier.py"],
    cwd=PROJECT_ROOT, text=True, capture_output=True,
)
print(completed.stdout, completed.stderr)
assert completed.returncode == 0

# %% [markdown]
# The tests use a tiny generated provider-shaped CSV, so they run without the network or full archive. They catch header/schema/date/missingness/flag/calculation and failure-path regressions. They cannot validate the real observations, all possible future schemas, sampling representativeness, statistical independence, or interpretation.

# %%
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(paired.date, paired.surface_minus_bottom_c, lw=1.2)
ax.axhline(0, color="0.3", lw=0.8)
ax.set(title="Scripps Pier surface minus near-bottom temperature", xlabel="Date", ylabel="Temperature difference (°C)")
ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# For this January–June 2025 selection, the plotted difference uses only paired values with provider flag 0 for both depths. The changing sign/magnitude describes the selected records but does not establish a physical cause; daily sampling, missingness, depth context, and serial dependence remain limitations.
