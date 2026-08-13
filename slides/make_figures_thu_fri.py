"""Figures for the Thursday and Friday decks.

Everything is computed from the course data already on disk: the Pier temperature
archive and the preserved NASA GISTEMP response. No invented numbers — the values
printed at the end are the ones quoted on the slides.

    python3 slides/make_figures_thu_fri.py
"""
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
OUT = Path(__file__).parent / "figs"
OUT.mkdir(exist_ok=True)

from climate_course.pier import load_pier_temperature  # noqa: E402
from climate_course.climate_series import (  # noqa: E402
    annual_pier_surface,
    load_gistemp_annual,
)

RED, CYAN, GRAY, AMBER = "#D9534A", "#2E9BA0", "#8A939F", "#C9A227"
plt.rcParams.update({
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
    "text.color": GRAY, "axes.labelcolor": GRAY, "xtick.color": GRAY,
    "ytick.color": GRAY, "axes.edgecolor": GRAY, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
})
RNG = np.random.default_rng(2026)


def save(fig, name, **kw):
    fig.savefig(OUT / f"{name}.png", transparent=True, bbox_inches="tight", **kw)
    plt.close(fig)


# ---------------------------------------------------------------- data
pier = load_pier_temperature(sorted((ROOT / "data/raw/pier").glob("LaJolla_TEMP_*.csv"))[-1])
paired = pier.dropna(subset=["SURF_TEMP_C", "BOT_TEMP_C"]).copy()
paired["surface_minus_bottom_c"] = paired.SURF_TEMP_C - paired.BOT_TEMP_C
summer = paired[paired.date.dt.month.isin([6, 7, 8])]
daily = summer.surface_minus_bottom_c.to_numpy()
annual = summer.groupby(summer.date.dt.year).surface_minus_bottom_c.mean()
annual_means = annual.to_numpy()

s_daily, n_daily = daily.std(ddof=1), daily.size
s_annual, n_annual = annual_means.std(ddof=1), annual_means.size

# ============================================================ THURSDAY
# 1 — one distribution, three summaries
fig, ax = plt.subplots(figsize=(7.6, 3.6), dpi=170)
ax.hist(daily, bins=60, color=CYAN, alpha=0.55, edgecolor="none")
for value, color, label in [(daily.mean(), RED, f"mean {daily.mean():.2f}"),
                             (np.median(daily), AMBER, f"median {np.median(daily):.2f}")]:
    ax.axvline(value, color=color, lw=1.8, label=label)
ax.axvspan(daily.mean() - s_daily, daily.mean() + s_daily, color=RED, alpha=0.10,
           label=f"± 1 s  ({s_daily:.2f} °C)")
ax.set_xlabel("surface − bottom temperature (°C)")
ax.set_ylabel("number of summer days")
ax.set_title(f"Every usable summer day, {n_daily:,} of them", color=GRAY, fontsize=12, pad=8)
ax.legend(frameon=False, fontsize=10, labelcolor=GRAY)
save(fig, "thu_distribution")

# 2 — the central distinction: spread of data vs spread of the estimate
sample_means = np.array([RNG.choice(daily, size=n_daily, replace=True).mean()
                         for _ in range(4000)])
# Stacked on one shared axis: the estimate's distribution is ~90x narrower, so
# overlaying them on one y-scale renders it as a spike and flattens the other.
fig, axes = plt.subplots(2, 1, figsize=(8.6, 4.4), dpi=170, sharex=True)
axes[0].hist(daily, bins=70, color=CYAN, alpha=0.6, edgecolor="none")
axes[0].set_ylabel("summer days")
axes[0].set_title(f"How much do individual days vary?   s = {s_daily:.2f} °C",
                  color=CYAN, fontsize=12, pad=8, fontweight="bold")
axes[0].annotate("", xy=(daily.mean() - s_daily, axes[0].get_ylim()[1] * 0.72),
                 xytext=(daily.mean() + s_daily, axes[0].get_ylim()[1] * 0.72),
                 arrowprops=dict(arrowstyle="<->", color=CYAN, lw=1.8))
axes[0].text(daily.mean(), axes[0].get_ylim()[1] * 0.78, "± 1 s", ha="center",
             fontsize=10.5, color=CYAN, fontweight="bold")

se = sample_means.std(ddof=1)
axes[1].hist(sample_means, bins=70, color=RED, alpha=0.85, edgecolor="none")
axes[1].set_ylabel("resamples")
axes[1].set_xlabel("surface − bottom temperature (°C)")
axes[1].set_title(f"How much would the estimated mean move?   SE = {se:.3f} °C",
                  color=RED, fontsize=12, pad=8, fontweight="bold")
axes[1].annotate(f"the whole distribution is {2 * se:.2f} °C wide —\n"
                 f"about {s_daily / se:.0f}× narrower than the panel above",
                 xy=(daily.mean(), axes[1].get_ylim()[1] * 0.5),
                 xytext=(daily.mean() + 1.6, axes[1].get_ylim()[1] * 0.75),
                 fontsize=10.5, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
for a in axes:
    a.grid(True, lw=0.4, alpha=0.2, color=GRAY)
fig.suptitle("Same axis, same data, two completely different questions",
             color=GRAY, fontsize=11.5, y=1.02)
save(fig, "thu_spread_vs_error")

# 3 — why the interval narrows and the data does not
counts = np.unique(np.geomspace(5, n_daily, 40).astype(int))
fig, ax = plt.subplots(figsize=(7.0, 3.4), dpi=170)
ax.plot(counts, s_daily / np.sqrt(counts), lw=2, color=RED, label=r"SE = s / $\sqrt{n}$")
ax.axhline(s_daily, ls="--", lw=1.4, color=CYAN, label=f"s = {s_daily:.2f} °C, unchanged")
ax.set_xscale("log")
ax.set_xlabel("number of observations, n")
ax.set_ylabel("°C")
ax.set_title("More data shrinks the uncertainty, not the variability",
             color=GRAY, fontsize=12, pad=8)
ax.legend(frameon=False, fontsize=10.5, labelcolor=GRAY)
ax.grid(True, lw=0.4, alpha=0.22, color=GRAY)
save(fig, "thu_sqrt_n")

# 4 — bootstrap over years
boot_years = np.array([RNG.choice(annual_means, size=n_annual, replace=True).mean()
                       for _ in range(4000)])
lo, hi = np.percentile(boot_years, [2.5, 97.5])
fig, ax = plt.subplots(figsize=(7.6, 3.4), dpi=170)
ax.hist(boot_years, bins=60, color=CYAN, alpha=0.65, edgecolor="none")
ax.axvline(annual_means.mean(), color=RED, lw=2, label=f"estimate {annual_means.mean():.2f} °C")
for edge in (lo, hi):
    ax.axvline(edge, color=RED, ls="--", lw=1.4)
ax.axvspan(lo, hi, color=RED, alpha=0.08, label=f"95% interval  {lo:.2f} to {hi:.2f} °C")
ax.set_xlabel("mean of a resampled set of summers (°C)")
ax.set_ylabel("resamples")
ax.set_title(f"4,000 resamples of the {n_annual} summers", color=GRAY, fontsize=12, pad=8)
ax.legend(frameon=False, fontsize=10.5, labelcolor=GRAY)
save(fig, "thu_bootstrap")

# 5 — the unit you resample decides the answer
boot_days = np.array([RNG.choice(daily, size=n_daily, replace=True).mean()
                      for _ in range(2000)])
d_lo, d_hi = np.percentile(boot_days, [2.5, 97.5])
fig, ax = plt.subplots(figsize=(8.2, 2.9), dpi=170)
ax.errorbar(annual_means.mean(), 1, xerr=[[annual_means.mean() - lo], [hi - annual_means.mean()]],
            fmt="o", color=RED, capsize=6, lw=2.4, ms=9)
ax.errorbar(daily.mean(), 0, xerr=[[daily.mean() - d_lo], [d_hi - daily.mean()]],
            fmt="o", color=CYAN, capsize=6, lw=2.4, ms=9)
ax.set_yticks([0, 1])
ax.set_yticklabels([f"resample DAYS\n{n_daily:,} units", f"resample SUMMERS\n{n_annual} units"],
                   fontsize=10.5)
ax.set_ylim(-0.6, 1.6)
ax.set_xlabel("mean summer surface − bottom difference (°C)")
ax.text(daily.mean(), -0.42, f"width {d_hi - d_lo:.3f} °C", ha="center", fontsize=10, color=CYAN)
ax.text(annual_means.mean(), 1.42, f"width {hi - lo:.3f} °C  ·  {(hi - lo) / (d_hi - d_lo):.1f}× wider",
        ha="center", fontsize=10, color=RED, fontweight="bold")
ax.set_title("Same data, same statistic, one modeling choice",
             color=GRAY, fontsize=12, pad=10)
save(fig, "thu_resampling_unit")

# 6 — why days are not independent units
lag_x, lag_y = daily[:-1], daily[1:]
same_summer = summer.date.dt.year.to_numpy()
keep = same_summer[:-1] == same_summer[1:]
fig, ax = plt.subplots(figsize=(4.6, 4.4), dpi=170)
ax.scatter(lag_x[keep], lag_y[keep], s=4, color=CYAN, alpha=0.28, edgecolors="none")
ax.set_xlabel("difference on day t (°C)")
ax.set_ylabel("difference on day t + 1 (°C)")
lag1 = pd.Series(daily).autocorr(1)
ax.set_title(f"Adjacent days, r = {lag1:.2f}", color=GRAY, fontsize=12, pad=8)
ax.text(0.04, 0.96, "independent units\nwould be a shapeless blob",
        transform=ax.transAxes, va="top", fontsize=10, color=RED)
save(fig, "thu_autocorrelation")

# ============================================================ FRIDAY
gistemp = load_gistemp_annual(ROOT / "data/raw/climate/NASA_GISTEMP_global.csv")
pier_annual = annual_pier_surface(pier)
matched = (gistemp.merge(pier_annual, on="year", how="inner")
           .dropna(subset=["global_temp_anomaly_c", "pier_mean_sst_c"]))
matched = matched[matched.n_pier_days >= 300].reset_index(drop=True)

x = matched.global_temp_anomaly_c.to_numpy()
y = matched.pier_mean_sst_c.to_numpy()
years = matched.year.to_numpy()
r_levels = np.corrcoef(x, y)[0, 1]
b1 = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
b0 = y.mean() - b1 * x.mean()
fitted = b0 + b1 * x
resid = y - fitted
dx, dy = np.diff(x), np.diff(y)
r_changes = np.corrcoef(dx, dy)[0, 1]
resid_ac = pd.Series(resid).autocorr(1)

# 7 — look at time before anything else
fig, axes = plt.subplots(2, 1, figsize=(8.4, 4.4), dpi=170, sharex=True)
axes[0].plot(years, x, lw=1.5, color=RED)
axes[0].set_ylabel("global anomaly (°C)")
axes[0].set_title("Both series rise. That alone will produce a correlation.",
                  color=GRAY, fontsize=12, pad=8)
axes[1].plot(years, y, lw=1.5, color=CYAN)
axes[1].set_ylabel("Pier SST (°C)")
axes[1].set_xlabel("year")
for a in axes:
    a.grid(True, lw=0.4, alpha=0.22, color=GRAY)
save(fig, "fri_time_first")

# 8 — the fit itself
fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=170)
points = ax.scatter(x, y, c=years, cmap="viridis", s=26, edgecolors="none")
order = np.argsort(x)
ax.plot(x[order], fitted[order], lw=2, color=RED)
bar = fig.colorbar(points, ax=ax, pad=0.02)
bar.set_label("year", color=GRAY)
bar.ax.tick_params(colors=GRAY)
ax.set_xlabel("NASA global temperature anomaly (°C)")
ax.set_ylabel("annual mean Pier SST (°C)")
ax.set_title(f"r = {r_levels:+.2f}   slope = {b1:+.2f} °C per °C",
             color=GRAY, fontsize=12, pad=8)
ax.text(0.03, 0.96, f"Pier SST = {b0:.2f} + {b1:.2f} × anomaly",
        transform=ax.transAxes, va="top", fontsize=10.5, color=RED, family="monospace")
save(fig, "fri_regression")

# 9 — residuals, the diagnostic view
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.4), dpi=170)
axes[0].scatter(fitted, resid, s=22, color=CYAN, alpha=0.75, edgecolors="none")
axes[0].axhline(0, color=RED, lw=1.2)
axes[0].set_xlabel("fitted Pier SST (°C)")
axes[0].set_ylabel("residual (°C)")
axes[0].set_title("against the fit", color=GRAY, fontsize=11.5, pad=6)
axes[1].plot(years, resid, lw=1.3, color=CYAN)
axes[1].axhline(0, color=RED, lw=1.2)
axes[1].set_xlabel("year")
axes[1].set_title(f"against time — lag-1 r = {resid_ac:+.2f}", color=GRAY, fontsize=11.5, pad=6)
for a in axes:
    a.grid(True, lw=0.4, alpha=0.22, color=GRAY)
fig.suptitle("Long runs above and below zero: the line left time structure behind",
             color=GRAY, fontsize=11.5, y=1.04)
save(fig, "fri_residuals")

# 10 — levels versus year-to-year changes
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.9), dpi=170)
axes[0].scatter(x, y, s=24, color=CYAN, alpha=0.75, edgecolors="none")
axes[0].plot(x[order], fitted[order], lw=1.8, color=RED)
axes[0].set_xlabel("global anomaly (°C)")
axes[0].set_ylabel("Pier SST (°C)")
axes[0].set_title(f"LEVELS    r = {r_levels:+.2f}", color=RED, fontsize=12.5, pad=8,
                  fontweight="bold")
axes[1].scatter(dx, dy, s=24, color=CYAN, alpha=0.75, edgecolors="none")
axes[1].axhline(0, color=GRAY, lw=0.8)
axes[1].axvline(0, color=GRAY, lw=0.8)
axes[1].set_xlabel("change in global anomaly (°C)")
axes[1].set_ylabel("change in Pier SST (°C)")
axes[1].set_title(f"YEAR-TO-YEAR CHANGES    r = {r_changes:+.2f}", color=RED,
                  fontsize=12.5, pad=8, fontweight="bold")
for a in axes:
    a.grid(True, lw=0.4, alpha=0.22, color=GRAY)
fig.suptitle("Remove the shared trend and most of the relationship goes with it",
             color=GRAY, fontsize=11.5, y=1.03)
save(fig, "fri_levels_vs_changes")

# 11 — four samples, one correlation
def build_same_r(n=120):
    base_x = RNG.normal(0, 1, n)
    linear = 0.75 * base_x + RNG.normal(0, 0.66, n)
    curved = 0.9 * base_x ** 2 + RNG.normal(0, 0.4, n)
    clustered = np.where(base_x > 0, base_x * 0.3 + 1.4, base_x * 0.3 - 1.4)
    outlier_x = np.append(RNG.normal(0, 0.55, n - 1), 4.2)
    outlier_y = np.append(RNG.normal(0, 0.55, n - 1), 4.2)
    return [("a straight relationship", base_x, linear),
            ("a curve", base_x, curved),
            ("two groups", base_x, clustered),
            ("one influential point", outlier_x, outlier_y)]


fig, axes = plt.subplots(1, 4, figsize=(11.6, 3.0), dpi=170)
for ax, (label, px, py) in zip(axes, build_same_r()):
    ax.scatter(px, py, s=14, color=CYAN, alpha=0.7, edgecolors="none")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(label, color=GRAY, fontsize=10.5, pad=6)
    ax.text(0.5, -0.09, f"r = {np.corrcoef(px, py)[0, 1]:+.2f}", transform=ax.transAxes,
            ha="center", va="top", fontsize=11, color=RED, fontweight="bold")
fig.suptitle("Four samples. Similar correlations. Only one is a straight line.",
             color=GRAY, fontsize=11.5, y=1.08)
save(fig, "fri_same_r")

# ---------------------------------------------------------------- report
print(f"""
THURSDAY
  summer daily differences   n = {n_daily:,}   s = {s_daily:.3f} °C
  iid standard error         {s_daily / np.sqrt(n_daily):.4f} °C
  annual summer means        n = {n_annual}   s = {s_annual:.3f} °C
  bootstrap over summers     {annual_means.mean():.2f} °C  [{lo:.2f}, {hi:.2f}]  width {hi - lo:.3f}
  bootstrap over days        [{d_lo:.2f}, {d_hi:.2f}]  width {d_hi - d_lo:.3f}
  years interval is          {(hi - lo) / (d_hi - d_lo):.1f}x wider
  daily lag-1 autocorrelation {lag1:+.3f}

FRIDAY
  matched years              {len(matched)}  ({years.min()}-{years.max()}, >= 300 days)
  r levels                   {r_levels:+.3f}
  r first differences        {r_changes:+.3f}
  slope                      {b1:+.3f} °C local per °C global
  intercept                  {b0:.2f} °C
  lag-1 residual autocorr    {resid_ac:+.3f}
""")
for p in sorted(OUT.glob("thu_*.png")) + sorted(OUT.glob("fri_*.png")):
    print(f"  {p.name:28s} {p.stat().st_size / 1024:6.0f} KB")
