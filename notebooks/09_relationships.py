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
# # Wave relationships, residuals, and bounded claims
#
# Friday's application begins with the local CDIP MOP file acquired Tuesday. You will examine the relationship between peak period (`waveTp`) and significant wave height (`waveHs`), interpret a fitted slope in physical units, inspect residuals and time dependence, and visualize peak direction without averaging angles naively.
#
# **Minimum viable takeaway:** plot before calculating a relationship, report slope units, inspect what the line missed, and state what the association cannot establish.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - inspect the source, metadata, flags, and missingness used in a relationship analysis;
# - calculate and interpret correlation and a least-squares line;
# - calculate fitted values/residuals and diagnose one limitation;
# - compare a full and trimmed fit as a sensitivity check; and
# - display direction as circular data with its convention stated.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists(), "Open the course project folder first."

# %% [markdown]
# ## 1. Select the preserved local response
#
# You may have both a seven-day teaching file and a longer assignment file. The code chooses the local NetCDF with the most `obs` values and prints the choice. It never analyzes the live URL.

# %%
mop_files = sorted((PROJECT_ROOT / "data" / "raw" / "mop").glob("*.nc"))
assert mop_files, "No local MOP NetCDF found. Revisit Tuesday's acquisition/recovery checkpoint."


def observation_count(path):
    with xr.open_dataset(path) as candidate:
        return int(candidate.sizes.get("obs", 0))


mop_path = max(mop_files, key=observation_count)
with xr.open_dataset(mop_path) as opened:
    mop = opened.load()

required = {"waveHs", "waveTp", "waveDp", "waveFlagPrimary", "waveFlagSecondary"}
assert required.issubset(mop.data_vars), f"Missing variables: {sorted(required.difference(mop.data_vars))}"

print("Local source:", mop_path.relative_to(PROJECT_ROOT))
print("Dimensions:", dict(mop.sizes))
print("Time coverage:", mop.time.min().item(), "to", mop.time.max().item())
for name in ["waveHs", "waveTp", "waveDp"]:
    print(
        name,
        "| units:", mop[name].attrs.get("units", "not stated"),
        "| long_name:", mop[name].attrs.get("long_name", "not stated"),
    )
print("Primary flag meanings:", mop.waveFlagPrimary.attrs.get("flag_meanings", "not stated"))

# %% [markdown]
# Record before analysis:
#
# - Why is this MOP product not a direct buoy observation? **TODO**
# - `waveHs` meaning/units: **TODO**
# - `waveTp` meaning/units: **TODO**
# - `waveDp` convention from the received metadata: **TODO**
# - One reason hourly rows may be dependent: **TODO**

# %% [markdown]
# ## 2. Make the usable paired table
#
# The core selection requires primary flag value `1` (`good` in the development response) and finite height/period pairs. Confirm the meaning from your own file before accepting the rule.

# %%
frame = mop[["waveHs", "waveTp", "waveDp", "waveFlagPrimary", "waveFlagSecondary"]].to_dataframe().reset_index()
print("Primary flag counts")
display(frame.waveFlagPrimary.value_counts(dropna=False).sort_index())
display(frame[["waveHs", "waveTp", "waveDp"]].isna().mean().rename("missing fraction"))

analysis = (
    frame.loc[frame.waveFlagPrimary.eq(1)]
    .dropna(subset=["time", "waveHs", "waveTp"])
    .sort_values("time")
    .copy()
)
assert len(analysis) >= 10, "Too few good finite pairs for this exercise."
print("Usable height-period pairs:", len(analysis))

# %% [markdown]
# **Selection statement:** TODO—name the file/window, paired variables, flag rule, missing rule, and one limitation.

# %% [markdown]
# ## 3. Plot first, then calculate
#
# Predict the sign of the relationship and name one possible nonlinear, seasonal, or event-related pattern a single coefficient could miss. **TODO**

# %%
fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.scatter(analysis.waveTp, analysis.waveHs, s=14, alpha=0.25)
ax.set(
    title="CDIP MOP: significant wave height versus peak period",
    xlabel=f"Peak period ({mop.waveTp.attrs.get('units', 'units not stated')})",
    ylabel=f"Significant wave height ({mop.waveHs.attrs.get('units', 'units not stated')})",
)
ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# Describe direction, form, strength, unusual points, and any group/time structure you cannot see in this uncolored scatterplot. **TODO**

# %% [markdown]
# ## 4. Correlation and least-squares line
#
# Here $x$ is peak period in seconds and $y$ is wave height in meters. Therefore the slope units are meters per second: fitted height change per one-second higher peak period in this selected sample.

# %%
x = analysis.waveTp.to_numpy()
y = analysis.waveHs.to_numpy()

correlation = float(np.corrcoef(x, y)[0, 1])
slope_m_per_s, intercept_m = np.polyfit(x, y, deg=1)
analysis["fitted_waveHs"] = intercept_m + slope_m_per_s * analysis.waveTp
analysis["residual_m"] = analysis.waveHs - analysis.fitted_waveHs

print(f"Pearson correlation r = {correlation:.3f}")
print(f"Slope = {slope_m_per_s:.3f} m per s")
print(f"Intercept = {intercept_m:.3f} m")
print(f"Mean residual = {analysis.residual_m.mean():.3e} m")

# %%
order = np.argsort(x)
fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.scatter(x, y, s=14, alpha=0.22, label="Hourly model output")
ax.plot(x[order], analysis.fitted_waveHs.to_numpy()[order], color="C3", lw=2, label="Least-squares line")
ax.set(
    title="Height–period relationship with fitted line",
    xlabel="Peak period (s)",
    ylabel="Significant wave height (m)",
)
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# Complete:
#
# - A one-second higher peak period is associated with **TODO** m higher/lower fitted wave height in this selected file.
# - The correlation says **TODO**, but it does not say **TODO**.
# - The intercept **is/is not** physically useful here because **TODO**.

# %% [markdown]
# ## 5. Inspect what the line missed
#
# A residual is observed minus fitted: $e_i=y_i-\hat{y}_i$. Positive residuals are higher than the line predicted.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].scatter(analysis.fitted_waveHs, analysis.residual_m, s=14, alpha=0.25)
axes[0].axhline(0, color="0.25", lw=0.8)
axes[0].set(title="Residuals versus fitted height", xlabel="Fitted wave height (m)", ylabel="Residual (m)")

axes[1].plot(analysis.time, analysis.residual_m, lw=0.8)
axes[1].axhline(0, color="0.25", lw=0.8)
axes[1].set(title="Residuals in time order", xlabel="Time (UTC)", ylabel="Residual (m)")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()

lag1_residual_correlation = float(analysis.residual_m.autocorr(lag=1))
print(f"Lag-one residual autocorrelation = {lag1_residual_correlation:.3f}")

# %% [markdown]
# Identify one residual pattern or lack of pattern. What does lag-one residual correlation suggest about treating every hourly row as independent? **TODO**

# %% [markdown]
# ## 6. Sensitivity to the most extreme predictor/response values
#
# This is not an instruction to delete extremes. It asks whether the fitted summary is dominated by the outer 1% of height or period values. Investigate those rows before defending either analysis.

# %%
tp_low, tp_high = analysis.waveTp.quantile([0.01, 0.99])
hs_low, hs_high = analysis.waveHs.quantile([0.01, 0.99])
central = analysis.loc[
    analysis.waveTp.between(tp_low, tp_high)
    & analysis.waveHs.between(hs_low, hs_high)
].copy()

trimmed_r = float(central.waveTp.corr(central.waveHs))
trimmed_slope, trimmed_intercept = np.polyfit(central.waveTp, central.waveHs, 1)

sensitivity = pd.DataFrame(
    {
        "n": [len(analysis), len(central)],
        "correlation": [correlation, trimmed_r],
        "slope_m_per_s": [slope_m_per_s, trimmed_slope],
        "intercept_m": [intercept_m, trimmed_intercept],
    },
    index=["all selected rows", "central 98% of height and period"],
)
display(sensitivity)

# %% [markdown]
# Did the sign and practical magnitude remain similar? What evidence would you inspect before deciding whether an outer value is valid, influential, or erroneous? **TODO**

# %% [markdown]
# ## 7. Peak direction is circular
#
# Read the received `waveDp` metadata aloud. The plot below treats 0°/360° as the same direction. Do not report an ordinary arithmetic mean of degrees near the wraparound.

# %%
direction = analysis.waveDp.dropna().to_numpy() % 360
theta = np.deg2rad(direction)
direction_bins = np.linspace(0, 2 * np.pi, 13)

fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw={"projection": "polar"})
ax.hist(theta, bins=direction_bins, alpha=0.75)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title("Peak-direction distribution\n(check wave-from convention in metadata)", pad=18)
fig.tight_layout()

print("waveDp attributes:", mop.waveDp.attrs)

# %% [markdown]
# **Direction note:** TODO—state the convention/units from the file, describe the dominant sector without an ordinary mean, and explain why 1° and 359° are neighbors.

# %% [markdown]
# ## Core product: bounded relationship statement
#
# Write four to six sentences that include:
#
# 1. source/window and selected rows;
# 2. direction/strength plus fitted slope with units;
# 3. one residual or time-dependence finding;
# 4. one sensitivity result; and
# 5. one claim the analysis cannot support.
#
# **Interpretation:** TODO

# %% [markdown]
# ## Exit ticket
#
# Write one claim the fitted result supports and one it cannot support. Name the plot/check that most changed your trust in the coefficient.
#
# **Answer:** TODO

# %% [markdown]
# ## Continuation lane
#
# Choose one:
#
# 1. Fit the relationship separately by month or by two physically meaningful periods. Plot both groups and report whether pooled correlation hides a difference.
# 2. Add one deliberately extreme but labeled point to a copy of the table and quantify its effect on $r$, slope, and residuals. Never alter the raw NetCDF.
# 3. Calculate a circular mean direction from sine/cosine components and report resultant-vector length as concentration; verify the file's wave-from convention first.
# 4. Aggregate to daily values and compare slope/residual autocorrelation with the hourly analysis. Explain what information and dependence the aggregation changes.
