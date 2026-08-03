# Final-assignment data plan

The acquisition exercise and final analysis have different size needs. Keep both explicit.

## Pier option

Students use the original Pier archive acquired Monday. The temperature CSV is about 1.5 MB and
already contains the full surface and bottom history, so no second Pier download is necessary.

## MOP option

### In-class acquisition

- Site: `D0513`
- Window: seven recent days inside current nowcast coverage
- Variables: `waveHs`, `waveTp`, `waveDp`, `waveFlagPrimary`, `waveFlagSecondary`
- Purpose: learn request construction, local storage, xarray inspection, flags, and plotting

The seven-day development response contained 168 hourly observations and was about 44 KB.

### Assignment-sized acquisition

- Site: `D0513`
- Proposed window: `2026-01-01T00:00:00Z` through `2026-07-31T23:00:00Z`
- Same five variables and NetCDF4 format
- Suggested small question: compare January 2026 and July 2026 `waveHs` or `waveTp`
- Suggested filename: `data/raw/mop/D0513_2026-01-01_2026-07-31.nc`

The 2026-08-03 preflight returned 5,088 hourly observations in a 79,201-byte file, with all primary
flags equal to `good`. The size is small enough for every student to acquire. Recheck rolling nowcast
coverage and flags immediately before the course; choose replacement months if the course date or
source coverage changes.

Students construct this second request by changing the time parameters from the seven-day example,
save the exact URL and checksum in their manifest, and use the local response for the assignment.
Provide an authorized recovery copy only after the documented troubleshooting checkpoint.

## ERA5 option

ERA5 remains a prepared course subset unless credential/queue setup becomes a separate learning
objective. Its manifest must document the original request used by the instructor. It should not be
the only final-assignment route because students do not acquire it during the current core sequence.

## Release check

- [ ] Verify Pier redistribution/recovery terms.
- [ ] Recheck D0513 nowcast coverage and run both requests.
- [ ] Record expected filenames, sizes, dimensions, time coverage, variables, units, and checksums.
- [ ] Test downstream notebooks with the network disabled.
- [ ] Keep recovery files outside Git unless redistribution is explicitly permitted.
