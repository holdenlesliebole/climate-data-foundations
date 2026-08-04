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
# # Reference: from variability to uncertainty
#
# This completed reference estimates a mean June–August Pier surface-minus-bottom difference by resampling one summer mean per year. Values update with the provider archive.

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
from climate_course.statistics import bootstrap_mean_interval

# %%
files = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
assert files, "Acquire/extract the original Pier temperature CSV first."
path = files[-1]
pier = load_pier_temperature(path)
latest_year = int(pier.date.dt.year.max())
last_complete_year = latest_year - 1
first_year = last_complete_year - 9
paired = surface_bottom_difference(
    pier, f"{first_year}-01-01", f"{last_complete_year}-12-31", good_only=True
)
paired["year"] = paired.date.dt.year
paired["month"] = paired.date.dt.month
summer = paired.loc[paired.month.isin([6, 7, 8])].copy()
assert summer.year.nunique() >= 5
print(path.name, first_year, last_complete_year, len(summer), summer.year.nunique())

# %% [markdown]
# The target is the average June–August surface-minus-near-bottom difference across the selected recent summers. One raw analysis observation is a good-flag paired daily difference. Adjacent days can share persistent ocean conditions, so they are not assumed to be independent evidence in the primary interval.

# %%
daily_values = summer.surface_minus_bottom_c.to_numpy()
daily_summary = pd.Series(
    {
        "n daily values": len(daily_values),
        "mean difference (°C)": daily_values.mean(),
        "daily standard deviation (°C)": daily_values.std(ddof=1),
        "iid standard error (°C)": daily_values.std(ddof=1) / np.sqrt(len(daily_values)),
    }
)
display(daily_summary)

# %% [markdown]
# The daily standard deviation describes variation among selected daily differences. The iid standard error estimates repeated-sample variation of the daily mean only under an exchangeable independent-day model, which is questionable for a smooth ocean time series.

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

fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(annual.year, annual.mean_difference_c, marker="o")
ax.axhline(annual.mean_difference_c.mean(), color="0.25", ls="--", label="Mean across summers")
ax.set(title="One June–August mean per year", xlabel="Year", ylabel="Surface-minus-bottom difference (°C)")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# Annual grouping retains between-summer variation and each year's average but discards within-summer timing and extremes. It is useful here because a whole summer/year is the stated primary resampling unit, keeping much short-term dependence together.

# %%
year_interval = bootstrap_mean_interval(
    annual.mean_difference_c.to_numpy(), confidence=0.95, n_resamples=5_000, seed=2026
)
daily_interval = bootstrap_mean_interval(
    daily_values, confidence=0.95, n_resamples=3_000, seed=2026
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
ax.errorbar(
    positions,
    intervals.estimate,
    yerr=np.vstack([intervals.estimate - intervals.lower, intervals.upper - intervals.estimate]),
    fmt="o",
    capsize=5,
)
ax.axhline(0, color="0.4", lw=0.8)
ax.set(xticks=positions, xticklabels=intervals.method, ylabel="Mean difference (°C)", title="Sensitivity to resampling unit")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()

# %%
print(
    f"Across {year_interval['n_units']} selected summers, the mean annual June–August "
    f"surface-minus-bottom difference was {year_interval['estimate']:.2f} °C; the 95% "
    f"percentile bootstrap interval was [{year_interval['lower']:.2f}, "
    f"{year_interval['upper']:.2f}] °C."
)

# %% [markdown]
# **Bounded interpretation:** The interval resamples the selected summer/year means and treats those years as exchangeable representatives of the stated recent-summer target. The comparison with iid daily resampling exposes sensitivity to the observational-unit assumption; a narrower daily interval is not automatically more defensible because adjacent days are persistent and years may have different numbers of usable days. Neither interval addresses sensor/method bias, nonrandom missingness, choice of recent period, representativeness beyond these years, or physical cause.

# %% [markdown]
# **Exit ticket:** My estimate is the mean of the selected annual June–August surface-minus-bottom means; I resampled summers/years; this treats the selected years as exchangeable under the bootstrap model; and the interval does not address bias, missingness mechanisms, or generalization outside the selected recent period.

# %% [markdown]
# A moving-block daily bootstrap can preserve short runs, and mean-versus-median annual summaries can test robustness. Block length and boundaries remain modeling choices; report how they change the conclusion rather than presenting them as automatic corrections.
