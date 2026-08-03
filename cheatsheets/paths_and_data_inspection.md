# Paths and data inspection: first-response sheet

Use this when a file will not load or a dataset is unfamiliar. Do not change five things at once.

## 1. Locate yourself and the file

```python
from pathlib import Path

print("working directory:", Path.cwd())
path = Path("data/raw/pier/example.csv")
print("full path:", path.resolve())
print("exists:", path.exists())
print("suffix:", path.suffix)
print("bytes:", path.stat().st_size if path.exists() else "file not found")
```

Build portable paths with `/`:

```python
PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name in {"notebooks", "reference"}:
    PROJECT_ROOT = PROJECT_ROOT.parent

path = PROJECT_ROOT / "data" / "raw" / "pier" / "filename.csv"
```

Avoid paths containing your username or `Downloads` in submitted code.

## 2. Inspect bytes/text before parsing

```python
print(path.read_bytes()[:16])

lines = path.read_text(encoding="utf-8-sig").splitlines()
for number, line in enumerate(lines[:20], start=1):
    print(f"{number:>3}: {line}")
```

Ask: Is this actually CSV/NetCDF, or did I save an HTML error page? Where is the real header? What
delimiter and missing-value marker are used?

## 3. Load a CSV deliberately

```python
import pandas as pd

frame = pd.read_csv(
    path,
    skiprows=0,          # change only after inspecting the file
    na_values=["NaN"],
)
```

First inspection:

```python
display(frame.head())
print(frame.shape)
print(frame.columns.tolist())
frame.info()
display(frame.describe(include="all"))
display(frame.isna().mean().sort_values(ascending=False))
```

For date parts:

```python
date_parts = frame[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower)
frame["date"] = pd.to_datetime(date_parts, errors="coerce")
print(frame["date"].min(), frame["date"].max())
```

## 4. Open a local NetCDF with xarray

```python
import xarray as xr

with xr.open_dataset(path) as opened:
    dataset = opened.load()

print(dataset)
print(dataset.sizes)
print(dataset.coords)
print(dataset.data_vars)
print(dataset.attrs)
```

Inspect one variable before using it:

```python
name = "waveHs"
print(dataset[name].dims)
print(dataset[name].attrs)
print(dataset[name].min().item(), dataset[name].max().item())
print(dataset[name].isnull().mean().item())
```

Select by coordinate label when possible:

```python
subset = dataset.sel(time=slice("2026-07-01", "2026-07-07"))
```

## 5. The six inspection questions

1. **Source:** Who produced the values? Measured, modeled, or derived?
2. **Shape:** What does one row/index position represent?
3. **Coordinates/time:** Where and when, in which time zone/calendar?
4. **Variables/units:** What quantity, unit, sign, depth, and directional convention?
5. **Missingness:** How much, where, and could it be patterned?
6. **Quality:** What do flags/valid ranges mean, and what rule will you apply?

## 6. Record provenance

At minimum:

```text
provider + dataset title
landing page and/or exact request URL
archive/version/component date
access date/time
requested site, dates, variables, and format
project-relative raw filename
browser/script/recovery acquisition method
```

Do not overwrite a raw file. Record recovery use honestly; it is not a penalty.

## Common symptoms

| Symptom | Inspect first | Likely cause |
|---|---|---|
| `FileNotFoundError` | `Path.cwd()`, `path.resolve()`, `exists()` | wrong project folder or filename |
| Strange CSV columns | first 20–60 text lines | metadata preamble, delimiter, or wrong header |
| xarray cannot open `.nc` | file size and first bytes | HTML error response or incomplete download |
| Empty selection | coordinate values and time zone | requested labels outside coverage |
| Plausible but wrong magnitude | units and fill values | Kelvin/Celsius or encoded missing value |
| Directional mean looks wrong | convention and 0°/360° | ordinary statistics applied to circular data |
