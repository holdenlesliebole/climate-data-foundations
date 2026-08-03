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
# # Climate Data Foundations: setup check
#
# Run this notebook **before Monday**. It checks the course Python environment, project paths, plotting, CSV support, and NetCDF/xarray support without using the internet.
#
# A successful setup means this notebook runs from top to bottom and produces a small plot plus two temporary files in `data/processed/setup_check/`. It does not mean you are expected to understand all the code yet.

# %% [markdown]
# ## 1. Which Python am I using?
#
# The interpreter shown below should belong to the `climate-data-foundations` environment. If it points to another environment, select the correct notebook kernel in VS Code or JupyterLab before continuing.

# %%
import platform
import sys
from pathlib import Path

print("Python version:", sys.version.split()[0])
print("Python executable:", sys.executable)
print("Operating system:", platform.platform())

assert sys.version_info >= (3, 12), "Select the course Python 3.12 environment."

# %% [markdown]
# ## 2. Can Python find the course project?
#
# A working directory is the folder relative paths start from. This cell accepts either the project root or its `notebooks/` folder.

# %%
PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent

assert (PROJECT_ROOT / "README.md").exists(), (
    "Course README not found. Open the Climate_science_bootcamp folder as your project."
)

CHECK_DIR = PROJECT_ROOT / "data" / "processed" / "setup_check"
CHECK_DIR.mkdir(parents=True, exist_ok=True)

print("Current working directory:", Path.cwd())
print("Project root:", PROJECT_ROOT)
print("Temporary check folder:", CHECK_DIR.relative_to(PROJECT_ROOT))

# %% [markdown]
# ## 3. Are the core packages available?

# %%
import h5netcdf
import h5py
import matplotlib
import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pandas as pd
import scipy
import statsmodels
import xarray as xr

versions = {
    "numpy": np.__version__,
    "pandas": pd.__version__,
    "xarray": xr.__version__,
    "matplotlib": matplotlib.__version__,
    "scipy": scipy.__version__,
    "statsmodels": statsmodels.__version__,
    "netCDF4": netCDF4.__version__,
    "h5netcdf": h5netcdf.__version__,
    "h5py": h5py.__version__,
}

for package, version in versions.items():
    print(f"{package:>12}: {version}")

# %% [markdown]
# ## 4. Can NumPy, pandas, and plotting work together?
#
# This creates a tiny table in memory and plots it. You should see two temperature curves, one for the surface and one for the bottom.

# %%
dates = pd.date_range("2026-01-01", periods=7, freq="D")
surface = np.array([16.1, 16.3, 16.2, 16.5, np.nan, 16.7, 16.6])
bottom = np.array([15.8, 15.9, 16.0, 16.1, 16.1, 16.2, 16.3])

example = pd.DataFrame(
    {"surface_temperature_c": surface, "bottom_temperature_c": bottom},
    index=dates,
)
example.index.name = "date"
display(example)

ax = example.plot(marker="o", figsize=(8, 3))
ax.set(title="Setup check: example temperatures", xlabel="Date", ylabel="Temperature (°C)")
ax.grid(alpha=0.25)
plt.tight_layout()

# %% [markdown]
# It is normal for the surface line to have a gap: the example deliberately contains one missing value. If you see no figure or a red traceback, save the error and use the troubleshooting section below.

# %% [markdown]
# ## 5. Can this environment write and read a CSV?
#
# These are generated test files, so they belong in `processed/`, not `raw/`.

# %%
csv_path = CHECK_DIR / "setup_example.csv"
example.to_csv(csv_path, index_label="date")
reloaded_csv = pd.read_csv(csv_path, parse_dates=["date"], index_col="date")

pd.testing.assert_frame_equal(example, reloaded_csv, check_freq=False)
print("CSV round trip passed:", csv_path.relative_to(PROJECT_ROOT))

# %% [markdown]
# ## 6. Can xarray write and read NetCDF?
#
# This is the file format used for many climate and ocean datasets. The test includes variable units because labeled metadata are a major reason to use xarray.

# %%
example_xr = xr.Dataset(
    data_vars={
        "surface_temperature": ("time", surface, {"units": "degree_Celsius"}),
        "bottom_temperature": ("time", bottom, {"units": "degree_Celsius"}),
    },
    coords={"time": dates},
    attrs={"title": "Generated setup-check data"},
)

netcdf_path = CHECK_DIR / "setup_example.nc"
example_xr.to_netcdf(netcdf_path, engine="h5netcdf")
with xr.open_dataset(netcdf_path, engine="h5netcdf") as opened:
    reloaded_xr = opened.load()

xr.testing.assert_identical(example_xr, reloaded_xr)
print("NetCDF round trip passed:", netcdf_path.relative_to(PROJECT_ROOT))
reloaded_xr

# %% [markdown]
# ## 7. Final automated check

# %%
checks = {
    "course project found": (PROJECT_ROOT / "README.md").exists(),
    "Python 3.12+": sys.version_info >= (3, 12),
    "expected table shape": example.shape == (7, 2),
    "missing value preserved": reloaded_csv.isna().sum().sum() == 1,
    "CSV round trip": csv_path.exists(),
    "NetCDF round trip": netcdf_path.exists(),
    "NetCDF units preserved": reloaded_xr.surface_temperature.attrs["units"] == "degree_Celsius",
}

for name, passed in checks.items():
    print(("PASS" if passed else "FAIL"), "-", name)

assert all(checks.values()), "At least one setup check failed. See the result above."
print("\nSetup check complete. You are ready for the course.")

# %% [markdown]
# ## Troubleshooting without guessing
#
# If a cell fails:
#
# 1. Stop at the **first** red traceback. Later failures may be consequences.
# 2. Read the final line of the traceback and note the cell number.
# 3. Copy the Python executable and working-directory output from sections 1–2.
# 4. Compare the symptom below, then contact the setup clinic/instructors with those details.
#
# | Symptom | Likely cause | First check |
# |---|---|---|
# | `ModuleNotFoundError` | wrong kernel or incomplete environment | Does `sys.executable` belong to `climate-data-foundations`? |
# | `Course README not found` | wrong project/working directory | Open the whole course folder, not only the notebook file |
# | NetCDF engine error | `h5netcdf`/HDF5 installation problem | Save the complete traceback and package versions |
# | Plot does not appear | kernel or notebook rendering problem | Restart the kernel and rerun from the top |
# | Permission error writing the check file | project is in a read-only/protected location | Move your course copy to a normal documents folder |
#
# Do not repeatedly reinstall packages into different environments. That usually makes the diagnosis harder.

# %% [markdown]
# ## What to send an instructor
#
# - A screenshot or copy of the **first** traceback
# - Your operating system
# - The printed Python executable
# - The printed current working directory
# - Which checks passed before the failure
#
# Do not send passwords, tokens, or other credentials.
