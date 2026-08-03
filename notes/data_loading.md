# Data loading is a research workflow

`pandas.read_csv` and `xarray.open_dataset` are important, but they are not the beginning. A
reproducible data-loading workflow connects a scientific source to a verified local object:

```text
authoritative source → choose a subset → acquire → preserve raw → record provenance
                     → load locally → inspect structure → check scientific meaning
```

The landing page, download/request URL, local file path, and in-memory Python object are four
different things. Many frustrating errors come from confusing them.

## The seven-step habit

1. **Find the authoritative source.** Who created or curates the data? Read the documentation,
   version/date, citation, license, methods, and known limitations.
2. **Choose the smallest useful input.** Decide variables, site, time window, format, and resolution
   before downloading. Start small enough to inspect.
3. **Acquire deliberately.** A browser download is appropriate for an occasional versioned archive;
   a parameterized script is better for repeatable subsets.
4. **Preserve the provider response.** Save it in `data/raw/`, use an informative name, and never
   silently overwrite or hand-edit it.
5. **Record provenance.** Save the landing page or exact request URL, provider, access time, archive
   version, selection, local filename, terms, and later a checksum.
6. **Load the local file.** Acquisition code and analysis code should be separable. Once the bytes
   are local, the analysis should not depend on the network.
7. **Validate before analyzing.** Inspect shape, variables, coordinates, units, ranges, missingness,
   flags, and a few actual values. Ask whether the object matches the scientific story.

## Relative paths and the project root

Run the course notebooks from the repository root. This small setup also works if VS Code starts a
notebook from the `notebooks/` folder:

```python
from pathlib import Path

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent

assert (PROJECT_ROOT / "README.md").exists(), "Open the course project folder first."
RAW = PROJECT_ROOT / "data" / "raw"
```

Prefer `PROJECT_ROOT / "data" / "raw" / ...` to a machine-specific path such as
`/Users/name/Downloads/file.csv`.

## Example A: manually acquire and load the Pier archive

Start at the [UC San Diego Library Scripps Pier collection](https://library.ucsd.edu/dc/object/bb4003017c).
Select the newest component, record its archive date and DOI, and use **Download file**. Move the ZIP
to `data/raw/pier/` without renaming its contents.

### 1. List before extracting

```python
from zipfile import ZipFile

pier_dir = RAW / "pier"
zip_files = sorted(pier_dir.glob("*.zip"))
assert zip_files, "Download the Pier ZIP into data/raw/pier/ first."

pier_zip = zip_files[-1]
with ZipFile(pier_zip) as archive:
    members = archive.namelist()

members
```

Ask: Are these the variables and formats you expected? Is there more than one representation of the
same data? Keep the ZIP. Extract once, without overwriting an existing file:

```python
with ZipFile(pier_zip) as archive:
    targets = [pier_dir / name for name in archive.namelist()]
    existing = [path for path in targets if path.exists()]
    if existing:
        print("Already present; not overwriting:", existing)
    else:
        archive.extractall(pier_dir)
```

### 2. Inspect the file as text

Do not guess that row 1 is the table header.

```python
temperature_files = sorted(pier_dir.glob("LaJolla_TEMP_*.csv"))
assert temperature_files, "No Pier temperature CSV found after extraction."
temperature_path = temperature_files[-1]

lines = temperature_path.read_text(encoding="utf-8-sig").splitlines()
for line_number, line in enumerate(lines[:55], start=1):
    print(f"{line_number:>3}: {line}")
```

Find the true header instead of permanently hard-coding its current position:

```python
header_matches = [
    index for index, line in enumerate(lines)
    if line.startswith("YEAR,MONTH,DAY")
]
assert len(header_matches) == 1, f"Expected one header, found {header_matches}"
header_index = header_matches[0]  # zero-based; 46 means human-readable line 47
```

### 3. Load with an explicit decision

The archive CSV includes trailing empty columns. Load the first nine meaningful columns and assemble
a date from its three date fields:

```python
import pandas as pd

pier = pd.read_csv(
    temperature_path,
    skiprows=header_index,
    usecols=range(9),
    na_values=["NaN"],
)

date_parts = pier[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower)
pier["date"] = pd.to_datetime(date_parts, errors="coerce")
pier.head()
```

### 4. Validate structure and meaning

```python
expected = {
    "YEAR", "MONTH", "DAY", "TIME_PST", "TIME_FLAG",
    "SURF_TEMP_C", "SURF_FLAG", "BOT_TEMP_C", "BOT_FLAG",
}
assert expected.issubset(pier.columns)
assert pier["date"].notna().any()

print("shape:", pier.shape)
print("coverage:", pier["date"].min(), "to", pier["date"].max())
print("missing fraction:")
print(pier[["SURF_TEMP_C", "BOT_TEMP_C"]].isna().mean())
print("surface flags:")
print(pier["SURF_FLAG"].value_counts(dropna=False).sort_index())
print(pier[["SURF_TEMP_C", "BOT_TEMP_C"]].describe())
```

The current file documents `0` as good data and `1`–`5` as different uncertainty or collection
conditions. Missing data are not necessarily bad data, and an unusual value is not automatically an
error. Preserve the original flags and explain any filtering.

## Example B: programmatically acquire and load a CDIP MOP subset

Start at the [D0513 NCSS request page](https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/MOP_alongshore/D0513_nowcast.nc/dataset.html).
Read the current coverage and variable attributes. The following pattern makes each choice visible;
the dates are an example and must lie inside the current rolling coverage.

```python
from urllib.parse import urlencode
from urllib.request import urlretrieve

base_url = (
    "https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/"
    "MOP_alongshore/D0513_nowcast.nc"
)

variables = [
    "waveHs", "waveTp", "waveDp",
    "waveFlagPrimary", "waveFlagSecondary",
]

parameters = [("var", variable) for variable in variables]
parameters += [
    ("stns", "all"),
    ("time_start", "2026-07-01T00:00:00Z"),
    ("time_end", "2026-07-07T23:00:00Z"),
    ("timeStride", "1"),
    ("accept", "netcdf4"),
]

request_url = f"{base_url}?{urlencode(parameters)}"
destination = RAW / "mop" / "D0513_2026-07-01_2026-07-07.nc"
print(request_url)
print(destination)
```

Predict what will happen before running the request. Then refuse a silent overwrite:

```python
destination.parent.mkdir(parents=True, exist_ok=True)
if destination.exists():
    raise FileExistsError(f"Raw file already exists: {destination}")

urlretrieve(request_url, destination)
assert destination.stat().st_size > 0
print(f"Saved {destination.stat().st_size:,} bytes")
```

If this fails, do not immediately change five things. Read the error and check, in order: network,
current dataset coverage, variable spelling, encoded URL, destination folder, and whether the server
returned an error page instead of NetCDF. After the class troubleshooting checkpoint, use the
recovery copy if necessary and record that route in the manifest.

Open the saved local response, not the remote URL:

```python
import xarray as xr

with xr.open_dataset(destination) as remote_file:
    mop = remote_file.load()

print(mop)
for name in variables:
    print(name, mop[name].attrs)
```

For the preflighted file, `waveHs` is significant wave height in meters, `waveTp` is peak period in
seconds, and `waveDp` uses degrees true with a “wave from” convention. Inspect the file you acquired
instead of copying those facts into code. Primary flag values distinguish good, not evaluated,
questionable, bad, and missing; secondary flags describe additional model/input conditions.

Direction is circular: 1° and 359° are close. Do not take an ordinary mean of peak direction across
the 0°/360° boundary.

## A checksum identifies the exact bytes

Filenames can be reused. A SHA-256 digest provides evidence that two people have the same file:

```python
import hashlib

def sha256(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

print(sha256(destination))
```

A checksum does not prove the data are scientifically correct. It only identifies the bytes you
used.

## Fast diagnostic table

| Symptom | First thing to inspect | Common cause |
|---|---|---|
| `FileNotFoundError` | `Path.cwd()` and `path.exists()` | wrong working directory or filename |
| Every column is named `Unnamed...` | first 50 text lines and delimiter | metadata preamble or wrong header |
| CSV parser error | raw lines around the reported row | wrong delimiter/header or malformed row |
| xarray cannot identify the file | file size and first response bytes | an HTML error page was saved as `.nc` |
| Empty time selection | dataset coverage, timezone, and coordinate values | request/selection outside coverage |
| Plausible plot with wrong magnitude | variable attributes and units | Kelvin/Celsius, meters/centimeters, or fill values |
| Strange directional average | circular plot or wraparound | ordinary statistics applied to angles |

## Using Copilot without outsourcing judgment

A useful bounded prompt is: “Given these exact column names, write a check that dates are increasing
and temperature units are Celsius. Do not drop or fill any values.” Then verify each condition
yourself. Never paste credentials, restricted data, or unpublished information into an external
service, and never accept generated acquisition code that silently overwrites raw files.

## Stop-and-check questions

Before analysis, you should be able to answer:

- Who produced this dataset, and what exactly is measured or modeled?
- Which version, site, dates, variables, and file format did I obtain?
- Can I point to the exact raw file and repeat the acquisition?
- What are the dimensions/columns, units, missing-value rules, and quality flags?
- What is one value or range I can check for plausibility?
- If the network disappears now, can the analysis rerun from the local file?
