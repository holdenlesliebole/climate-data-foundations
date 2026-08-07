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
# # Code you can trust: errors, functions, and one honest check
#
# By now you have copied a block of plotting code more than once. That is normal, and it is also the
# moment when repeated code starts producing quietly inconsistent figures. Today you give that
# repeated work a name, and you add one check that makes a wrong result fail loudly instead of
# looking plausible.
#
# **Minimum viable takeaway:** read the last line of an error message first, write and call one
# function, and add one check that would catch a real mistake.
#
# **You do not need to finish the whole notebook.** The core path ends at the **Core checkpoint**
# after section 5. Everything after it is **Go further**.
#
# :::{tip} Need an example?
# The [annotated completed reference](../reference/05_reliable_code_complete.ipynb) shows every core
# step with an explanation of *why* it works and which mistakes are most common. Looking at it is a
# research skill, not cheating. Predict first, then compare.
# :::
#
# Keep open: the [errors and functions guide](../notes/functions_and_errors.md) and the
# [plotting-format guide](../notes/plotting_foundations.md).

# %% [markdown]
# ## Learning objectives
#
# By the core checkpoint, you can:
#
# - read a Python traceback from its last line upward and say what failed before changing anything;
# - name the three errors you will hit most often this year and the first thing to check for each;
# - write a function with inputs, a body, and a return value, and call it more than once;
# - replace repeated plotting code with one function call per panel; and
# - add one `assert` that catches a wrong unit before it reaches a figure.
#
# In **Go further** you can read the course loader module, use `ValueError` for invalid user input,
# write a known-value test, and run the repository `pytest` suite.

# %% [markdown]
# ## Setup: run this first
#
# This cell finds the project root and loads the Pier record. `load_pier_temperature` is supplied
# working code for now — you will open it in **Go further** and see exactly what it does.
#
# If the Pier archive from Monday is missing, the cell falls back to a small built-in teaching
# example so that today's lesson still works. The printed source line tells you which one you have.
# Teaching values are invented; never cite them as observations.

# %%
from pathlib import Path
import sys
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists(), f"Unexpected working directory: {Path.cwd()}"

SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.pier import (
    EXAMPLE_PIER_NOTE,
    example_pier_frame,
    load_pier_temperature,
)

temperature_files = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
if temperature_files:
    pier = load_pier_temperature(temperature_files[-1])
    data_source = temperature_files[-1].name
else:
    pier = example_pier_frame()
    data_source = EXAMPLE_PIER_NOTE

print("Data source:", data_source)
print("Rows and columns:", pier.shape)
print("Date range:", pier["date"].min().date(), "to", pier["date"].max().date())
pier.head()

# %% [markdown]
# ## 1. Worked example: three cells that are almost the same
#
# Read the next cell before running it. It is close to what you would get by copying Monday's
# plotting block twice and editing it.
#
# **Predict:** what will be different about the two figures, and what will be identical?

# %%
recent = pier[pier["date"] >= pier["date"].max() - pd.Timedelta(days=365)]

# Panel 1 — surface
fig, ax = plt.subplots(figsize=(9, 2.8))
ax.plot(recent["date"], recent["SURF_TEMP_C"], lw=1.2, label="Surface")
ax.set(title="Scripps Pier surface temperature", xlabel="Date", ylabel="Temperature (°C)")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()

# Panel 2 — bottom
fig, ax = plt.subplots(figsize=(9, 2.8))
ax.plot(recent["date"], recent["BOT_TEMP_C"], lw=1.2, label="Bottom")
ax.set(title="Scripps Pier bottom temperature", xlabel="Date", ylabel="Temp")
ax.legend()
fig.tight_layout()

# %% [markdown]
# ### Read, then answer
#
# 1. How many lines differ between the two blocks? Name each difference.
# 2. Two differences are *intentional* (the data and the label). The rest are *accidents* of copying.
#    Find the accidents.
# 3. If you now wanted every Pier figure in your final project to have a grid, how many places would
#    you have to edit?
#
# **Accidents I found:** TODO
#
# This is the argument for functions. Not elegance — consistency. A copied block drifts, and the
# drift is invisible in the figure.

# %% [markdown]
# ## 2. Errors are evidence, not verdicts
#
# Before writing a function, learn to read what Python says when something goes wrong. A traceback
# is a report, and its **last line** is the finding. Everything above it is the chain of calls that
# led there — useful second, not first.
#
# Each of the next three cells fails on purpose. They are wrapped so the notebook keeps running;
# outside a `try` block Jupyter shows the same text in a red box.
#
# For each one, answer in this order: **What is the error type? What is the last line telling me?
# What is the smallest thing I can print to check it?**

# %% [markdown]
# ### Error 1: `NameError`

# %%
try:
    print(suface_temperature)  # noqa: F821 — deliberate typo
except Exception:
    traceback.print_exc()

# %% [markdown]
# - Error type: **TODO**
# - What it means in plain language: **TODO**
# - First thing to check: **TODO**

# %% [markdown]
# ### Error 2: `FileNotFoundError`
#
# This is the most common error of the whole week. It is almost never about the file.

# %%
try:
    pd.read_csv("data/raw/pier/temperatures.csv")
except Exception:
    traceback.print_exc()

# %%
# The diagnostic, in three prints. Run this before you change any path.
print("Python is currently working in:", Path.cwd())
print("The pier folder exists:", (PROJECT_ROOT / "data" / "raw" / "pier").exists())
print("Files it contains:", [p.name for p in (PROJECT_ROOT / "data" / "raw" / "pier").glob("*")])

# %% [markdown]
# - Was the path wrong, or was the file genuinely absent? **TODO**
# - A relative path such as `"data/raw/..."` is interpreted from the working directory printed
#   above, which is why the same line works in one notebook and fails in another.

# %% [markdown]
# ### Error 3: `KeyError`

# %%
try:
    print(pier["SURFACE_TEMP_C"])
except Exception:
    traceback.print_exc()

# %%
# The diagnostic: ask the data what it actually contains.
print("Requested: SURFACE_TEMP_C")
print("Available columns:", list(pier.columns))
print("Exact match exists:", "SURFACE_TEMP_C" in pier.columns)


# %% [markdown]
# The provider's column is `SURF_TEMP_C`. A good diagnosis names the symptom *and* the evidence:
# "pandas raised `KeyError` because the requested string does not exactly match any column name."
#
# Notice what none of these three errors required: reinstalling anything, restarting the computer, or
# rewriting the analysis. Each was answered by one print.
#
# **Pair task:** the person who has typed least so far reads the next traceback aloud, last line
# first. Say what failed before either of you touches the code.

# %% [markdown]
# ## 3. Worked example: the anatomy of a function
#
# A function packages a piece of work under a name so you can run it again without retyping it.
#
# ```python
# def name_of_function(input_one, input_two):   # header: name and inputs (parameters)
#     """One line saying what it does."""       # docstring: what a reader needs to know
#     result = input_one + input_two           # body: the work
#     return result                            # return: the value handed back to the caller
# ```
#
# **Predict** the two printed values before running.

# %%
def temperature_range(values):
    """Return the difference between the largest and smallest recorded value."""
    observed = pd.Series(values).dropna()
    return observed.max() - observed.min()


print("range of [10, 12, 15]:", temperature_range([10, 12, 15]))
print("range of recent surface temperature (°C):", round(temperature_range(recent["SURF_TEMP_C"]), 2))


# %% [markdown]
# Four things to notice, because they are where beginners get stuck:
#
# 1. Defining a function runs nothing. `def` only creates the name. The work happens when you
#    *call* it with parentheses.
# 2. `values` is a placeholder. It takes whatever you pass in, and it exists only inside the
#    function.
# 3. Without `return`, a function hands back `None` — a very common cause of "why is my variable
#    empty?"
# 4. The same function worked on a plain list and on a DataFrame column. That reuse is the point.
#
# **Modify and check:** change `temperature_range` so it returns the range rounded to one decimal
# place, then call it again on both inputs.
#
# **What changed:** TODO

# %% [markdown]
# ## 4. Core task: turn the repeated plotting code into a function
#
# Now fix section 1. The scaffold below has the function header, docstring, and return statement.
# Copy the plotting lines from the **first** panel of section 1 into the body, replacing the
# hard-coded pieces with the parameter names.

# %%
def plot_pier_temperature(dates, values, label, title):
    """Plot one labeled Pier temperature series and return its axes."""
    fig, ax = plt.subplots(figsize=(9, 2.8))

    # TODO: plot `values` against `dates` using `label` for the legend entry.
    # TODO: set the title from `title`, the x-label to "Date", and the y-label to "Temperature (°C)".
    # TODO: add the legend and the grid.

    fig.tight_layout()
    return ax


plot_pier_temperature(
    recent["date"],
    recent["SURF_TEMP_C"],
    label="Surface",
    title="Scripps Pier surface temperature, most recent year",
)

# %% [markdown]
# ### Check before continuing
#
# - Does the figure have a title, both axis labels with a unit, a legend, and a grid?
# - Call the function a second time with `recent["BOT_TEMP_C"]` and `label="Bottom"`. Did you have
#   to retype any plotting code?
# - Change `figsize` to `(9, 2.2)` **inside the function** and rerun both calls. Both panels change
#   from one edit. That is the property you were missing in section 1.

# %%
# TODO: call plot_pier_temperature a second time for the bottom series.

# %% [markdown]
# ## 5. One check that fails loudly
#
# A function can also carry an assumption. `assert` states a condition that must be true and stops
# with your message when it is not.
#
# Sea-surface temperature at Scripps Pier is somewhere between about −2 °C and 40 °C. Anything
# outside that is not an unusual ocean — it is a unit mistake, a fill value, or the wrong column.
# The version below refuses to draw such a figure.

# %%
PLAUSIBLE_SST_C = (-2.0, 40.0)


def plot_pier_temperature_checked(dates, values, label, title):
    """Plot one Pier temperature series after checking that the values are plausible °C."""
    observed = pd.Series(values).dropna()
    low, high = PLAUSIBLE_SST_C

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
    recent["date"],
    recent["SURF_TEMP_C"],
    label="Surface",
    title="Scripps Pier surface temperature, checked",
)

# %% [markdown]
# ### Watch it catch a real mistake
#
# Someone converts to Fahrenheit and forgets to change the axis label. Without the check you get a
# clean, well-labeled, completely wrong figure. **Predict what the message will say.**

# %%
surface_f = recent["SURF_TEMP_C"] * 9 / 5 + 32

try:
    plot_pier_temperature_checked(
        recent["date"],
        surface_f,
        label="Surface",
        title="Scripps Pier surface temperature",
    )
except AssertionError:
    traceback.print_exc()

# %% [markdown]
# A silent wrong answer is worse than a loud failure. The check cost two lines and caught a mistake
# that a reviewer would probably not notice on a plot.
#
# What the check does **not** establish: that the sensor was calibrated, that the record is complete,
# that flagged values were handled, or that the interpretation is right. A passing check is a
# statement about one specific assumption and nothing else.
#
# **Discuss:** name one Pier or MOP assumption you could write as an `assert` in one line.
#
# **My check:** TODO

# %% [markdown]
# ## Core checkpoint
#
# Produce three panels — surface, bottom, and their difference — using **only calls** to
# `plot_pier_temperature_checked`, then answer the figure questions below.
#
# The difference series is computed for you. Note that it can be near zero or slightly negative, so
# it needs its own plausible range; that is a hint about what makes a check honest rather than
# decorative.

# %%
paired = recent.dropna(subset=["SURF_TEMP_C", "BOT_TEMP_C"]).copy()
paired["surface_minus_bottom_c"] = paired["SURF_TEMP_C"] - paired["BOT_TEMP_C"]

# TODO: call plot_pier_temperature_checked three times — surface, bottom, and the difference.
# The difference will fail the -2 to 40 °C check for a good reason. Read the message, then decide:
# do you widen the range, or do you write a second function for differences? Say why in one sentence.

# %% [markdown]
# ### Figure check (use this every day)
#
# 1. What question does the figure answer? **TODO**
# 2. What does each axis represent, including units? **TODO**
# 3. What is the one-sentence interpretation? **TODO**
# 4. What can this figure **not** establish? **TODO**
#
# ### And the code check
#
# - Which lines exist once now that existed three times in section 1? **TODO**
# - Your decision about the difference panel's range, and why: **TODO**
#
# :::{tip} Compare with the completed reference
# This is the end of the core path. Open the
# [annotated reference](../reference/05_reliable_code_complete.ipynb), compare your function with
# the one there, and read the "common mistakes" notes before continuing.
# :::

# %% [markdown]
# ## Exit ticket
#
# - One mistake today's check would catch: **TODO**
# - One scientifically important mistake it would **not** catch: **TODO**

# %% [markdown]
# ---
#
# # Go further
#
# The rest of the notebook is the deeper version of the same ideas. Choose a section; you are not
# expected to finish them all.

# %% [markdown]
# ### A. Default arguments and a real multi-panel figure
#
# Three separate figures are three separate images. Adding an `ax=None` parameter lets the same
# function either make its own figure or draw into one you supply.

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
# `ax=None` is a *default argument*: callers who do not care get sensible behavior, callers who do
# get control. Compare the three-panel version with three separate figures and say which better
# supports the comparison you actually want to make.
#
# **Which and why:** TODO

# %% [markdown]
# ### B. Read the loader you have been using
#
# Open `src/climate_course/pier.py` in VS Code. It contains the header discovery, column check, and
# date construction that Monday made you do by hand. Find:
#
# - the function's input and what it returns;
# - where the header row is discovered, and why it is not hard-coded as line 47;
# - where expected columns are checked;
# - which failures raise `ValueError` rather than returning something wrong;
# - one scientific problem the loader cannot detect.
#
# **Notes:** TODO

# %% [markdown]
# ### C. `assert` versus `ValueError`
#
# `assert` is a check *you* run on your own reasoning. A `ValueError` is how a function tells its
# *caller* that the request was invalid. Assertions can be disabled by the interpreter; validation of
# user input should not depend on them.

# %%
from climate_course.pier import surface_bottom_difference

selection = surface_bottom_difference(
    pier,
    str(pier["date"].min().date()),
    str(pier["date"].max().date()),
    good_only=True,
)
print("paired good-flagged rows:", len(selection))
selection.head()

# %%
try:
    surface_bottom_difference(pier, "2025-06-30", "2025-01-01")
except ValueError as error:
    print("Expected failure:", error)
else:
    raise AssertionError("A reversed window should fail.")


# %% [markdown]
# The reversed window fails immediately with a message naming the problem, instead of silently
# returning an empty table that you would later summarize as though it meant something.

# %% [markdown]
# ### D. A summary function and a known-value test
#
# The strongest test uses an input whose answer you already know by hand.

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
print("Known-value test passed:", known)
print("Real selection:", summarize_difference(selection))

# %% [markdown]
# Add a `NaN` to `tiny` and decide whether `dropna` is the behavior you intend. Then write a test
# that documents the choice, so a future reader learns it from the code rather than guessing.

# %% [markdown]
# ### E. Run the repository test suite
#
# `tests/test_pier.py` builds a tiny provider-shaped CSV, so it runs without the network or the full
# archive. Run it from the VS Code terminal at the course root:
#
# ```bash
# pytest -q tests/test_pier.py
# ```
#
# Then open the file and read one test. Passing means those specific examples behaved as expected in
# this environment. It does not prove the observations are correct, that a future provider schema
# will load, or that any interpretation is sound. A test is an executable claim with a stated
# boundary.

# %% [markdown]
# ### F. Continuation
#
# - Move `plot_pier_temperature_checked` into `src/climate_course/` and import it here and in one
#   other notebook; confirm both produce the same figure.
# - Add type hints to your function and a `Raises:` line to its docstring.
# - Use `pytest.mark.parametrize` to test `surface_bottom_difference` with `good_only=True/False`,
#   a missing column, and several date windows.
# - Restart the kernel and run the whole notebook. A notebook that only works in the order you
#   happened to click is not a reproducible analysis.
