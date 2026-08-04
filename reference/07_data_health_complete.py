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
# # Reference: Pier data health before statistics
#
# This completed reference shows the reasoning expected from the guided data-health notebook. Numerical values update with the acquired provider archive, so the code prints them instead of embedding a dated result in prose.

# %%
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from climate_course.pier import load_pier_temperature, surface_bottom_difference

# %%
files = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
assert files, "Acquire/extract the original Pier temperature CSV first."
path = files[-1]
pier = load_pier_temperature(path)

health_report = pd.DataFrame(
    {"value": [
        path.name,
        len(pier),
        pier.date.min().date(),
        pier.date.max().date(),
        int(pier.date.duplicated().sum()),
        float(pier.SURF_TEMP_C.isna().mean()),
        float(pier.BOT_TEMP_C.isna().mean()),
        float(pier.SURF_FLAG.ne(0).mean()),
        float(pier.BOT_FLAG.ne(0).mean()),
    ]},
    index=[
        "local raw file", "rows", "first date", "last date", "duplicate dates",
        "surface missing fraction", "bottom missing fraction",
        "surface flag not 0 fraction", "bottom flag not 0 fraction",
    ],
)
display(health_report)
display(pier.SURF_FLAG.value_counts(dropna=False).sort_index().rename("surface flag count"))
display(pier.BOT_FLAG.value_counts(dropna=False).sort_index().rename("bottom flag count"))

# %% [markdown]
# One row is a calendar-date record, with time-of-collection populated only for part of the archive. Bottom missingness deserves special attention because the bottom series begins later and a paired difference requires both depths. Flag meanings must come from the provider preamble; flag values are not temperatures and are not averaged.

# %%
latest_year = int(pier.date.dt.year.max())
last_complete_year = latest_year - 1
first_year = last_complete_year - 9
paired = surface_bottom_difference(
    pier, f"{first_year}-01-01", f"{last_complete_year}-12-31", good_only=True
)
paired["year"] = paired.date.dt.year
paired["month"] = paired.date.dt.month

assert paired[["SURF_TEMP_C", "BOT_TEMP_C"]].notna().all().all()
assert paired[["SURF_FLAG", "BOT_FLAG"]].eq(0).all().all()
np.testing.assert_allclose(
    paired.surface_minus_bottom_c,
    paired.SURF_TEMP_C - paired.BOT_TEMP_C,
)
print(first_year, last_complete_year, len(paired), paired.year.nunique())

# %%
def iqr(series):
    return float(series.quantile(0.75) - series.quantile(0.25))


descriptive = pd.DataFrame(
    {
        "surface_c": paired.SURF_TEMP_C,
        "bottom_c": paired.BOT_TEMP_C,
        "surface_minus_bottom_c": paired.surface_minus_bottom_c,
    }
).agg(["count", "mean", "median", "std", iqr, "min", "max"])
display(descriptive)

temperature_bins = np.linspace(
    pd.concat([paired.SURF_TEMP_C, paired.BOT_TEMP_C]).min(),
    pd.concat([paired.SURF_TEMP_C, paired.BOT_TEMP_C]).max(),
    30,
)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(paired.SURF_TEMP_C, bins=temperature_bins, alpha=0.65, label="Surface")
axes[0].hist(paired.BOT_TEMP_C, bins=temperature_bins, alpha=0.65, label="Near-bottom")
axes[0].set(title=f"Pier temperatures, {first_year}–{last_complete_year}", xlabel="Temperature (°C)", ylabel="Daily paired observations")
axes[0].legend()
axes[1].plot(paired.date, paired.surface_minus_bottom_c, lw=0.7)
axes[1].axhline(0, color="0.25", lw=0.8)
axes[1].set(title="Surface minus near-bottom temperature", xlabel="Date", ylabel="Difference (°C)")
for ax in axes:
    ax.grid(alpha=0.2)
fig.tight_layout()

# %% [markdown]
# The table reports center and spread in °C; variance would have squared units and is less direct beside the measured temperatures. The histogram reveals distribution overlap/shape, while the time view reveals persistence, seasonality, gaps, and changing behavior that an unordered histogram hides. These are descriptions of the selected good-flag paired records, not proof of independence or representativeness.

# %%
median = paired.surface_minus_bottom_c.median()
extreme_index = (paired.surface_minus_bottom_c - median).abs().idxmax()
display(paired.loc[[extreme_index]])

teaching_copy = paired.head(14).copy()
injected_index = teaching_copy.index[7]
teaching_copy.loc[injected_index, "SURF_TEMP_C"] = 180.0
teaching_copy.loc[injected_index, "surface_minus_bottom_c"] = (
    teaching_copy.loc[injected_index, "SURF_TEMP_C"]
    - teaching_copy.loc[injected_index, "BOT_TEMP_C"]
)
display(teaching_copy.loc[[injected_index]])

# %% [markdown]
# The most extreme provider row should be investigated with nearby dates, both depths, flags, preamble/method notes, and other context before retaining or excluding it. The generated 180 °C value conflicts with the physical variable, neighbors, and plausible range. It should be traced in the generated copy or reacquired—not silently repaired inside raw provider data.

# %% [markdown]
# **Bounded health statement:** This analysis uses the latest ten complete calendar years in the acquired original Pier temperature CSV and defines one observation as a paired surface/near-bottom daily record. It requires provider flag 0 at both depths and excludes missing pairs because their difference is undefined; the report above records the resulting coverage and missing/flag fractions. Distribution and time views should be interpreted together because time ordering reveals dependence and changing structure. Flag-0 selection and a clean calculation do not establish representativeness, independence, freedom from method changes, or physical cause.

# %% [markdown]
# **Exit ticket:** An unusual value can be real evidence of an event or uncommon state, so retain and investigate it when provenance, flags, nearby values, and physical context remain plausible. Exclusion/correction needs specific evidence such as an impossible physical value, documented bad flag, parse/unit error, duplicate, or reproducible acquisition/processing fault.

# %% [markdown]
# ## Continuation result to report
#
# Repeating with `good_only=False` is a sensitivity analysis. Compare counts, flag categories, and the same statistics/axes. A defensible choice follows the provider's flag definitions and the scientific question; the version with more rows is not automatically preferable.
