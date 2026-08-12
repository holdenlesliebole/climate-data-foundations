# Course data workspace

Data acquisition is part of the course. You will obtain the Pier, MOP, NASA GISTEMP, and optional
Scripps Mauna Loa CO₂ files yourself, preserve each provider response, record where it came from,
and then load the local copy. The instructor recovery folder exists so a temporary network problem
does not prevent you from learning the rest of the workflow.

## Folder contract

```text
data/
├── manifest_template.yml   # copy to manifest.yml and fill in
├── raw/
│   ├── pier/               # downloaded ZIP plus its untouched CSV/XLS files
│   ├── mop/                # NetCDF response from your NCSS request
│   ├── climate/            # NASA GISTEMP and Scripps Mauna Loa CSV responses
│   └── era5/               # local copy of the instructor-prepared course subset
├── recovery/               # instructor-only fallback with the same expected bytes
└── processed/              # files your code creates; safe to recreate
```

- `raw/` means **as received**. Do not edit or overwrite these files.
- `processed/` is for cleaned tables, derived values, and exports.
- A recovery file should be copied into the appropriate `raw/` folder. Record
  `acquisition_method: instructor_recovery` in your manifest rather than pretending it came directly
  from the provider.
- Notebooks and scripts should use paths relative to the project, such as
  `data/raw/pier/filename.csv`. A path containing a student's username is not reproducible.
- Raw and recovery files are ignored by Git by default. The manifest, code, and small derived outputs
  are the reproducible record. Do not commit a data file unless its license and the course repository
  policy both allow it.

## Route 1: Scripps Pier archive

1. Open the [UC San Diego Library collection](https://library.ucsd.edu/dc/object/bb4003017c).
2. Identify the newest archive component. Record its title/date, DOI, citation, and license.
3. Use **Download file** and save the ZIP in `data/raw/pier/`.
4. List the ZIP contents before extracting it. Keep both the ZIP and extracted files unchanged.
5. Inspect the first 50–60 lines of the temperature CSV as text before calling `pandas.read_csv`.

The archive available on 2026-06-30 contained temperature and salinity in CSV and XLS formats. The
temperature CSV's real header was on line 47; the preceding text contained the citation, provider,
flag meanings, time-zone note, and archive date. Treat those details as data, not clutter. Discover
the header in the file you actually downloaded rather than assuming it will never change.

## Route 2: CDIP MOP subset

1. Open the [NCSS request page for near-Pier MOP site D0513](https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/MOP_alongshore/D0513_nowcast.nc/dataset.html).
2. Check the current time coverage; the nowcast file rolls forward.
3. Select a small interval and request `waveHs`, `waveTp`, `waveDp`, `waveFlagPrimary`, and
   `waveFlagSecondary` as NetCDF4.
4. Save the exact request URL and the response in `data/raw/mop/`. Do not analyze the live endpoint
   repeatedly.
5. Open the saved file with xarray and inspect dimensions, coordinates, attributes, units, valid
   ranges, flags, and missingness before plotting.

A seven-day, one-site response with those five variables was about 44 KB in the August 2026
preflight. File sizes and coverage can change, so verify rather than relying on that number.

## Route 3: annual Pier SST and global climate series

Friday's core relationship analysis reuses the Pier archive and adds NASA's global Land–Ocean
Temperature Index table.

1. Open the [NASA GISTEMP v4 data-download page](https://data.giss.nasa.gov/gistemp/data_v4.html).
2. Locate the CSV for global-mean monthly, seasonal, and annual means. Confirm that the values are
   anomalies relative to 1951–1980.
3. Preserve the response as `data/raw/climate/NASA_GISTEMP_global.csv`. The exact current URL used by
   the notebook is
   `https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts%2BdSST.csv`.
4. Inspect the title and header before loading. Record the access date because NASA updates and can
   revise the table.
5. Merge annual values by calendar year only after checking that both tables contain one row per
   retained year.

The continuation lane uses the [Scripps monthly in-situ Mauna Loa CO₂
record](https://scrippsco2.ucsd.edu/data/atmospheric-co2-data/sampling-station-records/mauna-loa-observatory-hawaii/).
Preserve the response as `data/raw/climate/Scripps_MLO_monthly_in_situ_CO2.csv`. Its provider CSV
contains a long preamble, a three-row header, measured and filled products, and `-99.99` missing
sentinels. Record which product you use. Scripps states that the data are subject to revision and
licenses its data under CC BY 4.0, so retain the citation and attribution with derived work.

## Route 4: CMS California Current System subsets

Notebook `045_3d_ccs.ipynb` uses a three-dimensional ocean biogeochemistry product. Each
published granule holds one variable at `time=48, depth=72, lat=171, lon=240` and is about
1.1 GB, so you never download a whole file. You request a bounded hyperslab and the server
sends only that.

### One-time access setup

1. Create a free account at [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov/).
2. Add one line to `~/.netrc`, creating the file if it does not exist:
   `machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD`
3. Restrict it: `chmod 600 ~/.netrc`.

Your password stays in that file. It must never appear in a notebook, a printed URL, or
the repository.

### Acquisition

1. Open the [dataset landing page](https://www.earthdata.nasa.gov/data/catalog/ges-disc-cms-oce-bgc-ccs-1)
   and the [OPeNDAP directory](https://acdisc.gesdisc.eosdis.nasa.gov/opendap/CMS/CMS_OCE_BGC_CCS.1/contents.html).
   Record the DOI, the citation, and the processing level.
2. Build a DAP4 constraint expression with `climate_course.ccs.dap4_subset_url`. Index
   ranges are inclusive at both ends, and every coordinate array must be sliced to match
   the data array or the server returns a 500.
3. Save the response unmodified in `data/raw/cms_ccs/`.
4. Record the exact request URL in your manifest. Each response also carries the request
   in its own `history` attribute, so the two can be compared.

The four course subsets total about 76 MB: three single-month volumes (`O2`, `NO3`, `pH`
for July 2010, 45 depth levels, roughly 5.9 MB each) and one twelve-month oxygen file
(2010, 37 depth levels, about 58 MB). `python scripts/fetch_cms_ccs.py` acquires all four
and is the recovery route after the troubleshooting checkpoint.

### Known traps, all verified during course development

- **Server-side striding does not work.** Asking for every second latitude fails with an
  internal `D4Maps` error. Thin the grid locally after downloading.
- **Large valid requests intermittently return HTTP 500.** Retry before rewriting the URL.
  `scripts/fetch_cms_ccs.py` retries three times.
- **The netCDF library's own DAP client is not portable.** On some machines it cannot
  authenticate against Earthdata Login at all. Course code therefore downloads over plain
  authenticated HTTPS using only the standard library.
- **The metadata contradicts the file** in three places: the declared latitude bounds are
  wider than the coordinate array; `WesternmostLatitude` and `EasternmostLatitude` hold
  longitudes on a 0–360 grid; and the fill value is spelled `_Fillvalue`, which is not the
  CF-standard `_FillValue` and so is ignored by xarray. Missing data are NaN in practice.
  The notebook treats all three as the lesson rather than as an obstacle.

These data are model output — a state estimate fitted to observations, not measurements.
Anything derived from them must say so. Cite as:

> Verdy, A. and M. Mazloff (2017), Ocean Biogeochemistry in the California Current System
> 2007-2010 L4 Monthly, Greenbelt, MD, USA, Goddard Earth Sciences Data and Information
> Services Center (GES DISC), doi:10.5067/G854SWM56S7H

## Manifest

Copy `manifest_template.yml` to `manifest.yml` and complete one entry per raw file. The manifest
answers four questions for your future self:

1. What did I obtain?
2. Where and when did it come from?
3. What subset or choices did I request?
4. Which exact local file did I analyze?

The data-loading notes show how to calculate a SHA-256 checksum once the file is present.
