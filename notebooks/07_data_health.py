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
# # Pier data health before statistics
#
# A statistical result is only as interpretable as the observations that entered it. In this first half of Thursday's application session, you will reopen the original Pier temperature file, describe its coverage and missingness, make a paired surface–bottom dataset, and distinguish an unusual observation from an obvious generated error.
#
# **Minimum viable takeaway:** before calculating a statistic, state what one row represents, which rows are usable, what was excluded, and what evidence supports each choice.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - produce a compact data-health table with source, coverage, duplicates, missingness, and flags;
# - create paired surface/bottom observations under an explicit quality rule;
# - compare center, spread, shape, and time behavior with units; and
# - investigate an extreme value without silently deleting or editing raw data.

# %%
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists(), "Open the course project folder first."

SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.pier import load_pier_temperature, surface_bottom_difference

# %% [markdown]
# ## 1. Predict before loading
#
# Write an answer before running the next cell.
#
# - What does one provider row represent? **TODO**
# - Which columns contain values, units, and evidence about quality? **TODO**
# - Which will be more common: missing surface values or missing bottom values? Why? **TODO**
# - Is one daily row necessarily independent of the next? **TODO**

# %%
temperature_files = sorted(
    (PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv")
)
assert temperature_files, (
    "No Pier temperature CSV found. Revisit Monday's acquisition or use the documented "
    "instructor recovery checkpoint."
)
temperature_path = temperature_files[-1]
pier = load_pier_temperature(temperature_path)

print("Source file:", temperature_path.relative_to(PROJECT_ROOT))
print("Shape:", pier.shape)
print("Coverage:", pier.date.min(), "to", pier.date.max())
display(pier.head())

# %% [markdown]
# Check your prediction against the provider preamble and the loaded columns. A row contains a calendar-date record; time of collection is available only for part of the archive. Surface and near-bottom values are separate measurements, and their flags are evidence—not values to average.

# %% [markdown]
# ## 2. Build a compact data-health table
#
# A health report does not pronounce the dataset “good” or “bad.” It makes consequential features visible before analysis.

# %%
health_report = pd.DataFrame(
    {
        "value": [
            temperature_path.name,
            len(pier),
            pier.date.min().date(),
            pier.date.max().date(),
            int(pier.date.duplicated().sum()),
            float(pier.SURF_TEMP_C.isna().mean()),
            float(pier.BOT_TEMP_C.isna().mean()),
            float(pier.SURF_FLAG.ne(0).mean()),
            float(pier.BOT_FLAG.ne(0).mean()),
        ]
    },
    index=[
        "local raw file",
        "rows",
        "first date",
        "last date",
        "duplicate dates",
        "surface missing fraction",
        "bottom missing fraction",
        "surface flag not 0 fraction",
        "bottom flag not 0 fraction",
    ],
)
display(health_report)

print("Surface flag counts")
display(pier.SURF_FLAG.value_counts(dropna=False).sort_index())
print("Bottom flag counts")
display(pier.BOT_FLAG.value_counts(dropna=False).sort_index())

# %% [markdown]
# **Explain:** Which health-report feature matters most for a surface–bottom comparison? Which feature needs provider documentation before you can act on it? **TODO**

# %% [markdown]
# ## 3. Make the analysis target and quality rule visible
#
# To keep today's computation bounded, use the ten most recent complete calendar years in the archive. `good_only=True` requires provider flag `0` at both depths and the helper drops rows lacking either temperature because their difference is undefined.

# %%
latest_observed_year = int(pier.date.dt.year.max())
last_complete_year = latest_observed_year - 1
first_year = last_complete_year - 9

paired = surface_bottom_difference(
    pier,
    f"{first_year}-01-01",
    f"{last_complete_year}-12-31",
    good_only=True,
)
paired["year"] = paired.date.dt.year
paired["month"] = paired.date.dt.month

assert paired.date.between(f"{first_year}-01-01", f"{last_complete_year}-12-31").all()
assert paired[["SURF_TEMP_C", "BOT_TEMP_C"]].notna().all().all()
assert paired[["SURF_FLAG", "BOT_FLAG"]].eq(0).all().all()

print(f"Target period: {first_year}–{last_complete_year}")
print("Usable paired rows:", len(paired))
print("Years represented:", paired.year.nunique())

# %% [markdown]
# Complete the chain in words:
#
# - **Scientific target for this exercise:** TODO
# - **One observation:** TODO
# - **Quality rule:** TODO
# - **Missing-pair rule:** TODO
# - **One limitation of this selection:** TODO

# %% [markdown]
# ## 4. Compare distributions and calculate descriptive summaries

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

# %%
all_temperatures = pd.concat([paired.SURF_TEMP_C, paired.BOT_TEMP_C])
temperature_bins = np.linspace(all_temperatures.min(), all_temperatures.max(), 30)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(
    paired.SURF_TEMP_C,
    bins=temperature_bins,
    alpha=0.65,
    label="Surface",
)
axes[0].hist(
    paired.BOT_TEMP_C,
    bins=temperature_bins,
    alpha=0.65,
    label="Near-bottom",
)
axes[0].set(
    title=f"Pier temperature distributions, {first_year}–{last_complete_year}",
    xlabel="Temperature (°C)",
    ylabel="Daily paired observations",
)
axes[0].legend()

axes[1].plot(paired.date, paired.surface_minus_bottom_c, lw=0.7)
axes[1].axhline(0, color="0.25", lw=0.8)
axes[1].set(
    title="Surface minus near-bottom temperature",
    xlabel="Date",
    ylabel="Temperature difference (°C)",
)
for ax in axes:
    ax.grid(alpha=0.2)
fig.tight_layout()

# %% [markdown]
# **Explain the evidence:**
#
# - Compare surface and bottom center and spread, with units. **TODO**
# - Describe one feature visible in the distribution plot and one visible only in time order. **TODO**
# - Why is variance not the easiest spread measure to report beside temperatures? **TODO**

# %% [markdown]
# ## 5. Extreme does not automatically mean erroneous
#
# Find the paired difference farthest from the median. The value may be scientifically real, affected by a method/flag issue not captured by the current rule, or an error. Its extremeness alone does not decide.

# %%
median_difference = paired.surface_minus_bottom_c.median()
extreme_index = (paired.surface_minus_bottom_c - median_difference).abs().idxmax()
extreme_row = paired.loc[
    extreme_index,
    ["date", "SURF_TEMP_C", "BOT_TEMP_C", "SURF_FLAG", "BOT_FLAG", "surface_minus_bottom_c"],
]
display(extreme_row.to_frame("most extreme paired difference"))

# %% [markdown]
# Before excluding anything, list two checks using date context, nearby observations, provider flags/preamble, or known methods. **TODO**
#
# Now compare that real row with a generated teaching error. This copy exists only in memory; raw data remain untouched.

# %%
teaching_copy = paired.head(14).copy()
injected_index = teaching_copy.index[7]
teaching_copy.loc[injected_index, "SURF_TEMP_C"] = 180.0
teaching_copy.loc[injected_index, "surface_minus_bottom_c"] = (
    teaching_copy.loc[injected_index, "SURF_TEMP_C"]
    - teaching_copy.loc[injected_index, "BOT_TEMP_C"]
)
display(teaching_copy.loc[[injected_index]])

# %% [markdown]
# A 180 °C surface measurement conflicts with physical range, nearby values, and the provider variable meaning. The response is to trace and correct/reacquire the generated derivative—not to edit an untouched provider file in place. Write the evidence that distinguishes this case from “largest valid observed difference.” **TODO**

# %% [markdown]
# ## Core product: one-page data health statement
#
# Complete four short parts:
#
# 1. **Source/coverage:** provider file and selected years — TODO
# 2. **Observation and quality policy:** one row, pairing, flags, missing values — TODO
# 3. **Distribution/time evidence:** center, spread, shape, and one time feature — TODO
# 4. **Limitation/next check:** one concern the health report cannot resolve — TODO

# %% [markdown]
# ## Exit ticket
#
# Name one reason to retain and investigate an unusual value and one piece of evidence that would justify excluding or correcting a value.
#
# **Answer:** TODO

# %% [markdown]
# ## Continuation lane
#
# Repeat the paired selection with `good_only=False`. Compare the number of rows, flag categories, descriptive results, and plots. Do **not** conclude that more rows are automatically better. Report which result changes, which evidence explains the change, and which quality policy you would defend for your stated question.
