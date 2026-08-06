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
# # Reference: Pier SST and global climate relationships
#
# This reference acquires NASA GISTEMP and Scripps Mauna Loa CO₂ files, constructs quality-controlled annual Pier surface-temperature means, fits the Pier–global-temperature relationship, inspects residuals, and compares annual levels with year-to-year changes. Numerical results update with the locally acquired Pier archive and current provider responses.

# %%
from pathlib import Path
import sys
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent

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
# The Pier archive is the original provider CSV acquired Monday. NASA GISTEMP reports global Land–Ocean Temperature Index anomalies relative to 1951–1980. Both raw responses are preserved locally before analysis; an access date and URL belong in the manifest because provider files can be revised.

# %%
GISTEMP_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts%2BdSST.csv"
CLIMATE_RAW = PROJECT_ROOT / "data" / "raw" / "climate"
CLIMATE_RAW.mkdir(parents=True, exist_ok=True)
gistemp_path = CLIMATE_RAW / "NASA_GISTEMP_global.csv"
if not gistemp_path.exists():
    urlretrieve(GISTEMP_URL, gistemp_path)

print("GISTEMP source URL:", GISTEMP_URL)
for line_number, line in enumerate(
    gistemp_path.read_text(encoding="utf-8-sig").splitlines()[:4], start=1
):
    print(f"{line_number:>2}: {line}")

temperature_files = sorted(
    (PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv")
)
assert temperature_files, "Acquire/extract the Pier temperature CSV first."
temperature_path = temperature_files[-1]
pier = load_pier_temperature(temperature_path)
gistemp = load_gistemp_annual(gistemp_path)

print("Pier file:", temperature_path.relative_to(PROJECT_ROOT))
print("Pier raw coverage:", pier.date.min().date(), "to", pier.date.max().date())
print("GISTEMP coverage:", gistemp.year.min(), "to", gistemp.year.max())

# %% [markdown]
# One Pier row is a dated local surface/near-bottom sampling record with provider flags. One NASA `J-D` value is a global annual temperature anomaly, not an absolute global temperature. Keeping local SST absolute and global temperature as an anomaly is valid for association/regression as long as the variables and slope units are stated; shifting a predictor by a constant changes the intercept, not the slope or correlation.

# %%
MIN_PIER_DAYS = 180
annual_pier = annual_pier_surface(pier, min_days=MIN_PIER_DAYS)
display(annual_pier.tail())

fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(annual_pier.year, annual_pier.n_pier_days, marker=".", lw=1)
ax.axhline(MIN_PIER_DAYS, color="C3", ls="--", label="Inclusion threshold")
ax.set(title="Pier SST coverage by year", xlabel="Year", ylabel="Good observed days")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# The annual Pier table uses good-flag surface values, averages duplicate good rows within date, then includes years with at least 180 observed dates. This reduces severe seasonal-coverage imbalance but does not make every retained year equally representative. A threshold or month-standardized anomaly sensitivity would be reasonable follow-up work.

# %%
analysis = (
    annual_pier.merge(gistemp, on="year", how="inner", validate="one_to_one")
    .sort_values("year")
    .reset_index(drop=True)
)
assert len(analysis) >= 20
print("matched years", analysis.year.min(), analysis.year.max(), "n=", len(analysis))
print("calendar gaps", int(analysis.year.diff().gt(1).sum()))
display(analysis.head())

# %% [markdown]
# The matched table contains one quality-controlled Pier annual mean and one finite GISTEMP annual anomaly per retained year. An inner one-to-one merge makes the paired sample explicit. It excludes sparse Pier years and any incomplete NASA annual value; it does not repair changes in local sampling or isolate a causal driver.

# %%
fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
axes[0].plot(analysis.year, analysis.pier_mean_sst_c, marker="o", ms=3, lw=1)
axes[0].set(ylabel="Pier annual mean SST (°C)", title="Matched annual climate series")
axes[1].plot(analysis.year, analysis.global_temp_anomaly_c, marker="o", ms=3, lw=1, color="C1")
axes[1].set(xlabel="Year", ylabel="Global anomaly (°C vs 1951–1980)")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# Both series may show low-frequency warming, while individual Pier years depart substantially from the global pattern. A shared time trend can create a strong scatterplot association even when short-term changes do not closely covary, so the coefficient must remain attached to the plotted time structure.

# %%
x = analysis.global_temp_anomaly_c.to_numpy()
y = analysis.pier_mean_sst_c.to_numpy()
correlation = float(np.corrcoef(x, y)[0, 1])
slope_local_per_global, intercept_c = np.polyfit(x, y, 1)
analysis["fitted_pier_sst_c"] = intercept_c + slope_local_per_global * x
analysis["residual_c"] = y - analysis.fitted_pier_sst_c

print(f"r={correlation:.3f}")
print(f"slope={slope_local_per_global:.3f} local °C per global-anomaly °C")
print(f"intercept={intercept_c:.3f} °C at a 0 °C global anomaly")

order = np.argsort(x)
fig, ax = plt.subplots(figsize=(7.5, 4.8))
points = ax.scatter(x, y, c=analysis.year, cmap="viridis", s=35, alpha=0.8)
ax.plot(x[order], analysis.fitted_pier_sst_c.to_numpy()[order], color="C3", lw=2)
ax.set(
    title="Annual Pier SST versus global temperature anomaly",
    xlabel="NASA global anomaly (°C vs 1951–1980)",
    ylabel="Pier annual mean SST (°C)",
)
ax.grid(alpha=0.25)
fig.colorbar(points, ax=ax, label="Year")
fig.tight_layout()

# %% [markdown]
# The slope is the fitted local annual-SST difference associated with a 1 °C higher global anomaly across the matched years. The intercept is the fitted Pier SST when the GISTEMP anomaly equals its 1951–1980 baseline. The color progression makes calendar time visible: this bivariate slope is not automatically a causal, equilibrium, or transferable local climate sensitivity.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].scatter(analysis.fitted_pier_sst_c, analysis.residual_c, c=analysis.year, cmap="viridis")
axes[0].axhline(0, color="0.25", lw=0.8)
axes[0].set(title="Residuals versus fitted", xlabel="Fitted Pier SST (°C)", ylabel="Residual (°C)")
axes[1].plot(analysis.year, analysis.residual_c, marker="o", ms=3, lw=1)
axes[1].axhline(0, color="0.25", lw=0.8)
axes[1].set(title="Residuals in time order", xlabel="Year", ylabel="Residual (°C)")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()
lag1 = float(analysis.residual_c.autocorr(lag=1))
print(f"lag-one residual correlation={lag1:.3f}")

# %% [markdown]
# The residual plots reveal local warm/cool departures, changing spread, nonlinear structure, or remaining runs that one fitted line cannot represent. Lag-one residual correlation is a dependence diagnostic, not an automatic correction or proof of a particular physical mechanism.

# %%
analysis["year_gap"] = analysis.year.diff()
analysis["pier_sst_change_c"] = analysis.pier_mean_sst_c.diff()
analysis["global_temp_change_c"] = analysis.global_temp_anomaly_c.diff()
changes = analysis.loc[
    analysis.year_gap.eq(1),
    ["year", "pier_sst_change_c", "global_temp_change_c"],
].copy()
assert len(changes) >= 10
change_correlation = float(changes.pier_sst_change_c.corr(changes.global_temp_change_c))
change_slope, change_intercept = np.polyfit(
    changes.global_temp_change_c,
    changes.pier_sst_change_c,
    1,
)

comparison = pd.DataFrame(
    {
        "n pairs": [len(analysis), len(changes)],
        "correlation": [correlation, change_correlation],
        "slope": [slope_local_per_global, change_slope],
    },
    index=["annual levels", "year-to-year changes"],
)
display(comparison)

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.scatter(changes.global_temp_change_c, changes.pier_sst_change_c, alpha=0.75)
change_x = np.linspace(changes.global_temp_change_c.min(), changes.global_temp_change_c.max(), 100)
ax.plot(change_x, change_intercept + change_slope * change_x, color="C3", lw=2)
ax.axhline(0, color="0.4", lw=0.7)
ax.axvline(0, color="0.4", lw=0.7)
ax.set(
    title="Sensitivity: year-to-year changes",
    xlabel="Change in global anomaly (°C/year)",
    ylabel="Change in Pier annual mean SST (°C/year)",
)
ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# Comparing levels with first differences diagnoses how strongly a shared low-frequency trend contributes to the reported association. Differencing changes the scientific question, emphasizes noisy short-term variability, and does not eliminate confounding, measurement change, lagged response, or dependence.

# %%
print(
    f"Across {len(analysis)} matched annual values from {analysis.year.min()}–{analysis.year.max()}, "
    f"Pier surface SST and NASA global temperature anomaly had r={correlation:.2f} and a fitted "
    f"slope of {slope_local_per_global:.2f} local °C per global-anomaly °C. The residual lag-one "
    f"correlation was {lag1:.2f}. In consecutive-year changes, r={change_correlation:.2f}; this "
    "sensitivity helps reveal the role of shared trend but does not establish attribution."
)

# %% [markdown]
# **Bounded claim:** Within the matched, quality-screened years, annual Pier SST and NASA's global anomaly have the plotted association and fitted slope. Residuals and the levels-versus-changes comparison show important time structure and sensitivity. This analysis does not identify a causal effect, isolate forcings or climate modes, guarantee independent annual errors, or establish the same relationship for another coastal site or period.

# %% [markdown]
# ## Continuation: Pier SST and Scripps Mauna Loa CO₂
#
# The official monthly in-situ record includes a scientific preamble, three header rows, measured and filled products, and `-99.99` missing sentinels. This example uses measured monthly CO₂ and requires at least eight observed months per annual mean.

# %%
MLO_URL = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"
mlo_path = CLIMATE_RAW / "Scripps_MLO_monthly_in_situ_CO2.csv"
if not mlo_path.exists():
    urlretrieve(MLO_URL, mlo_path)

mlo_lines = mlo_path.read_text(encoding="utf-8-sig").splitlines()
mlo_header_matches = [
    index for index, line in enumerate(mlo_lines) if line.lstrip().startswith("Yr, Mn,")
]
assert len(mlo_header_matches) == 1
print("MLO source URL:", MLO_URL)
print("MLO header line:", mlo_header_matches[0] + 1)

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

print("CO2 matched years", co2_analysis.year.min(), co2_analysis.year.max(), "n=", len(co2_analysis))
print(f"levels r={co2_levels_r:.3f}; year-to-year changes r={co2_changes_r:.3f}")

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
# A strong levels correlation is expected to be influenced by the fact that both series rise through much of the common period. Atmospheric CO₂ is a climate forcing, but this contemporaneous local bivariate fit is not an attribution model: forcing acts through the climate system, responses can lag, and Pier SST also reflects regional circulation, upwelling, climate modes, weather, and sampling. The measured-versus-filled product choice, access date, Scripps citation, and CC BY attribution must remain with the analysis.
