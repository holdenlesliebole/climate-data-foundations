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
# # Pier SST and global temperature: relationships, trends, and bounded claims
#
# Friday's application connects the Pier surface-temperature record you acquired Monday with NASA's annual global temperature anomaly. You will preserve and inspect both provider files, construct one row per year, plot the time series before calculating a relationship, interpret a fitted slope, inspect residuals, and ask how much of the correlation reflects shared low-frequency change.
#
# **Minimum viable takeaway:** a correlation between two climate time series is a description of the selected years—not proof of causation, independence, or a stable local response to global change.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - acquire, preserve, and inspect a second public climate dataset;
# - create annual means under an explicit coverage and quality rule;
# - merge two annual series by year and verify the matched sample;
# - calculate and interpret correlation and a least-squares slope with units;
# - inspect residual and time structure; and
# - compare relationships in annual levels and year-to-year changes.

# %%
from pathlib import Path
import sys
from urllib.request import urlretrieve

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

from climate_course.climate_series import (
    annual_mlo_co2,
    annual_pier_surface,
    load_gistemp_annual,
    load_scripps_mlo_monthly,
)
from climate_course.pier import load_pier_temperature

# %% [markdown]
# ## 1. Acquire the NASA global temperature table
#
# Open the [NASA GISTEMP v4 data-download page](https://data.giss.nasa.gov/gistemp/data_v4.html) and locate the CSV for **global-mean monthly, seasonal, and annual Land–Ocean Temperature Index values**. Confirm that it reports anomalies relative to 1951–1980.
#
# The cell below makes the network request visible and saves the exact response before analysis. If the provider is unavailable, use the documented recovery copy and record that route in your manifest. Do not repeatedly analyze a live URL.

# %%
GISTEMP_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts%2BdSST.csv"
CLIMATE_RAW = PROJECT_ROOT / "data" / "raw" / "climate"
CLIMATE_RAW.mkdir(parents=True, exist_ok=True)
gistemp_path = CLIMATE_RAW / "NASA_GISTEMP_global.csv"

if gistemp_path.exists():
    print("Reusing preserved response:", gistemp_path.relative_to(PROJECT_ROOT))
else:
    urlretrieve(GISTEMP_URL, gistemp_path)
    print("Downloaded:", gistemp_path.relative_to(PROJECT_ROOT))

print("Bytes:", gistemp_path.stat().st_size)
print("Source URL:", GISTEMP_URL)

# %% [markdown]
# Record the source URL, access date, local filename, provider, anomaly baseline, and acquisition method in `data/manifest.yml` before continuing.

# %% [markdown]
# ## 2. Inspect both raw sources before loading
#
# A CSV can contain scientific context outside its rectangular table. Compare the first lines of NASA's file with the preamble/header discovery you used for the Pier archive.

# %%
for line_number, line in enumerate(
    gistemp_path.read_text(encoding="utf-8-sig").splitlines()[:6], start=1
):
    print(f"{line_number:>2}: {line}")

# %%
temperature_files = sorted(
    (PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv")
)
assert temperature_files, "Acquire and extract the Pier temperature CSV first."
temperature_path = temperature_files[-1]

pier = load_pier_temperature(temperature_path)
gistemp = load_gistemp_annual(gistemp_path)

print("Pier source:", temperature_path.relative_to(PROJECT_ROOT))
print("Pier coverage:", pier.date.min().date(), "to", pier.date.max().date())
print("GISTEMP source:", gistemp_path.relative_to(PROJECT_ROOT))
print("GISTEMP coverage:", gistemp.year.min(), "to", gistemp.year.max())
display(gistemp.head())

# %% [markdown]
# Before calculating, answer:
#
# - What does one raw Pier row represent? **TODO**
# - What does one GISTEMP `J-D` value represent, and what is its baseline? **TODO**
# - Why is global temperature an anomaly while Pier SST remains an absolute temperature? **TODO**
# - Which source can be revised after you download it? What should your manifest preserve? **TODO**

# %% [markdown]
# ## 3. Construct annual Pier SST under a visible rule
#
# Use surface observations with the provider's good flag (`SURF_FLAG == 0`). If a date has multiple good rows, average that date first. Keep a year only when it has at least 180 observed days. This half-year threshold is a transparent teaching choice, not a universal definition of completeness.

# %%
MIN_PIER_DAYS = 180
annual_pier = annual_pier_surface(pier, min_days=MIN_PIER_DAYS)
display(annual_pier.tail())

fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(annual_pier.year, annual_pier.n_pier_days, marker=".", lw=1)
ax.axhline(MIN_PIER_DAYS, color="C3", ls="--", label="Inclusion threshold")
ax.set(
    title="Pier surface-temperature coverage by year",
    xlabel="Year",
    ylabel="Good observed days",
)
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# **Coverage decision:** Why might sparse years receive disproportionate seasonal weighting? Name one alternative threshold or seasonal adjustment you could test. **TODO**

# %% [markdown]
# ## 4. Merge by year and inspect the matched sample
#
# An inner merge keeps only years represented in both annual tables. `validate="one_to_one"` makes the intended unit—one Pier mean and one global anomaly per year—executable.

# %%
analysis = (
    annual_pier.merge(gistemp, on="year", how="inner", validate="one_to_one")
    .sort_values("year")
    .reset_index(drop=True)
)
assert len(analysis) >= 20, "Too few overlapping annual values; inspect coverage before changing rules."
assert analysis[["pier_mean_sst_c", "global_temp_anomaly_c"]].notna().all().all()

print("Matched years:", analysis.year.min(), "to", analysis.year.max())
print("Matched annual pairs:", len(analysis))
print("Missing calendar years inside span:", int(analysis.year.diff().gt(1).sum()))
display(analysis.head())

# %% [markdown]
# **Selection statement:** TODO—name both providers/files, the overlapping years, the Pier flag and coverage rules, NASA's anomaly baseline, and one limitation.

# %% [markdown]
# ## 5. Plot the time series before the scatterplot
#
# Separate panels avoid a dual-axis plot whose visual relationship can change when either axis is rescaled. Identify trends, unusual years, gaps, and multi-year structure before reducing the pair to one coefficient.

# %%
fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
axes[0].plot(analysis.year, analysis.pier_mean_sst_c, marker="o", ms=3, lw=1)
axes[0].set(ylabel="Annual mean Pier SST (°C)", title="Matched annual climate series")
axes[1].plot(
    analysis.year,
    analysis.global_temp_anomaly_c,
    marker="o",
    ms=3,
    lw=1,
    color="C1",
)
axes[1].set(xlabel="Year", ylabel="Global anomaly (°C vs 1951–1980)")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# Describe one shared low-frequency feature and one local feature that the global series does not explain. Why should a shared trend make you cautious about interpreting a scatterplot? **TODO**

# %% [markdown]
# ## 6. Correlation and a least-squares line
#
# Let $x$ be NASA global temperature anomaly in °C and $y$ be annual Pier SST in °C. The fitted slope therefore has units of **local °C per global-anomaly °C**. It is an association across the selected annual pairs, not a controlled climate sensitivity.

# %%
x = analysis.global_temp_anomaly_c.to_numpy()
y = analysis.pier_mean_sst_c.to_numpy()

correlation = float(np.corrcoef(x, y)[0, 1])
slope_local_per_global, intercept_c = np.polyfit(x, y, deg=1)
analysis["fitted_pier_sst_c"] = intercept_c + slope_local_per_global * x
analysis["residual_c"] = y - analysis.fitted_pier_sst_c

print(f"Pearson correlation r = {correlation:.3f}")
print(f"Slope = {slope_local_per_global:.3f} local °C per global-anomaly °C")
print(f"Intercept at a 0 °C global anomaly = {intercept_c:.3f} °C")

# %%
order = np.argsort(x)
fig, ax = plt.subplots(figsize=(7.5, 4.8))
points = ax.scatter(
    x,
    y,
    c=analysis.year,
    cmap="viridis",
    s=35,
    alpha=0.8,
    label="Annual pair",
)
ax.plot(x[order], analysis.fitted_pier_sst_c.to_numpy()[order], color="C3", lw=2)
ax.set(
    title="Annual Pier SST versus global temperature anomaly",
    xlabel="NASA global temperature anomaly (°C vs 1951–1980)",
    ylabel="Pier annual mean surface SST (°C)",
)
ax.grid(alpha=0.25)
fig.colorbar(points, ax=ax, label="Year")
fig.tight_layout()

# %% [markdown]
# Complete:
#
# - A 1 °C higher global anomaly is associated with **TODO** °C higher/lower fitted annual Pier SST across these years.
# - The color progression reveals **TODO** about time.
# - The intercept **is/is not** interpretable here because **TODO**.
# - This slope is not automatically a causal or transferable local climate sensitivity because **TODO**.

# %% [markdown]
# ## 7. Inspect what the line missed
#
# A residual is observed minus fitted: $e_i=y_i-\hat{y}_i$. Positive residuals are years when Pier SST was warmer than the fitted value associated with that year's global anomaly.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].scatter(analysis.fitted_pier_sst_c, analysis.residual_c, c=analysis.year, cmap="viridis")
axes[0].axhline(0, color="0.25", lw=0.8)
axes[0].set(
    title="Residuals versus fitted Pier SST",
    xlabel="Fitted Pier SST (°C)",
    ylabel="Residual (°C)",
)
axes[1].plot(analysis.year, analysis.residual_c, marker="o", ms=3, lw=1)
axes[1].axhline(0, color="0.25", lw=0.8)
axes[1].set(title="Residuals in time order", xlabel="Year", ylabel="Residual (°C)")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()

lag1_residual_correlation = float(analysis.residual_c.autocorr(lag=1))
print(f"Lag-one residual correlation = {lag1_residual_correlation:.3f}")

# %% [markdown]
# Identify one residual pattern or absence of pattern. What local processes, sampling changes, or climate modes might remain in the residuals? What does lag-one correlation suggest about treating annual rows as independent? **TODO**

# %% [markdown]
# ## 8. Sensitivity: annual levels versus year-to-year changes
#
# Two upward-trending series can have a high correlation even when their short-term co-variation is weak. First differences compare the change from one year to the next and remove much of a smooth shared trend. This is a diagnostic sensitivity check—not a complete causal model or a guarantee of independence.

# %%
analysis["year_gap"] = analysis.year.diff()
analysis["pier_sst_change_c"] = analysis.pier_mean_sst_c.diff()
analysis["global_temp_change_c"] = analysis.global_temp_anomaly_c.diff()
changes = analysis.loc[
    analysis.year_gap.eq(1),
    ["year", "pier_sst_change_c", "global_temp_change_c"],
].copy()
assert len(changes) >= 10, "Too few consecutive-year pairs for the sensitivity check."

change_correlation = float(changes.pier_sst_change_c.corr(changes.global_temp_change_c))
change_slope, change_intercept = np.polyfit(
    changes.global_temp_change_c,
    changes.pier_sst_change_c,
    deg=1,
)

display(
    pd.DataFrame(
        {
            "n pairs": [len(analysis), len(changes)],
            "correlation": [correlation, change_correlation],
            "slope": [slope_local_per_global, change_slope],
        },
        index=["annual levels", "year-to-year changes"],
    )
)

# %%
fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.scatter(changes.global_temp_change_c, changes.pier_sst_change_c, alpha=0.75)
change_x = np.linspace(changes.global_temp_change_c.min(), changes.global_temp_change_c.max(), 100)
ax.plot(change_x, change_intercept + change_slope * change_x, color="C3", lw=2)
ax.axhline(0, color="0.4", lw=0.7)
ax.axvline(0, color="0.4", lw=0.7)
ax.set(
    title="Sensitivity: changes from the previous year",
    xlabel="Change in global temperature anomaly (°C/year)",
    ylabel="Change in Pier annual mean SST (°C/year)",
)
ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# Compare the sign and magnitude of the two correlations. What does the comparison suggest about shared trend? Why would neither result alone establish that global mean temperature directly determines Pier SST? **TODO**

# %% [markdown]
# ## Core product: bounded relationship statement
#
# Write four to six sentences that include:
#
# 1. both sources, the matched years, and the Pier completeness rule;
# 2. the annual-level correlation and slope with units;
# 3. one residual or time-dependence finding;
# 4. the levels-versus-changes sensitivity result; and
# 5. one causal, attribution, prediction, or generalization claim the analysis cannot support.
#
# **Interpretation:** TODO

# %% [markdown]
# ## Exit ticket
#
# Why can two trending climate records have a high correlation even if their year-to-year changes are only weakly related? Name one additional analysis or source of evidence you would want before making a causal claim.
#
# **Answer:** TODO

# %% [markdown]
# ## Continuation lane: Pier SST and the Keeling Curve
#
# Download the official Scripps monthly in-situ Mauna Loa CO₂ record, inspect its preamble and three-row header, and make annual means from **measured** monthly `CO2` values. The loader treats the provider's `-99.99` sentinel as missing; require at least eight measured months per year.
#
# Atmospheric CO₂ is a well-established climate forcing, but a bivariate regression of local annual SST on contemporaneous Mauna Loa concentration is not an attribution model. Both series trend through time, local SST has many other controls, and the climate response is not an instantaneous one-predictor process.

# %%
MLO_URL = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"
mlo_path = CLIMATE_RAW / "Scripps_MLO_monthly_in_situ_CO2.csv"

if mlo_path.exists():
    print("Reusing preserved response:", mlo_path.relative_to(PROJECT_ROOT))
else:
    urlretrieve(MLO_URL, mlo_path)
    print("Downloaded:", mlo_path.relative_to(PROJECT_ROOT))

mlo_lines = mlo_path.read_text(encoding="utf-8-sig").splitlines()
mlo_header_matches = [
    index for index, line in enumerate(mlo_lines) if line.lstrip().startswith("Yr, Mn,")
]
assert len(mlo_header_matches) == 1, mlo_header_matches
mlo_header_index = mlo_header_matches[0]
print("Header begins on human-readable line:", mlo_header_index + 1)
for line in mlo_lines[max(0, mlo_header_index - 2) : mlo_header_index + 4]:
    print(line)

# %%
mlo_monthly = load_scripps_mlo_monthly(mlo_path)
annual_co2 = annual_mlo_co2(mlo_monthly, min_months=8)
co2_analysis = analysis[["year", "pier_mean_sst_c"]].merge(
    annual_co2,
    on="year",
    how="inner",
    validate="one_to_one",
)

co2_levels_r = float(co2_analysis.pier_mean_sst_c.corr(co2_analysis.mlo_co2_ppm))
co2_analysis["year_gap"] = co2_analysis.year.diff()
co2_analysis["pier_change_c"] = co2_analysis.pier_mean_sst_c.diff()
co2_analysis["co2_change_ppm"] = co2_analysis.mlo_co2_ppm.diff()
co2_changes = co2_analysis.loc[co2_analysis.year_gap.eq(1)].dropna().copy()
co2_changes_r = float(co2_changes.pier_change_c.corr(co2_changes.co2_change_ppm))

print("Matched CO2 years:", co2_analysis.year.min(), "to", co2_analysis.year.max())
print(f"Correlation in annual levels: {co2_levels_r:.3f}")
print(f"Correlation in year-to-year changes: {co2_changes_r:.3f}")

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].scatter(co2_analysis.mlo_co2_ppm, co2_analysis.pier_mean_sst_c, c=co2_analysis.year, cmap="plasma")
axes[0].set(xlabel="Annual mean Mauna Loa CO₂ (ppm)", ylabel="Pier annual mean SST (°C)", title="Annual levels")
axes[1].scatter(co2_changes.co2_change_ppm, co2_changes.pier_change_c, c=co2_changes.year, cmap="plasma")
axes[1].axhline(0, color="0.4", lw=0.7)
axes[1].set(xlabel="Annual CO₂ change (ppm/year)", ylabel="Annual Pier SST change (°C/year)", title="Year-to-year changes")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# **Continuation interpretation:** Compare the two correlations and plots. Explain why the annual-level association can be strong, why differencing changes the question, and why neither coefficient should be labeled “the effect of CO₂ on Scripps Pier temperature.” Record the Scripps source URL, access date, local file, observed-versus-filled choice, and citation/license information. **TODO**
