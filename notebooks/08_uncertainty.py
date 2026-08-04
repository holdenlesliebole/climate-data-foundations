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
# # From variability to uncertainty
#
# This second half of Thursday's application session estimates the mean June–August Pier surface-minus-bottom temperature difference. You will distinguish daily spread from uncertainty in the estimated mean, make one summer summary per year, and bootstrap years as the resampling units.
#
# **Minimum viable takeaway:** an uncertainty interval is inseparable from the statistic, target, resampling unit, and assumptions that produced it.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - distinguish the standard deviation of daily values from the standard error of an estimated mean;
# - aggregate daily paired differences into one summer mean per year;
# - calculate and plot a reproducible percentile bootstrap interval; and
# - compare daily-iid and year-resampling results as an assumption sensitivity check.

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
from climate_course.statistics import bootstrap_mean_interval

# %% [markdown]
# ## 1. Recreate the checked paired dataset
#
# This notebook intentionally reloads from the preserved raw file rather than relying on hidden state from notebook 07. The selection must be reproducible after a fresh kernel restart.

# %%
temperature_files = sorted(
    (PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv")
)
assert temperature_files, "Acquire/extract the Pier temperature CSV first."
temperature_path = temperature_files[-1]
pier = load_pier_temperature(temperature_path)

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

summer = paired.loc[paired.month.isin([6, 7, 8])].copy()
assert summer.year.nunique() >= 5, "Too few summers remain; ask the instructor before changing scope."
print("Raw source:", temperature_path.relative_to(PROJECT_ROOT))
print(f"June–August target period: {first_year}–{last_complete_year}")
print("Daily paired rows:", len(summer))
print("Summers represented:", summer.year.nunique())

# %% [markdown]
# Before calculating:
#
# - **Target quantity:** TODO
# - **One daily observation $x_i$:** TODO
# - **Why adjacent daily values may be dependent:** TODO
# - **Proposed resampling unit:** TODO

# %% [markdown]
# ## 2. Observation spread and an iid standard error
#
# Under an independent, identically distributed model, the standard error of a mean is $s/\sqrt{n}$. We calculate it to map Mark's notation into code—not to declare the daily rows independent.

# %%
daily_values = summer.surface_minus_bottom_c.to_numpy()
n_daily = daily_values.size
daily_mean_c = daily_values.mean()
daily_sd_c = daily_values.std(ddof=1)
daily_iid_se_c = daily_sd_c / np.sqrt(n_daily)

daily_summary = pd.Series(
    {
        "n daily paired observations": n_daily,
        "mean difference (°C)": daily_mean_c,
        "daily standard deviation (°C)": daily_sd_c,
        "iid standard error of mean (°C)": daily_iid_se_c,
    }
)
display(daily_summary)

# %% [markdown]
# Finish both sentences:
#
# - The standard deviation describes **TODO**.
# - The iid standard error would describe **TODO**, if **TODO**.

# %% [markdown]
# ## 3. Make one summer summary per year
#
# Grouping keeps most within-summer daily persistence inside a year. Each resampled value below is a summer mean, not a daily row.

# %%
annual = (
    summer.groupby("year", as_index=False)
    .agg(
        mean_difference_c=("surface_minus_bottom_c", "mean"),
        median_difference_c=("surface_minus_bottom_c", "median"),
        daily_sd_c=("surface_minus_bottom_c", "std"),
        n_days=("surface_minus_bottom_c", "size"),
    )
)
display(annual)

assert annual.year.nunique() == annual.shape[0]
assert annual.n_days.min() > 0

fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(annual.year, annual.mean_difference_c, marker="o")
ax.axhline(annual.mean_difference_c.mean(), color="0.25", ls="--", label="Mean across summers")
ax.set(
    title="One June–August surface-minus-bottom mean per year",
    xlabel="Year",
    ylabel="Annual summer mean difference (°C)",
)
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# **Explain:** What information did grouping retain? What daily information did it discard? Why can that tradeoff be useful for an introductory uncertainty estimate? **TODO**

# %% [markdown]
# ## 4. Bootstrap the annual summer means
#
# Open `src/climate_course/statistics.py` and identify the line that samples with replacement, the line that calculates a mean, and the lines that take interval endpoints. The function rejects missing values so the caller's missing-data policy stays visible.

# %%
annual_means = annual.mean_difference_c.to_numpy()
year_interval = bootstrap_mean_interval(
    annual_means,
    confidence=0.95,
    n_resamples=5_000,
    seed=2026,
)
display(pd.Series(year_interval, name="year-resampling bootstrap"))

assert year_interval["lower"] <= year_interval["estimate"] <= year_interval["upper"]
assert year_interval["n_units"] == len(annual_means)

# %% [markdown]
# Map the result to language:
#
# - **Estimate:** TODO (number, quantity, units)
# - **Interval:** TODO (endpoints, confidence level, method)
# - **Resampling unit:** TODO
# - **Exchangeability/representativeness assumption:** TODO
# - **Important limitation not repaired by the interval:** TODO

# %% [markdown]
# ## 5. Sensitivity to the resampling unit
#
# For comparison only, bootstrap individual daily differences as if they were exchangeable iid units. The daily and year analyses also weight years differently when days are missing, so both the interval width and estimate may change.

# %%
daily_interval = bootstrap_mean_interval(
    daily_values,
    confidence=0.95,
    n_resamples=3_000,
    seed=2026,
)

intervals = pd.DataFrame(
    [
        {"method": "resample daily rows", **daily_interval},
        {"method": "resample summer/year means", **year_interval},
    ]
)
display(intervals[["method", "estimate", "lower", "upper", "n_units"]])

fig, ax = plt.subplots(figsize=(8, 3.6))
positions = np.arange(len(intervals))
lower_error = intervals.estimate - intervals.lower
upper_error = intervals.upper - intervals.estimate
ax.errorbar(
    positions,
    intervals.estimate,
    yerr=np.vstack([lower_error, upper_error]),
    fmt="o",
    capsize=5,
)
ax.axhline(0, color="0.4", lw=0.8)
ax.set(
    xticks=positions,
    xticklabels=intervals.method,
    ylabel="Mean surface-minus-bottom difference (°C)",
    title="Interval sensitivity to the resampling unit",
)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()

# %% [markdown]
# **Interpret the comparison:** Which interval is narrower? Why is “narrower” not enough to choose a method? What feature of daily climate/ocean data makes the iid-day model questionable? **TODO**

# %% [markdown]
# ## Core product: three-sentence uncertainty statement
#
# 1. Report the year-level estimate and interval with units. **TODO**
# 2. State that summers/years were resampled and what exchangeability assumption that represents. **TODO**
# 3. State one limitation and what the daily-versus-year sensitivity comparison showed. **TODO**

# %% [markdown]
# ## Exit ticket
#
# Complete: “My estimate is ___; I resampled ___; this treats ___ as exchangeable; and the interval does not address ___.”
#
# **Answer:** TODO

# %% [markdown]
# ## Continuation lane: moving blocks of daily values
#
# A moving-block bootstrap resamples short consecutive runs instead of isolated days. Compare 7-day and 30-day blocks with the year-level interval. Block length is another modeling choice; this activity is a sensitivity check, not an automatic correction.

# %%
def moving_block_mean_interval(values, block_length, n_resamples=2_000, seed=2026):
    values = np.asarray(values, dtype=float)
    if not 1 <= block_length <= len(values):
        raise ValueError("block_length must fit inside the series")
    blocks = [values[start : start + block_length] for start in range(len(values) - block_length + 1)]
    blocks_needed = int(np.ceil(len(values) / block_length))
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_resamples):
        chosen = rng.integers(0, len(blocks), size=blocks_needed)
        resample = np.concatenate([blocks[index] for index in chosen])[: len(values)]
        means.append(resample.mean())
    lower, upper = np.quantile(means, [0.025, 0.975])
    return {"estimate": float(values.mean()), "lower": float(lower), "upper": float(upper)}


for block_days in [7, 30]:
    print(block_days, moving_block_mean_interval(daily_values, block_days))

# %% [markdown]
# Report how interval width changes with block length and why resampling across seasonal/year boundaries is still an approximation. Compare mean versus median annual summaries as a second robustness check if time permits.
