# Course data workspace

Data acquisition is part of the course. You will obtain the Pier and MOP files yourself, preserve
the provider's response, record where it came from, and then load the local copy. The instructor
recovery folder exists so a temporary network problem does not prevent you from learning the rest of
the workflow.

## Folder contract

```text
data/
├── manifest_template.yml   # copy to manifest.yml and fill in
├── raw/
│   ├── pier/               # downloaded ZIP plus its untouched CSV/XLS files
│   └── mop/                # NetCDF response from your NCSS request
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

## Manifest

Copy `manifest_template.yml` to `manifest.yml` and complete one entry per raw file. The manifest
answers four questions for your future self:

1. What did I obtain?
2. Where and when did it come from?
3. What subset or choices did I request?
4. Which exact local file did I analyze?

The data-loading notes show how to calculate a SHA-256 checksum once the file is present.
