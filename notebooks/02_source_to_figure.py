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
# # From source to figure: Scripps Pier temperature
#
# In this notebook you will acquire a public research archive, preserve the raw files, discover how the CSV is structured, load it with pandas, validate its contents, and make a first scientific figure.
#
# The goal is not merely to make `read_csv` run. By the end, another student should be able to tell **what you downloaded, where it came from, what choices you made, and which local file your plot used**.
#
# Core path: source → download → inspect archive → inspect text → load → validate → plot → record provenance.

# %% [markdown]
# ## 0. Set up the project paths
#
# Run this notebook from the course project in VS Code. We build paths from the project root so the notebook does not depend on anyone's username or operating system.

# %%
from pathlib import Path
from zipfile import ZipFile
import hashlib

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent

assert (PROJECT_ROOT / "README.md").exists(), (
    "Open the Climate_science_bootcamp project folder, then rerun this cell."
)

PIER_RAW = PROJECT_ROOT / "data" / "raw" / "pier"
PIER_RAW.mkdir(parents=True, exist_ok=True)
print("Project root:", PROJECT_ROOT)
print("Pier raw folder:", PIER_RAW)

# %% [markdown]
# ## 1. Find and acquire the authoritative data
#
# With your partner:
#
# 1. Open the [UC San Diego Library Scripps Pier collection](https://library.ucsd.edu/dc/object/bb4003017c).
# 2. Identify the newest archive component. Do not assume the first date you see describes the observations.
# 3. Find its archive date, DOI/citation, file format, license, and stated time coverage.
# 4. Choose **Download file** and save or move the ZIP into `data/raw/pier/`.
# 5. Do not open and resave the CSV in a spreadsheet program. `raw` means as received.
#
# Record before continuing:
#
# - Archive component/title: **TODO**
# - Provider: **TODO**
# - DOI: **TODO**
# - Access date/time: **TODO**
# - One method or sampling detail that matters: **TODO**

# %%
# What ZIP files are in the raw folder?
zip_files = sorted(PIER_RAW.glob("*.zip"))
zip_files

# %%
assert zip_files, (
    "No ZIP found. Download the newest Pier archive into data/raw/pier/ first."
)

# If there is more than one ZIP, inspect the list and choose deliberately.
PIER_ZIP = zip_files[-1]
print(PIER_ZIP.name, f"({PIER_ZIP.stat().st_size / 1_000_000:.2f} MB)")

# %% [markdown]
# ### Predict
#
# Before running the next cell, write down what files you expect inside the archive. Which variable(s) and format(s) do you expect?
#
# **Prediction:** TODO

# %%
with ZipFile(PIER_ZIP) as archive:
    members = archive.namelist()

print("Archive contents:")
for member in members:
    print(" -", member)

# %% [markdown]
# What matched your prediction? What surprised you? Why might the provider include both CSV and XLS?
#
# **Answer:** TODO

# %%
# Extract once. Refuse to overwrite a file that is already present.
with ZipFile(PIER_ZIP) as archive:
    targets = [PIER_RAW / name for name in archive.namelist()]
    existing = [path for path in targets if path.exists()]
    if existing:
        print("Already present; not overwriting:")
        for path in existing:
            print(" -", path.name)
    else:
        archive.extractall(PIER_RAW)
        print("Extracted", len(targets), "files.")

# %% [markdown]
# ## 2. Inspect before loading
#
# A `.csv` suffix tells us the general format, not which row is the header or what the columns mean. We will read a small part as plain text before asking pandas to interpret it.

# %%
temperature_files = sorted(PIER_RAW.glob("LaJolla_TEMP_*.csv"))
assert temperature_files, "No temperature CSV found after extraction."

# If several archives are present, replace this choice with the file you intend to analyze.
temperature_path = temperature_files[-1]
print(temperature_path.name, f"({temperature_path.stat().st_size:,} bytes)")

# %%
lines = temperature_path.read_text(encoding="utf-8-sig").splitlines()
for line_number, line in enumerate(lines[:55], start=1):
    print(f"{line_number:>3}: {line}")

# %% [markdown]
# With your partner, locate:
#
# - the real table header;
# - temperature units;
# - the meaning of `NaN`;
# - the flag meanings;
# - the time-zone note;
# - one fact that would be lost if someone handed you only a tidy DataFrame.
#
# **Notes:** TODO

# %%
# Find the header from its content instead of assuming it is always on today's line number.
header_matches = [
    index for index, line in enumerate(lines)
    if line.startswith("YEAR,MONTH,DAY")
]
assert len(header_matches) == 1, f"Expected one header, found {header_matches}"
header_index = header_matches[0]
print("Zero-based header index:", header_index)
print("Human-readable line number:", header_index + 1)

# %% [markdown]
# ### Predict
#
# What would happen if we ran `pd.read_csv(temperature_path)` without `skiprows`? What do you expect the first three data rows to represent?
#
# **Prediction:** TODO

# %% [markdown]
# ## 3. Load with an explicit decision

# %%
pier = pd.read_csv(
    temperature_path,
    skiprows=header_index,
    usecols=range(9),  # ignore trailing empty columns
    na_values=["NaN"],
)

date_parts = pier[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower)
pier["date"] = pd.to_datetime(date_parts, errors="coerce")
pier.head()

# %% [markdown]
# ## 4. Validate before plotting
#
# A successful load means only that pandas created an object. It does not mean we loaded the intended rows, interpreted dates correctly, or understood the flags.

# %%
expected_columns = {
    "YEAR", "MONTH", "DAY", "TIME_PST", "TIME_FLAG",
    "SURF_TEMP_C", "SURF_FLAG", "BOT_TEMP_C", "BOT_FLAG",
}
assert expected_columns.issubset(pier.columns)
assert pier["date"].notna().any()

print("Shape:", pier.shape)
print("Coverage:", pier["date"].min(), "to", pier["date"].max())
print("Duplicate dates:", pier["date"].duplicated().sum())
print("Date parse failures:", pier["date"].isna().sum())
pier.info()

# %%
temperature_columns = ["SURF_TEMP_C", "BOT_TEMP_C"]
print("Temperature summary (°C):")
display(pier[temperature_columns].describe())

print("Missing fraction:")
display(pier[temperature_columns].isna().mean().rename("missing_fraction"))

print("Surface flags:")
display(pier["SURF_FLAG"].value_counts(dropna=False).sort_index())

print("Bottom flags:")
display(pier["BOT_FLAG"].value_counts(dropna=False).sort_index())

# %% [markdown]
# Answer the six inspection questions:
#
# 1. **Source:** Who produced and archived the data?
# 2. **Shape:** What does one row represent?
# 3. **Time:** What is the coverage, sampling pattern, and time zone?
# 4. **Variables/units:** What do surface and bottom mean, and what are the units?
# 5. **Missingness:** Which series has more missing values, and is missingness constant over time?
# 6. **Quality:** What do the flags mean, and what will you do with them in this first plot?
#
# **Answers:** TODO

# %% [markdown]
# ## 5. Make a bounded first figure
#
# Choose a period with both surface and bottom observations. Start with a few months to a year so individual observations remain visible.

# %%
# TODO: change this window after inspecting the time coverage.
start = "2025-01-01"
end = "2025-06-30"

window = pier.loc[pier["date"].between(start, end)].copy()
assert not window.empty, "Your selected window contains no rows."

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(window["date"], window["SURF_TEMP_C"], label="Surface (~0.5 m)", lw=1.5)
ax.plot(window["date"], window["BOT_TEMP_C"], label="Near bottom (~5 m)", lw=1.5)
ax.set(
    title=f"Scripps Pier temperature, {start} to {end}",
    xlabel="Date",
    ylabel="Temperature (°C)",
)
ax.legend()
ax.grid(alpha=0.25)
fig.text(0.99, -0.02, "Source: UC San Diego Shore Stations Program", ha="right", fontsize=8)
fig.tight_layout()


# %% [markdown]
# ### Caption and limitation
#
# Write two sentences: one describes a visible feature without claiming a cause; the other names a data limitation or decision involving missing values, flags, sampling, or depth.
#
# **Caption:** TODO

# %% [markdown]
# ## 6. Record the exact local input
#
# The archive title tells us which published component we intended to use. A checksum identifies the exact bytes on this computer.

# %%
def sha256(path, chunk_size=1024 * 1024):
    """Return the SHA-256 checksum of a file without loading it all at once."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

print("ZIP:", PIER_ZIP.relative_to(PROJECT_ROOT))
print("ZIP SHA-256:", sha256(PIER_ZIP))
print("CSV:", temperature_path.relative_to(PROJECT_ROOT))
print("CSV SHA-256:", sha256(temperature_path))


# %% [markdown]
# Copy `data/manifest_template.yml` to `data/manifest.yml` and complete the Pier entry. If you used the instructor recovery file, record `acquisition_method: instructor_recovery`. That is honest provenance, not a penalty.
#
# ## Exit ticket
#
# What scientifically useful information would have been lost if you had received only an already-loaded, tidy DataFrame? Give one concrete example from this archive.
#
# **Answer:** TODO

# %% [markdown]
# ## Continuation lane
#
# Write `load_pier_temperature(path)` below. It should discover the header, load the first nine columns, create `date`, check the expected columns, and return the DataFrame. Test it on the downloaded file. Then explain one failure your checks catch and one they do not.

# %%
def load_pier_temperature(path):
    """Load an original Shore Stations Pier temperature CSV."""
    # TODO: implement the same discovery, loading, date parsing, and checks used above.
    raise NotImplementedError

# loaded_again = load_pier_temperature(temperature_path)
# pd.testing.assert_frame_equal(pier, loaded_again)
