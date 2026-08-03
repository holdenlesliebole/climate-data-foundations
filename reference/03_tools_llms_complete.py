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
# # Reference: terminal, VS Code, and verified Copilot use
#
# This reference records the concepts and completed code from Tuesday 1. It does not reproduce a student's Copilot conversation; prompts and proposals should be saved only when they contain no credentials or restricted information.

# %%
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent
PRACTICE_ROOT = PROJECT_ROOT / "data" / "processed" / "terminal_practice"
print(Path.cwd(), sys.executable, sep="\n")

# %% [markdown]
# ## Terminal meanings
#
# - `pwd`: print the current working directory.
# - `ls`: list a directory without changing it.
# - `cd`: change the terminal's current directory.
# - `mkdir`: create a directory.
# - `cp`: make another file while preserving the source.
# - `mv`: move or rename a path.
# - `head`: inspect the beginning of a text file.
#
# The scavenger hunt created `results/temperature_preview.csv`; it did not alter `observations/pier_preview.csv`. We practiced under `processed/` because generated/disposable files do not belong beside immutable provider responses in `raw/`.

# %%
paths = {
    "source": PRACTICE_ROOT / "observations" / "pier_preview.csv",
    "copy": PRACTICE_ROOT / "results" / "temperature_preview.csv",
}
for label, path in paths.items():
    print(label, path.exists(), path.relative_to(PROJECT_ROOT))


# %% [markdown]
# ## Four related pieces of state
#
# The VS Code project folder anchors relative paths. The terminal has its own current working directory. The selected interpreter supplies packages. The notebook kernel is a running interpreter process. Checking `Path.cwd()`, `path.exists()`, and `sys.executable` distinguishes many path/environment failures before reinstalling anything.

# %% [markdown]
# ## Correct unit conversion and explicit missingness

# %%
def kelvin_to_celsius(values):
    """Convert Kelvin values to degrees Celsius."""
    values = np.asarray(values)
    return values - 273.15

assert np.isclose(kelvin_to_celsius(273.15), 0.0)
assert np.isclose(kelvin_to_celsius(0.0), -273.15)
print(kelvin_to_celsius([273.15, 300.0]))


# %%
def mean_temperature(values, *, skip_missing=False):
    """Return a mean; missing values propagate unless the caller opts out."""
    values = np.asarray(values, dtype=float)
    if skip_missing:
        return np.nanmean(values)
    return np.mean(values)

example = [15.0, 16.0, np.nan, 17.0]
print("propagate:", mean_temperature(example))
print("skip explicitly:", mean_temperature(example, skip_missing=True))


# %% [markdown]
# The keyword makes the scientific choice visible at the call site. It still does not establish that omitting missing observations is unbiased; the analyst must inspect the amount and pattern of missingness.

# %% [markdown]
# ## Completed bounded plotting change

# %%
def plot_temperature(time, temperature_c):
    """Plot equal-length one-dimensional time and Celsius arrays."""
    time = np.asarray(time)
    temperature_c = np.asarray(temperature_c, dtype=float)
    if time.ndim != 1 or temperature_c.ndim != 1:
        raise ValueError("time and temperature_c must both be one-dimensional")
    if len(time) != len(temperature_c):
        raise ValueError("time and temperature_c must have equal length")

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(time, temperature_c, marker="o")
    ax.set(
        title="Example temperature record",
        xlabel="Observation",
        ylabel="Temperature (°C)",
    )
    ax.grid(alpha=0.25)
    return ax


# %%
ax = plot_temperature([1, 2, 3], [15.0, np.nan, 16.2])
assert ax.get_ylabel() == "Temperature (°C)"

for bad_time, bad_temperature in [([1, 2], [15.0]), ([[1, 2]], [[15.0, 16.0]])]:
    try:
        plot_temperature(bad_time, bad_temperature)
    except ValueError as error:
        print("expected error:", error)
    else:
        raise AssertionError("invalid input should have raised ValueError")

# %% [markdown]
# A suitable prompt named the exact function, required one-dimensional equal-length arrays, preserved labels/return type, prohibited filling/dropping and new packages, and supplied normal/adversarial checks. Those checks catch shape/length regression and a lost unit label. They do not catch a scientifically wrong temperature series, incorrect time zone, misleading sampling, or a plausible-but-wrong interpretation.

# %% [markdown]
# ## Safety
#
# Never paste credentials, access tokens, personally identifiable information, unpublished/restricted data, reviewer material, or private code into an external service. Inspect generated commands especially for deletion, permissions, installation, upload, credentials, or broad paths. A generated suggestion cannot authorize an action.
