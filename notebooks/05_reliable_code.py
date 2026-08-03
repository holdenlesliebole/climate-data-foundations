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
# # Code you can trust: functions, failures, and tests
#
# A notebook is good at showing a scientific question and interpretation. Repeated loading, selection, and validation logic is easier to trust when it has a name, explicit inputs/outputs, clear failure messages, and small tests.
#
# **Minimum viable takeaway:** reliable code is readable, broken into small pieces, and equipped with checks that make wrong results fail loudly.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - decide what belongs in a narrative notebook versus a reusable function/module;
# - read a traceback from its final line upward and isolate the smallest failing example;
# - use assertions and `ValueError` to state assumptions;
# - run a small pytest suite and interpret pass/fail evidence;
# - restart and run an analysis from a local raw input.

# %%
from pathlib import Path
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists()

SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.pier import load_pier_temperature, surface_bottom_difference

# %% [markdown]
# ## 1. A familiar result with hidden fragility
#
# Monday's notebook discovered a header, parsed nine columns, constructed dates, selected a period, handled flags/missing values, and calculated a difference. Copying all those cells into every later analysis can create several almost-identical versions.
#
# With your partner, mark which parts are:
#
# - **scientific narrative:** question, period choice, figure, interpretation;
# - **reusable mechanism:** header discovery, expected-column check, date parsing;
# - **scientific policy:** whether to require flag 0, how to treat missing pairs.
#
# A function can make a policy visible, but it cannot choose the policy for you.

# %%
temperature_files = sorted((PROJECT_ROOT / "data" / "raw" / "pier").glob("LaJolla_TEMP_*.csv"))
assert temperature_files, "Acquire/extract the Pier archive from Monday first."
temperature_path = temperature_files[-1]
pier = load_pier_temperature(temperature_path)
print(pier.shape, pier.date.min(), pier.date.max())

# %% [markdown]
# Open `src/climate_course/pier.py` in VS Code. Find:
#
# - the function input and returned object;
# - where the header is discovered;
# - where expected columns are checked;
# - which errors fail loudly;
# - one scientific issue the loader cannot validate.
#
# **Notes:** TODO

# %% [markdown]
# ## 2. Read tracebacks from the bottom
#
# Imagine a cell used `pier["SURFACE_TEMP_C"]`. The final traceback line is:
#
# ```text
# KeyError: 'SURFACE_TEMP_C'
# ```
#
# Do not start by reinstalling pandas. The exception type and missing key point to a column-name mismatch. Reduce the problem to:

# %%
requested = "SURFACE_TEMP_C"
print("requested:", requested)
print("available temperature columns:", [name for name in pier.columns if "TEMP" in name])
print("exact match exists:", requested in pier.columns)

# %% [markdown]
# Correction: the provider's column is `SURF_TEMP_C`. A good diagnosis names both the symptom and evidence: “pandas raised `KeyError` because the requested string does not exactly match the available column.”
#
# Pair task: for three printed tracebacks, underline the final exception line, identify the first frame in course code, and state the smallest diagnostic print/check before editing.

# %% [markdown]
# ## 3. Turn assumptions into visible failures
#
# The helper below requires a valid period, expected columns, paired measurements, and optionally provider flag 0 for both series. It returns a copy with `surface_minus_bottom_c`.

# %%
paired = surface_bottom_difference(
    pier,
    "2025-01-01",
    "2025-06-30",
    good_only=True,
)
print(paired.shape)
display(paired.head())
display(paired.surface_minus_bottom_c.describe())

# %%
assert paired.date.between("2025-01-01", "2025-06-30").all()
assert paired[["SURF_TEMP_C", "BOT_TEMP_C"]].notna().all().all()
assert paired[["SURF_FLAG", "BOT_FLAG"]].eq(0).all().all()
np.testing.assert_allclose(
    paired.surface_minus_bottom_c,
    paired.SURF_TEMP_C - paired.BOT_TEMP_C,
)
print("CHECK PASSED: dates, paired values, flag policy, and calculation.")

# %% [markdown]
# Assertions are compact developer/scientist checks. A function should raise a descriptive `ValueError` for invalid user input rather than allowing a distant operation to fail confusingly. Neither mechanism proves the observations are unbiased or independent.

# %%
try:
    surface_bottom_difference(pier, "2025-06-30", "2025-01-01")
except ValueError as error:
    print("Expected failure:", error)
else:
    raise AssertionError("A reversed window should fail.")


# %% [markdown]
# ## 4. Write a small summary function and known-value test
#
# This function receives an already selected difference table. Its input is narrower than the whole raw DataFrame, making it easier to reason about and test.

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

summary = summarize_difference(paired)
summary

# %%
tiny = pd.DataFrame({"surface_minus_bottom_c": [1.0, 2.0, 3.0]})
known = summarize_difference(tiny)
assert known["count"] == 3
assert np.isclose(known["mean_c"], 2.0)
assert np.isclose(known["std_c"], 1.0)
print("Known-value test passed:", known)

# %% [markdown]
# Modify the tiny case to include `NaN`. Decide whether `dropna` is the intended behavior, then add a test documenting that choice. Ask a partner for an adversarial input; improve the error/check without changing the scientific question.

# %% [markdown]
# ## 5. Run repository tests
#
# `tests/test_pier.py` uses a tiny generated CSV fixture. It tests header discovery, missing preservation, date parsing, flag filtering, a known difference, and two failure paths without depending on the live Pier archive.

# %%
completed = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", "tests/test_pier.py"],
    cwd=PROJECT_ROOT,
    text=True,
    capture_output=True,
)
print(completed.stdout)
print(completed.stderr)
assert completed.returncode == 0, "The test suite failed; read the first failure above."

# %% [markdown]
# A passing test suite means those specified examples behaved as expected in this environment. It does not prove all inputs, future provider schemas, or scientific interpretations are correct. Tests are executable claims with a defined boundary.

# %% [markdown]
# ## 6. Notebook narrative stays visible

# %%
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(paired.date, paired.surface_minus_bottom_c, lw=1.2)
ax.axhline(0, color="0.3", lw=0.8)
ax.set(
    title="Scripps Pier surface minus near-bottom temperature",
    xlabel="Date",
    ylabel="Temperature difference (°C)",
)
ax.grid(alpha=0.25)
fig.tight_layout()

# %% [markdown]
# **Interpretation:** TODO—write two bounded sentences, including the selection/flag policy and one limitation. The reusable code made the transformation consistent; the notebook still carries the question and scientific meaning.

# %% [markdown]
# ## Exit ticket
#
# Name one failure caught by today's code/tests and one scientifically important failure they cannot catch.
#
# - Caught: **TODO**
# - Not caught: **TODO**

# %% [markdown]
# ## Continuation lane
#
# Add type hints and parameterized tests for `good_only=True/False`, an invalid/missing column, and several date windows. Then use the same helper from a short script and this notebook; verify both produce the same count/mean for a fixed selection.
