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
# # Annotated reference: errors, functions, and one honest check
#
# This is the completed version of
# [Wednesday 1](../notebooks/05_reliable_code.ipynb). It is written to be read after you have tried
# the exercise, and it explains *why* each piece works rather than only what to type. Each core
# section ends with a **Common mistakes** box describing what actually goes wrong in class.
#
# Core check: **Can I read a traceback, write a function that removes repetition, and say what my
# check does and does not establish?**

# %%
from pathlib import Path
import sys
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name in {"notebooks", "reference"}:
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from climate_course.pier import (
    EXAMPLE_PIER_NOTE,
    example_pier_frame,
    load_pier_temperature,
    surface_bottom_difference,
)

temperature_files = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
if temperature_files:
    pier = load_pier_temperature(temperature_files[-1])
    data_source = temperature_files[-1].name
else:
    pier = example_pier_frame()
    data_source = EXAMPLE_PIER_NOTE

recent = pier[pier["date"] >= pier["date"].max() - pd.Timedelta(days=365)]
print("Data source:", data_source)
print("Rows in the most recent year:", len(recent))

# %% [markdown]
# The `if/else` is not decoration. It answers a question every analysis should answer in writing:
# *which file produced this figure?* Printing the source is the cheapest form of provenance there
# is, and it costs one line.

# %% [markdown]
# ## 1. Why the repeated cells were a problem
#
# The two copied blocks in the guided notebook differ in five places, but only two of those
# differences were intended:
#
# | Line | Intended? | Consequence |
# |---|---|---|
# | `SURF_TEMP_C` → `BOT_TEMP_C` | yes | different data, the point of the second panel |
# | `label="Surface"` → `label="Bottom"` | yes | correct legend |
# | `ylabel="Temperature (°C)"` → `ylabel="Temp"` | no | second panel loses its unit |
# | title text | partly | fine here, but hand-edited titles drift out of date |
# | missing `ax.grid(alpha=0.25)` | no | the two panels are no longer visually comparable |
#
# Three of five differences are copy damage. Nothing in either figure looks broken, which is exactly
# why this is worth catching: the failure mode of copied code is not a crash, it is quiet
# inconsistency. Answer to "how many places would you edit to add a grid everywhere?" — one per
# copy, forever, and you will miss one.

# %% [markdown]
# ## 2. Reading tracebacks
#
# The rule is **last line first**. The last line names the error type and the specific thing Python
# could not do. The lines above it are the call chain — read them second, to find which of *your*
# lines started it.

# %%
try:
    print(suface_temperature)  # noqa: F821 — deliberate typo
except Exception:
    traceback.print_exc()

# %% [markdown]
# `NameError: name 'suface_temperature' is not defined` means Python has never seen that name. In
# practice it is one of three things, in order of likelihood:
#
# 1. a typo (`suface` for `surface`);
# 2. the cell that defined the name was never run, or was run and then the kernel restarted;
# 3. the name is defined inside a function and is not visible outside it.
#
# The diagnostic is to look at the name Python quoted back at you, character by character. It is
# quoting *your* spelling, not the correct one.

# %%
try:
    pd.read_csv("data/raw/pier/temperatures.csv")
except Exception:
    traceback.print_exc()

# %%
print("Python is currently working in:", Path.cwd())
print("The pier folder exists:", (PROJECT_ROOT / "data" / "raw" / "pier").exists())
print("Files it contains:", [p.name for p in (PROJECT_ROOT / "data" / "raw" / "pier").glob("*")])

# %% [markdown]
# `FileNotFoundError` is the week's most common error and it is usually about the **working
# directory**, not the file. A relative path such as `"data/raw/pier/..."` is resolved from wherever
# Python currently is. Open the same notebook from a different folder and the identical line fails.
#
# Two habits remove the problem permanently:
#
# - print `Path.cwd()` before blaming the path;
# - build paths from an anchor — `PROJECT_ROOT / "data" / "raw" / "pier"` — instead of writing
#   relative strings that depend on where you happened to start.
#
# Note also that the real filename is `LaJolla_TEMP_1916-202603.csv`, not `temperatures.csv`. Use
# `.glob()` and print what you found rather than typing a filename you half-remember.

# %%
try:
    print(pier["SURFACE_TEMP_C"])
except Exception:
    traceback.print_exc()

# %%
print("Requested: SURFACE_TEMP_C")
print("Available columns:", list(pier.columns))
print("Exact match exists:", "SURFACE_TEMP_C" in pier.columns)


# %% [markdown]
# `KeyError` means the label does not exist in the object you asked. The provider's column is
# `SURF_TEMP_C`. Column names are exact: case, underscores, and stray spaces all count. When a name
# looks right but fails, print `list(frame.columns)` — trailing whitespace in a provider header is
# invisible until you do.
#
# ### Common mistakes: tracebacks
#
# - **Reading top-down and panicking at the file paths.** The top of a traceback is often inside
#   pandas or matplotlib. That is not where your bug is. Start at the bottom.
# - **Changing code before naming the failure.** If you cannot say the failure in a sentence, any
#   edit is a guess. One print first.
# - **Treating an error as a verdict on yourself.** Three of the errors above are typing and
#   location problems. Every working scientist produces them daily.
# - **Reinstalling packages.** A `KeyError` is evidence about a string, not about your installation.

# %% [markdown]
# ## 3. What a function is
#
# A function has four parts: a header naming it and its parameters, a docstring, a body, and a
# `return` handing a value back.

# %%
def temperature_range(values):
    """Return the difference between the largest and smallest recorded value."""
    observed = pd.Series(values).dropna()
    return observed.max() - observed.min()


print("range of [10, 12, 15]:", temperature_range([10, 12, 15]))
print("range of recent surface temperature (°C):", round(temperature_range(recent["SURF_TEMP_C"]), 2))


# %% [markdown]
# `pd.Series(values)` is what lets one function accept a plain list *and* a DataFrame column: both
# are converted to the same representation before the work starts. `.dropna()` states the missing
# value policy in the open — a range calculated across a `NaN` would be `NaN`, which is technically
# correct and practically useless.
#
# ### Common mistakes: functions
#
# - **"I ran the cell and nothing happened."** Defining a function runs none of its body. `def`
#   creates a name; calling it with `(...)` does the work.
# - **Forgetting `return`.** A function without `return` hands back `None`, so
#   `answer = my_function(x)` silently produces `None` and the failure appears three cells later.
# - **Expecting the parameter name to exist outside.** `values` lives only inside the function.
#   Printing `values` afterwards raises `NameError`.
# - **Relying on a variable the function did not receive.** If the body mentions `recent` without it
#   being a parameter, the function quietly works on whatever `recent` happens to be at call time.
#   That is the single most common source of "it worked yesterday."

# %% [markdown]
# ## 4. Core solution: the repeated plot becomes one function

# %%
def plot_pier_temperature(dates, values, label, title):
    """Plot one labeled Pier temperature series and return its axes."""
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.plot(dates, values, lw=1.2, label=label)
    ax.set(title=title, xlabel="Date", ylabel="Temperature (°C)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return ax


plot_pier_temperature(
    recent["date"], recent["SURF_TEMP_C"], "Surface", "Scripps Pier surface temperature"
)
plot_pier_temperature(
    recent["date"], recent["BOT_TEMP_C"], "Bottom", "Scripps Pier bottom temperature"
)

# %% [markdown]
# Both panels now share one definition of "a Pier temperature figure." The y-label and the grid
# cannot drift apart, because there is only one of each. Changing `figsize` once changes both.
#
# `return ax` is what makes the function composable: the caller can keep adjusting the figure
# afterwards (`ax.axhline(0)`, `ax.set_ylim(...)`) without the function having to anticipate every
# need.
#
# ### Common mistakes: this refactor
#
# - **Leaving a hard-coded column inside the body.** If `ax.plot(dates, recent["SURF_TEMP_C"])`
#   survives the edit, every call draws the surface series regardless of what was passed. The
#   giveaway is two identical figures with different legends.
# - **Passing the whole DataFrame.** `plot_pier_temperature(recent, ...)` is tempting, but then the
#   function must know the column names, and it stops working on MOP or ERA5 data. Passing the two
#   arrays keeps it general.
# - **Calling with arguments in the wrong order.** Positional arguments are matched by position, not
#   name. Writing `label="Surface"` explicitly at the call site is worth the extra characters.

# %% [markdown]
# ## 5. One check that fails loudly

# %%
PLAUSIBLE_SST_C = (-2.0, 40.0)


def plot_pier_temperature_checked(dates, values, label, title, plausible=PLAUSIBLE_SST_C):
    """Plot one Pier temperature series after checking that the values are plausible °C."""
    observed = pd.Series(values).dropna()
    low, high = plausible

    assert len(observed) > 0, f"Nothing to plot for {label}: every value is missing."
    assert observed.between(low, high).all(), (
        f"{label} values fall outside {low} to {high} °C "
        f"(observed {observed.min():.1f} to {observed.max():.1f}). "
        "Check the units before plotting."
    )

    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.plot(dates, values, lw=1.2, label=label)
    ax.set(title=title, xlabel="Date", ylabel="Temperature (°C)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return ax


plot_pier_temperature_checked(
    recent["date"], recent["SURF_TEMP_C"], "Surface", "Scripps Pier surface temperature, checked"
)

# %%
surface_f = recent["SURF_TEMP_C"] * 9 / 5 + 32

try:
    plot_pier_temperature_checked(
        recent["date"], surface_f, "Surface", "Scripps Pier surface temperature"
    )
except AssertionError:
    traceback.print_exc()

# %% [markdown]
# The Fahrenheit series produces a figure that is clean, labeled, and wrong by 30-odd degrees. No
# reviewer scanning a slide would catch it; two lines of `assert` catch it every time.
#
# Three properties make this a good check rather than a ritual:
#
# 1. **It encodes physics, not code.** −2 °C to 40 °C comes from what seawater at a Southern
#    California pier can be, not from anything about pandas.
# 2. **The message names the evidence.** It prints the observed minimum and maximum, so the reader
#    diagnoses the problem from the message alone.
# 3. **It fails before the figure exists.** A check placed after plotting still leaves a wrong
#    figure on screen for someone to screenshot.
#
# What it does **not** establish: sensor calibration, that the record is complete, that flagged
# observations were handled, that the sampling is representative, that observations are independent,
# or that the interpretation is right. A check is a statement about one assumption. It is silent
# about every other assumption.
#
# ### Common mistakes: assertions
#
# - **A check with no message.** `assert observed.between(low, high).all()` alone prints nothing
#   useful. The message is most of the value.
# - **A range so wide it can never fire.** `assert observed.between(-1000, 1000).all()` is
#   decoration. If you cannot describe a value the check would reject, it is not a check.
# - **A range so narrow it fires on real data.** A check that people learn to comment out is worse
#   than no check, because it teaches the habit of ignoring failures.
# - **Using `assert` to validate someone else's input.** Assertions can be switched off by the
#   interpreter (`python -O`). For a function others call, raise `ValueError` — see section B.

# %% [markdown]
# ## Core checkpoint solution: three panels, and an honest range
#
# The difference series is the interesting case. Surface minus bottom is a small number near zero,
# often slightly negative, so it legitimately fails the −2 to 40 °C check.

# %%
paired = recent.dropna(subset=["SURF_TEMP_C", "BOT_TEMP_C"]).copy()
paired["surface_minus_bottom_c"] = paired["SURF_TEMP_C"] - paired["BOT_TEMP_C"]

plot_pier_temperature_checked(
    paired["date"], paired["SURF_TEMP_C"], "Surface", "Surface temperature"
)
plot_pier_temperature_checked(
    paired["date"], paired["BOT_TEMP_C"], "Bottom", "Bottom temperature"
)

difference_axes = plot_pier_temperature_checked(
    paired["date"],
    paired["surface_minus_bottom_c"],
    "Surface − bottom",
    "Surface minus bottom temperature",
    plausible=(-10.0, 10.0),
)
difference_axes.set_ylabel("Difference (°C)")
difference_axes.axhline(0, color="0.3", lw=0.8)


# %% [markdown]
# **The decision, and why.** Widening the shared range to cover differences would destroy the
# check for the temperature panels: −10 to 10 °C would happily accept a Kelvin mix-up as a
# temperature. The right move is a *separate* plausible range for a *different physical quantity*,
# passed explicitly at the call site. That is why the reference version takes `plausible` as a
# parameter with a default: a temperature and a temperature difference are not the same quantity and
# should not share a validity range.
#
# This is the general lesson about checks. The question is never "what range makes the error go
# away," it is "what does this number physically mean, and what values would be impossible?"
#
# **Figure check answers for the difference panel**
#
# 1. *Question:* how does the top-to-bottom temperature contrast at the Pier vary through the year?
# 2. *Axes:* date on the horizontal axis; surface minus bottom temperature in °C on the vertical.
# 3. *Interpretation:* the difference is largest in the warm season and near zero in winter, which is
#    consistent with a stratified water column in summer and a mixed one in winter.
# 4. *Cannot establish:* it cannot establish the cause of stratification, whether the two depths were
#    measured simultaneously, whether unflagged data are unbiased, or anything about years outside
#    the plotted window. With the built-in teaching values it establishes nothing about the ocean at
#    all.

# %% [markdown]
# ---
#
# # Go further reference

# %% [markdown]
# ### A. `ax=None` and a real multi-panel figure

# %%
def plot_series(dates, values, label, title, ax=None, ylabel="Temperature (°C)"):
    """Plot one labeled series, creating a figure only when no axes are supplied."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 2.8))
    ax.plot(dates, values, lw=1.2, label=label)
    ax.set(title=title, xlabel="Date", ylabel=ylabel)
    ax.legend()
    ax.grid(alpha=0.25)
    return ax


fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
plot_series(paired["date"], paired["SURF_TEMP_C"], "Surface", "Surface", ax=axes[0])
plot_series(paired["date"], paired["BOT_TEMP_C"], "Bottom", "Bottom", ax=axes[1])
plot_series(
    paired["date"],
    paired["surface_minus_bottom_c"],
    "Surface − bottom",
    "Difference",
    ax=axes[2],
    ylabel="Difference (°C)",
)
axes[2].axhline(0, color="0.3", lw=0.8)
fig.suptitle("Scripps Pier temperature, most recent year", y=1.0)
fig.tight_layout()

# %% [markdown]
# The default `ax=None` means the simple call still works unchanged, while a caller who wants a
# shared x-axis can supply the axes. `sharex=True` is what makes the three panels genuinely
# comparable: the dates line up vertically, so a feature in one panel can be traced to the same day
# in the others. Three separate figures cannot do that.

# %% [markdown]
# ### B. `assert` versus `ValueError`

# %%
selection = surface_bottom_difference(
    pier, str(pier["date"].min().date()), str(pier["date"].max().date()), good_only=True
)
print("paired good-flagged rows:", len(selection))

for start, end in [("2025-06-30", "2025-01-01"), ("1899-01-01", "1899-01-02")]:
    try:
        surface_bottom_difference(pier, start, end)
    except ValueError as error:
        print("expected:", error)


# %% [markdown]
# Both failures are useful because they happen *at the point of the mistake*. Without them, a
# reversed window returns an empty table, `mean()` of an empty table is `NaN`, and the problem
# surfaces as a blank figure several cells later — far from its cause. The distance between a bug
# and its symptom is what makes debugging expensive; validation shortens it.
#
# `good_only=True` is a **scientific policy**, not a mechanism. The function makes the policy visible
# and reversible; it cannot tell you whether excluding flagged observations is right for your
# question. That decision stays with you, and belongs in your written interpretation.

# %% [markdown]
# ### C. A summary function and a known-value test

# %%
def summarize_difference(frame):
    """Return count, mean, and sample standard deviation of surface-minus-bottom °C."""
    required = "surface_minus_bottom_c"
    if required not in frame.columns:
        raise ValueError(f"Missing required column: {required}")
    values = frame[required].dropna()
    if len(values) < 2:
        raise ValueError("At least two differences are required.")
    return {
        "count": int(values.count()),
        "mean_c": float(values.mean()),
        "std_c": float(values.std(ddof=1)),
    }


tiny = pd.DataFrame({"surface_minus_bottom_c": [1.0, 2.0, 3.0]})
known = summarize_difference(tiny)
assert known["count"] == 3
assert np.isclose(known["mean_c"], 2.0)
assert np.isclose(known["std_c"], 1.0)
print("known-value test passed:", known)
print("real selection:", summarize_difference(paired))

# %% [markdown]
# The test uses `[1, 2, 3]` because you can do it in your head: the mean is 2, and the sample
# standard deviation is exactly 1. That is the whole trick of a known-value test — pick an input
# where you, not the computer, are the authority on the answer.
#
# `ddof=1` is a scientific choice, not a default to accept silently: it computes the *sample*
# standard deviation, dividing by n−1. With `ddof=0` the expected value here would be about 0.816,
# and the test would fail. Mark's Thursday session explains why the distinction matters.

# %% [markdown]
# ### D. What the repository tests do and do not establish
#
# ```bash
# pytest -q tests/test_pier.py
# ```
#
# The suite builds a small provider-shaped CSV in a temporary folder, so it runs offline and without
# the full archive. It covers header discovery, preserved missing values, date construction, the
# flag policy, one hand-checked difference, and two failure paths.
#
# It cannot establish that the real observations are accurate, that a future provider schema will
# load, that the sampling is representative, that observations are independent, or that any
# interpretation follows. Tests are executable claims with a stated boundary — which is precisely
# what makes them worth writing down.
