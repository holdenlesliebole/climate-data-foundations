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
# # Reference: from source to figure—Scripps Pier temperature
#
# This completed reference begins with the original archive in `data/raw/pier/`. It preserves the provider's metadata preamble, discovers the table header, loads the first nine meaningful columns, constructs dates, checks structure/flags/missingness, and makes a bounded figure.
#
# Source: [UC San Diego Library, Shore Stations Program—La Jolla, Scripps Pier](https://library.ucsd.edu/dc/object/bb4003017c), DOI [10.6075/J06T0K0M](https://doi.org/10.6075/J06T0K0M). Recheck the current component and citation in the file you acquired.

# %%
from pathlib import Path
from zipfile import ZipFile
import hashlib

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "reference":
    PROJECT_ROOT = PROJECT_ROOT.parent
assert (PROJECT_ROOT / "README.md").exists()
PIER_RAW = PROJECT_ROOT / "data" / "raw" / "pier"

# %% [markdown]
# ## Inspect and extract the acquired archive
#
# The archive is a provider response and remains unchanged in `raw/`. Listing it first confirms its contents and formats before extraction.

# %%
zip_files = sorted(PIER_RAW.glob("*.zip"))
assert zip_files, "Download the current Pier ZIP into data/raw/pier/."
PIER_ZIP = zip_files[-1]

with ZipFile(PIER_ZIP) as archive:
    members = archive.namelist()
    print("Archive contents:", *members, sep="\n - " )
    targets = [PIER_RAW / name for name in members]
    if any(path.exists() for path in targets):
        print("At least one extracted file is already present; not overwriting raw files.")
    else:
        archive.extractall(PIER_RAW)

# %% [markdown]
# The June 2026 component contained temperature and salinity in CSV and XLS. CSV is a transparent text representation well suited to pandas; XLS is useful for spreadsheet users but adds a binary/container reader to the workflow. Future components may differ, so the code inspects rather than assumes.

# %% [markdown]
# ## Discover the real table header

# %%
temperature_files = sorted(PIER_RAW.glob("LaJolla_TEMP_*.csv"))
assert temperature_files, "No extracted temperature CSV found."
temperature_path = temperature_files[-1]

lines = temperature_path.read_text(encoding="utf-8-sig").splitlines()
for line_number, line in enumerate(lines[:55], start=1):
    print(f"{line_number:>3}: {line}")

# %%
header_matches = [
    index for index, line in enumerate(lines)
    if line.startswith("YEAR,MONTH,DAY")
]
assert len(header_matches) == 1, f"Expected one header; found {header_matches}"
header_index = header_matches[0]
print("Header line:", header_index + 1)

# %% [markdown]
# In the June 2026 file, the table header is on human-readable line 47. The preceding lines contain the archive date, citation, provider, uncertainty flag definitions, and a time-zone caveat. A tidy derivative without that preamble would require a separate metadata record to preserve those facts.

# %% [markdown]
# ## Load with explicit parsing decisions

# %%
pier = pd.read_csv(
    temperature_path,
    skiprows=header_index,
    usecols=range(9),
    na_values=["NaN"],
)
date_parts = pier[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower)
pier["date"] = pd.to_datetime(date_parts, errors="coerce")
pier.head()

# %% [markdown]
# `skiprows=header_index` skips only the preamble; pandas then uses the discovered line as column names. `usecols=range(9)` omits trailing empty CSV fields. `errors='coerce'` makes an unparseable date visibly missing rather than guessing.

# %% [markdown]
# ## Validate structure and scientific meaning

# %%
expected_columns = {
    "YEAR", "MONTH", "DAY", "TIME_PST", "TIME_FLAG",
    "SURF_TEMP_C", "SURF_FLAG", "BOT_TEMP_C", "BOT_FLAG",
}
assert expected_columns.issubset(pier.columns)
assert pier["date"].notna().any()

print("shape:", pier.shape)
print("coverage:", pier.date.min(), "to", pier.date.max())
print("duplicate dates:", pier.date.duplicated().sum())
print("date parse failures:", pier.date.isna().sum())
display(pier[["SURF_TEMP_C", "BOT_TEMP_C"]].describe())
display(pier[["SURF_TEMP_C", "BOT_TEMP_C"]].isna().mean().rename("missing_fraction"))

# %%
print("Surface flags")
display(pier.SURF_FLAG.value_counts(dropna=False).sort_index())
print("Bottom flags")
display(pier.BOT_FLAG.value_counts(dropna=False).sort_index())

# %% [markdown]
# One row represents a calendar date, with time-of-collection available only for part of the record. `SURF_TEMP_C` is the approximately 0.5 m measurement and `BOT_TEMP_C` is near 5 m. The archive documents `0` as good and `1`–`5` as distinct uncertainty or collection conditions. Missing bottom values are expected before the bottom record begins and should not be replaced with zero.

# %% [markdown]
# ## A bounded first figure

# %%
start, end = "2025-01-01", "2025-06-30"
window = pier.loc[pier.date.between(start, end)].copy()
assert not window.empty

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(window.date, window.SURF_TEMP_C, label="Surface (~0.5 m)", lw=1.5)
ax.plot(window.date, window.BOT_TEMP_C, label="Near bottom (~5 m)", lw=1.5)
ax.set(
    title=f"Scripps Pier temperature, {start} to {end}",
    xlabel="Date", ylabel="Temperature (°C)",
)
ax.legend()
ax.grid(alpha=0.25)
fig.text(0.99, -0.02, "Source: UC San Diego Shore Stations Program", ha="right", fontsize=8)
fig.tight_layout()


# %% [markdown]
# The surface and near-bottom series generally move together during this selected interval, while their separation changes over time. This descriptive plot does not establish a cause; missing observations, flagged conditions, different sampling depths, and the once-daily sampling context limit interpretation.

# %% [markdown]
# ## Provenance and a reusable loader

# %%
def sha256(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

print(PIER_ZIP.relative_to(PROJECT_ROOT), sha256(PIER_ZIP))
print(temperature_path.relative_to(PROJECT_ROOT), sha256(temperature_path))


# %%
def load_pier_temperature(path):
    """Load an original Shore Stations Pier temperature CSV with its flags."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith("YEAR,MONTH,DAY")]
    if len(matches) != 1:
        raise ValueError(f"Expected one Pier header; found {matches}")

    frame = pd.read_csv(path, skiprows=matches[0], usecols=range(9), na_values=["NaN"])
    missing_columns = expected_columns.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing expected columns: {sorted(missing_columns)}")

    date_parts = frame[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower)
    frame["date"] = pd.to_datetime(date_parts, errors="coerce")
    if not frame["date"].notna().any():
        raise ValueError("No dates could be parsed.")
    return frame

loaded_again = load_pier_temperature(temperature_path)
pd.testing.assert_frame_equal(pier, loaded_again)
print("Loader check passed.")

# %% [markdown]
# The loader catches a missing/duplicated header, missing expected columns, and a total date-parse failure. It cannot prove that the provider's measurements are unbiased, that every plausible value is correct, or that a chosen analysis answers a sensible question. Code checks support scientific judgment; they do not replace it.
