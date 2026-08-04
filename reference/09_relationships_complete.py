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
# # Reference: wave relationships, residuals, and bounded claims
#
# This completed reference fits a simple peak-period/significant-height relationship in the longest local D0513 MOP response, checks residual/time structure, performs a trimmed sensitivity comparison, and treats direction as circular. Results update with the locally acquired response.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent

files = sorted((PROJECT_ROOT / "data" / "raw" / "mop").glob("*.nc"))
assert files, "Acquire the MOP NetCDF response first."


def observation_count(path):
    with xr.open_dataset(path) as candidate:
        return int(candidate.sizes.get("obs", 0))


path = max(files, key=observation_count)
with xr.open_dataset(path) as opened:
    mop = opened.load()

required = {"waveHs", "waveTp", "waveDp", "waveFlagPrimary", "waveFlagSecondary"}
assert required.issubset(mop.data_vars)
print(path.relative_to(PROJECT_ROOT), dict(mop.sizes), mop.time.min().item(), mop.time.max().item())
for name in ["waveHs", "waveTp", "waveDp", "waveFlagPrimary"]:
    print(name, mop[name].attrs)

# %% [markdown]
# MOP values are model-derived nearshore output rather than direct buoy observations. The received attributes define units, valid ranges, primary/secondary flag meanings, and peak-direction convention. Hourly rows can be dependent because wave fields and forcing persist through time.

# %%
frame = mop[["waveHs", "waveTp", "waveDp", "waveFlagPrimary", "waveFlagSecondary"]].to_dataframe().reset_index()
display(frame.waveFlagPrimary.value_counts(dropna=False).sort_index())
display(frame[["waveHs", "waveTp", "waveDp"]].isna().mean().rename("missing fraction"))
analysis = (
    frame.loc[frame.waveFlagPrimary.eq(1)]
    .dropna(subset=["time", "waveHs", "waveTp"])
    .sort_values("time")
    .copy()
)
assert len(analysis) >= 10
print("usable pairs", len(analysis))

# %% [markdown]
# The analysis uses finite height/period pairs whose primary flag equals the file's documented good value. It retains direction when present for a separate circular view. This selection does not make consecutive hours independent or turn model output into direct observation.

# %%
fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.scatter(analysis.waveTp, analysis.waveHs, s=14, alpha=0.25)
ax.set(title="CDIP MOP: significant wave height versus peak period", xlabel="Peak period (s)", ylabel="Significant wave height (m)")
ax.grid(alpha=0.25)
fig.tight_layout()

x = analysis.waveTp.to_numpy()
y = analysis.waveHs.to_numpy()
correlation = float(np.corrcoef(x, y)[0, 1])
slope_m_per_s, intercept_m = np.polyfit(x, y, 1)
analysis["fitted_waveHs"] = intercept_m + slope_m_per_s * analysis.waveTp
analysis["residual_m"] = analysis.waveHs - analysis.fitted_waveHs
print(f"r={correlation:.3f}; slope={slope_m_per_s:.3f} m/s; intercept={intercept_m:.3f} m")

order = np.argsort(x)
fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.scatter(x, y, s=14, alpha=0.22, label="Hourly model output")
ax.plot(x[order], analysis.fitted_waveHs.to_numpy()[order], color="C3", lw=2, label="Least-squares line")
ax.set(title="Height–period relationship with fitted line", xlabel="Peak period (s)", ylabel="Significant wave height (m)")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

# %% [markdown]
# The slope is the fitted change in significant wave height, in meters, associated with a one-second higher peak period within this selected file. Pearson $r$ reports unitless linear association, not physical effect size or causation. The intercept evaluates an extrapolated 0-second period and is unlikely to have a useful physical interpretation.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].scatter(analysis.fitted_waveHs, analysis.residual_m, s=14, alpha=0.25)
axes[0].axhline(0, color="0.25", lw=0.8)
axes[0].set(title="Residuals versus fitted height", xlabel="Fitted height (m)", ylabel="Residual (m)")
axes[1].plot(analysis.time, analysis.residual_m, lw=0.8)
axes[1].axhline(0, color="0.25", lw=0.8)
axes[1].set(title="Residuals in time order", xlabel="Time (UTC)", ylabel="Residual (m)")
for ax in axes:
    ax.grid(alpha=0.25)
fig.tight_layout()
lag1 = float(analysis.residual_m.autocorr(lag=1))
print(f"lag-one residual autocorrelation={lag1:.3f}")

# %% [markdown]
# Residual-versus-fitted structure diagnoses curvature or changing variance; the time view exposes runs/events that the unordered scatterplot hides. Nonzero lag-one residual correlation is evidence against treating hourly residuals as independent, although it does not select a complete time-series model.

# %%
tp_low, tp_high = analysis.waveTp.quantile([0.01, 0.99])
hs_low, hs_high = analysis.waveHs.quantile([0.01, 0.99])
central = analysis.loc[
    analysis.waveTp.between(tp_low, tp_high) & analysis.waveHs.between(hs_low, hs_high)
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
    index=["all selected rows", "central 98%"],
)
display(sensitivity)

# %% [markdown]
# The full-versus-central comparison reveals whether the sign and practical slope magnitude depend strongly on outer observations. It does not justify deleting them. Check metadata, flags, neighboring times, physical range, and acquisition/processing evidence first.

# %%
direction = analysis.waveDp.dropna().to_numpy() % 360
theta = np.deg2rad(direction)
fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw={"projection": "polar"})
ax.hist(theta, bins=np.linspace(0, 2 * np.pi, 13), alpha=0.75)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title("Peak-direction distribution\n(use received wave-from convention)", pad=18)
fig.tight_layout()
print(mop.waveDp.attrs)

# %% [markdown]
# The polar histogram keeps north adjacent across 0°/360°. State the received direction convention before naming a sector. An ordinary arithmetic mean can place 1° and 359° at 180°, the opposite direction.

# %%
print(
    f"In {path.name}, {len(analysis)} good finite hourly MOP pairs had Pearson r={correlation:.2f}. "
    f"The fitted slope was {slope_m_per_s:.3f} m of significant wave height per second of peak "
    f"period. Lag-one residual correlation was {lag1:.2f}; inspect the plotted residual pattern and "
    f"the full-versus-central sensitivity table before interpreting precision."
)

# %% [markdown]
# **Bounded claim:** Within the selected local MOP model-output response, peak period and significant height show the plotted fitted association and slope above. Residual/time structure and the sensitivity comparison describe important limits of the single line. The analysis does not establish causation, independent hourly errors, direct-observation truth, long-term stability, or transfer to another site/season.
