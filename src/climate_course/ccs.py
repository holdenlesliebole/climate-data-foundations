"""Request building, loading, and derived surfaces for the CMS California Current subsets.

The published granules are one variable each and roughly 1.1 GB. Everything here works on
bounded OPeNDAP subsets saved under ``data/raw/cms_ccs/`` exactly as the server returned
them; the tidying that makes them convenient to plot happens on load, in code, so the
preserved response is never edited.
"""

from http.cookiejar import CookieJar
from pathlib import Path
import netrc
import urllib.request

import numpy as np
import pandas as pd
import xarray as xr


OPENDAP_ROOT = "https://acdisc.gesdisc.eosdis.nasa.gov/opendap/CMS/CMS_OCE_BGC_CCS.1"
EARTHDATA_HOST = "urs.earthdata.nasa.gov"
GRANULE_STEM = "cms_oce_bgc_ccs_i186_2007to2010_monthly"

RECORD_START_YEAR = 2007
RECORD_MONTHS = 48

# 60 mmol/m3 is the conventional hypoxia threshold for coastal ecosystems. The granules
# store oxygen in mol/m3, so the threshold is 0.06 in file units.
DEFAULT_HYPOXIC_THRESHOLD = 0.06

CITATION = (
    "Verdy, A. and M. Mazloff (2017), Ocean Biogeochemistry in the California Current "
    "System 2007-2010 L4 Monthly, Greenbelt, MD, USA, Goddard Earth Sciences Data and "
    "Information Services Center (GES DISC), doi:10.5067/G854SWM56S7H"
)


def earthdata_opener() -> urllib.request.OpenerDirector:
    """Return a URL opener that can authenticate against NASA Earthdata Login.

    Requesting a protected file redirects to Earthdata Login, which answers a Basic
    authentication challenge and then redirects back carrying a session cookie, so the
    opener needs both a password manager and a cookie jar. Credentials are read from
    ``~/.netrc`` and never appear in a notebook.

    Only the standard library is used on purpose. The netCDF library ships its own DAP
    client, but it is built against curl differently on different machines and fails to
    authenticate on some of them; a plain authenticated HTTPS GET is portable.
    """

    try:
        credentials = netrc.netrc().authenticators(EARTHDATA_HOST)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "No ~/.netrc found. See data/README.md route 4 for the one-time "
            "Earthdata Login setup."
        ) from error
    if credentials is None:
        raise ValueError(
            f"~/.netrc has no entry for machine {EARTHDATA_HOST}. "
            "See data/README.md route 4."
        )

    username, _, password = credentials
    manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, f"https://{EARTHDATA_HOST}", username, password)
    return urllib.request.build_opener(
        urllib.request.HTTPBasicAuthHandler(manager),
        urllib.request.HTTPCookieProcessor(CookieJar()),
    )


def month_index(year: int, month: int) -> int:
    """Return the integer time index for a calendar year and month.

    The record is monthly and starts in January 2007, but its ``time`` units are
    ``months since 2007-01-01``, which is not a unit the CF conventions can decode. The
    index therefore has to be computed rather than looked up.
    """

    if not 1 <= month <= 12:
        raise ValueError(f"month must be 1-12, got {month}")
    index = (year - RECORD_START_YEAR) * 12 + (month - 1)
    if not 0 <= index < RECORD_MONTHS:
        raise ValueError(
            f"{year}-{month:02d} is outside the 2007-2010 record (index {index})"
        )
    return index


def dap4_subset_url(
    variable: str,
    *,
    first_month: int,
    last_month: int,
    depth_levels: int,
    n_lat: int = 171,
    n_lon: int = 240,
) -> str:
    """Build the DAP4 URL for one bounded hyperslab, returned as a NetCDF4 file.

    Index ranges in a DAP4 constraint expression are inclusive at both ends, so a request
    for ``depth_levels`` levels ends at ``depth_levels - 1``. Coordinate arrays must be
    sliced to match the data array or the server cannot build a consistent file.

    Striding is deliberately not offered. The server rejects strided coordinate arrays
    with an internal error, so any thinning happens locally after download.
    """

    if last_month < first_month:
        raise ValueError("last_month must be greater than or equal to first_month")
    for name, value in (("first_month", first_month), ("last_month", last_month)):
        if not 0 <= value < RECORD_MONTHS:
            raise ValueError(f"{name} must be 0-{RECORD_MONTHS - 1}, got {value}")
    if not 1 <= depth_levels <= 72:
        raise ValueError(f"depth_levels must be 1-72, got {depth_levels}")

    time_range = f"{first_month}:{last_month}" if last_month > first_month else f"{first_month}"
    constraint = ";".join(
        [
            f"/{variable}[{time_range}][0:{depth_levels - 1}][0:{n_lat - 1}][0:{n_lon - 1}]",
            f"/time[{time_range}]",
            f"/depth[0:{depth_levels - 1}]",
            f"/lat[0:{n_lat - 1}]",
            f"/lon[0:{n_lon - 1}]",
        ]
    )
    return f"{OPENDAP_ROOT}/{GRANULE_STEM}_{variable}.nc.dap.nc4?dap4.ce={constraint}"


def load_ccs_subset(path: str | Path) -> xr.Dataset:
    """Open a preserved CMS response and apply the two conversions plotting needs.

    Longitude arrives on 0-360 and is converted to degrees east of Greenwich; ``time``
    arrives as an undecodable month count and is turned into real timestamps. Nothing
    else is altered, and the file on disk is not modified.
    """

    path = Path(path)
    with xr.open_dataset(path, decode_times=False) as opened:
        dataset = opened.load()

    missing = {"lat", "lon", "depth"}.difference(dataset.coords)
    if missing:
        raise ValueError(f"{path} is missing expected coordinates: {sorted(missing)}")

    if "time" in dataset.coords:
        months = np.asarray(dataset["time"].values, dtype=int)
        stamps = [
            pd.Timestamp(year=RECORD_START_YEAR, month=1, day=1)
            + pd.DateOffset(months=int(offset))
            for offset in months
        ]
        dataset = dataset.assign_coords(time=pd.DatetimeIndex(stamps))

    dataset = dataset.assign_coords(lon=(((dataset["lon"] + 180) % 360) - 180))
    return dataset.sortby("lon")


def hypoxic_boundary_depth(
    oxygen: xr.DataArray,
    *,
    threshold: float = DEFAULT_HYPOXIC_THRESHOLD,
) -> xr.DataArray:
    """Depth of the shallowest level at which oxygen first falls below ``threshold``.

    Returns NaN wherever the profile never crosses the threshold and wherever the column
    is land, so the resulting surface has honest holes rather than invented values. The
    result is the depth of the *first* crossing from above, which is the boundary an
    organism swimming down would meet, not the depth of the oxygen minimum.
    """

    required = ("depth", "lat", "lon")
    missing = [name for name in required if name not in oxygen.dims]
    if missing:
        raise ValueError(f"oxygen must have dims {required}; missing {missing}")
    if oxygen.sizes["depth"] < 2:
        raise ValueError("oxygen needs at least two depth levels")

    values = oxygen.transpose("depth", "lat", "lon").values
    depths = np.asarray(oxygen["depth"].values, dtype=float)

    below = values < threshold
    crosses = below.any(axis=0)
    first = np.argmax(below, axis=0)
    surface = np.where(crosses, depths[first], np.nan)
    surface = np.where(np.isnan(values).all(axis=0), np.nan, surface)

    return xr.DataArray(
        surface,
        dims=("lat", "lon"),
        coords={"lat": oxygen["lat"], "lon": oxygen["lon"]},
        name="hypoxic_boundary_depth",
        attrs={
            "long_name": f"Depth of the shallowest O2 < {threshold} mol/m3 level",
            "units": "m",
            "threshold_mol_m3": threshold,
        },
    )
