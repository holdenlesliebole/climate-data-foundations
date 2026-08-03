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
# # Working environment: terminal, VS Code, and Copilot
#
# This session connects three views of the same project: files in the terminal, files in VS Code, and Python running in a selected environment. It then treats Copilot/LLM output as a proposed change that must be read, run, checked, and explained.
#
# **Minimum viable takeaway:** know which folder and Python you are using; generated code is an untrusted draft until you verify it.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - navigate a bounded practice folder with `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, and `head`;
# - connect terminal working directory, VS Code project, interpreter, and notebook kernel;
# - give Copilot a bounded request with context and acceptance checks;
# - inspect and test a proposal before adopting it;
# - identify commands/data that should not be sent to or run from an AI tool.

# %%
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists(), "Open the whole course project first."

PRACTICE_ROOT = PROJECT_ROOT / "data" / "processed" / "terminal_practice"
print("Notebook working directory:", Path.cwd())
print("Project root:", PROJECT_ROOT)
print("Python executable:", sys.executable)

# %% [markdown]
# ## 1. Terminal scavenger hunt
#
# Open **Terminal → New Terminal** in VS Code. Confirm the prompt is inside the course project, then run:
#
# ```bash
# python scripts/setup_terminal_practice.py
# ```
#
# The script creates only generated files under `data/processed/terminal_practice/` and never overwrites an existing file.

# %% [markdown]
# ### Predict, run, explain
#
# Before each command, predict what folder/file it will show or change. Run one line at a time. Do not copy the comment text after `#`.
#
# ```bash
# pwd
# ls
# cd data/processed/terminal_practice
# pwd
# ls
# ls observations
# head observations/pier_preview.csv
# mkdir results
# cp observations/pier_preview.csv results/pier_preview_copy.csv
# mv results/pier_preview_copy.csv results/temperature_preview.csv
# ls results
# cd ../../..
# pwd
# ```
#
# Use Tab completion rather than retyping long paths. Use the Up arrow to retrieve a previous command. If `mkdir results` says the folder exists, inspect it; do not delete it merely to repeat the exercise.

# %%
expected = [
    PRACTICE_ROOT / "README.txt",
    PRACTICE_ROOT / "observations" / "pier_preview.csv",
    PRACTICE_ROOT / "results" / "temperature_preview.csv",
]
for path in expected:
    print(("FOUND" if path.exists() else "MISSING"), path.relative_to(PROJECT_ROOT))

# %% [markdown]
# ### Explain to your partner
#
# - What did `pwd` answer?
# - Which commands changed your current directory?
# - Which commands created a new path?
# - What is the difference between `cp` and `mv` in this example?
# - Why did we practice in `processed/` instead of `raw/`?
#
# **Notes:** TODO

# %% [markdown]
# ## 2. One project, four pieces of state
#
# Point to each in VS Code:
#
# 1. **Project folder:** top of the Explorer; the shared root for relative paths.
# 2. **Terminal working directory:** output of `pwd`; commands start here.
# 3. **Python interpreter/environment:** executable that supplies packages.
# 4. **Notebook kernel:** running Python process for this notebook.
#
# They should usually refer to this course project/environment, but they are not the same object. A correct file plus the wrong kernel can still produce `ModuleNotFoundError`. A correct kernel plus the wrong directory can produce `FileNotFoundError`.

# %%
preview = PRACTICE_ROOT / "results" / "temperature_preview.csv"
print("exists:", preview.exists())
print("relative path:", preview.relative_to(PROJECT_ROOT))
print("absolute path on this machine:", preview.resolve())
print("Python/kernel:", sys.executable)


# %% [markdown]
# ## 3. Diagnose before changing
#
# Match each symptom to the first check:
#
# | Symptom | First check |
# |---|---|
# | `FileNotFoundError` | `Path.cwd()`, the printed path, and `path.exists()` |
# | `ModuleNotFoundError` | selected kernel and `sys.executable` |
# | command not found | spelling, installed tool, and activated environment |
# | old output after editing | which file is open and whether the cell/script reran |
#
# Pairs: diagnose three instructor cards without fixing them yet. State the evidence that would distinguish your hypothesis from another one.

# %% [markdown]
# ## 4. Copilot/LLM workflow
#
# Use this loop:
#
# ```text
# state the bounded task and context
# → write acceptance checks before seeing the answer
# → request a small proposal
# → read every changed line
# → run it on normal and adversarial inputs
# → inspect scientific units/shape/assumptions
# → accept, revise, or reject
# → explain the final code yourself
# ```
#
# The scientist owns the question, data permissions, execution, validation, and interpretation.

# %% [markdown]
# ### Plausible proposal 1: unit error
#
# An assistant proposed the following conversion. Predict the result for 273.15 K and decide on a known-value check before running it.

# %%
def kelvin_to_celsius_candidate(values):
    values = np.asarray(values)
    return values + 273.15  # proposed code: inspect this sign

candidate_result = kelvin_to_celsius_candidate(273.15)
print("candidate result:", candidate_result)
print("known-value check passed:", np.isclose(candidate_result, 0.0))


# %% [markdown]
# The function runs and returns a number, but the known-value check fails. Fix the sign, rerun the check, and explain why “no traceback” was insufficient evidence.
#
# **Explanation:** TODO

# %% [markdown]
# ### Plausible proposal 2: missingness hidden in a summary

# %%
def mean_temperature_candidate(values):
    """Return the mean temperature."""
    return np.mean(values)

with_missing = np.array([15.0, 16.0, np.nan, 17.0])
print(mean_temperature_candidate(with_missing))


# %% [markdown]
# Should the function propagate missingness, omit missing positions, or refuse to summarize until the caller chooses? More than one design is defensible. The bad behavior is making that scientific choice silently. Write the behavior you want before asking Copilot to change the function.
#
# **Desired behavior and check:** TODO

# %% [markdown]
# ## 5. Bounded Copilot task
#
# The plotting function below works for equal-length one-dimensional inputs but does not check them. In Copilot Chat, request only these changes:
#
# - convert inputs to NumPy arrays;
# - raise a clear `ValueError` unless both are one-dimensional and have equal length;
# - preserve the existing title, labels, and returned `Axes`;
# - do not drop/fill values or add packages.
#
# Tell Copilot the acceptance checks before accepting code. Review the diff one block at a time.

# %%
def plot_temperature(time, temperature_c):
    """Plot temperature in degrees Celsius and return the Matplotlib Axes."""
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(time, temperature_c, marker="o")
    ax.set(
        title="Example temperature record",
        xlabel="Observation",
        ylabel="Temperature (°C)",
    )
    ax.grid(alpha=0.25)
    return ax

# Ask Copilot for the bounded change, then edit this function and rerun the cell.


# %% [markdown]
# ### Acceptance checks
#
# After editing, run the normal case. Then uncomment each adversarial check; both should raise `ValueError` with an explanation you understand.

# %%
ax = plot_temperature([1, 2, 3], [15.0, np.nan, 16.2])
assert ax.get_ylabel() == "Temperature (°C)"
print("normal case and unit-label check passed")

# Uncomment after adding validation:
# plot_temperature([1, 2], [15.0])
# plot_temperature([[1, 2]], [[15.0, 16.0]])

# %% [markdown]
# Record your verification trail:
#
# - **Bounded prompt:** TODO
# - **Proposed lines accepted/rejected:** TODO
# - **Normal check:** TODO
# - **Adversarial check:** TODO
# - **Scientific decision Copilot did not own:** TODO
# - **Explain every final line in your own words:** TODO

# %% [markdown]
# ## 6. Safety boundary
#
# Do not paste or expose credentials, access tokens, personally identifiable information, unpublished/restricted data, reviewer material, or private code to an external service. Pause before running generated commands involving deletion, permissions, installation, network upload, credentials, or broad paths.
#
# A tool suggestion cannot authorize an action. If you cannot explain a command's target and consequence, do not run it.

# %% [markdown]
# ## Exit ticket
#
# Name one failure caught by your checks and one important failure they do **not** catch.
#
# - Caught: **TODO**
# - Not caught: **TODO**

# %% [markdown]
# ## Continuation lane
#
# Ask Copilot and one other model/tool for the same bounded validation task. Before seeing either answer, define three comparison criteria such as correctness on adversarial inputs, preservation of units/missing values, and size/readability of the change. Compare the proposals, test both, and document why you accepted neither, one, or a combination.
