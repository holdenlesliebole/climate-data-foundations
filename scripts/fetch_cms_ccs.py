"""Acquire the bounded CMS California Current System subsets used by notebook 045.

The published granules are one variable each and about 1.1 GB apiece, which is far too
large for a classroom. This script asks the OPeNDAP server for only the hyperslabs the
lesson needs and saves each response exactly as it arrives, so ``data/raw/cms_ccs/``
holds provider files rather than edited ones. Longitude conversion and time decoding
happen later, on load, in ``climate_course.ccs.load_ccs_subset``.

Four requests, about 76 MB in total:

  2010-07  O2, NO3, pH   45 levels (to 1012 m)   ~5.9 MB each
  2010     O2, 12 months 37 levels (to 600 m)    ~58 MB

Access needs a NASA Earthdata Login in ``~/.netrc`` for machine ``urs.earthdata.nasa.gov``.
The download deliberately uses only the standard library: the netCDF library's own DAP
client is built against curl differently on different machines and fails to authenticate
on some of them, while a plain authenticated HTTPS GET works everywhere we have tried.

Instructors run this to build recovery copies. Students construct the same requests in
the notebook; this file is the fallback after the troubleshooting checkpoint.
"""

from pathlib import Path
import hashlib
import html
import re
import sys
import time
import urllib.error

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from climate_course.ccs import (  # noqa: E402
    dap4_subset_url,
    earthdata_opener,
    month_index,
)

RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "cms_ccs"

VOLUME_YEAR, VOLUME_MONTH = 2010, 7
VOLUME_VARIABLES = ("O2", "NO3", "pH")
VOLUME_LEVELS = 45  # depth[44] = 1012.5 m

SEASONAL_YEAR = 2010
SEASONAL_VARIABLE = "O2"
SEASONAL_LEVELS = 37  # depth[36] = 600 m, below the deepest hypoxic boundary observed


def _server_message(error: urllib.error.HTTPError) -> str:
    """Pull the human-readable sentence out of a Hyrax HTML error page."""
    try:
        body = error.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001 - a missing body must not mask the original error
        return ""
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    return re.sub(r"\s+", " ", text).strip()[:300]


def acquire(opener, url: str, destination: Path, *, attempts: int = 3) -> Path:
    """Download one subset unless it is already present, then report size and checksum.

    The server intermittently answers a valid large request with a 500, so a failed
    attempt is retried before it is believed. A malformed constraint expression fails
    the same way every time and still surfaces the server's own message.
    """

    if destination.exists():
        print(f"  exists, not overwriting: {destination.name}")
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")

    for attempt in range(1, attempts + 1):
        try:
            with opener.open(url) as response:
                content_type = response.headers.get("Content-Type", "")
                if "netcdf" not in content_type:
                    raise SystemExit(
                        f"Expected a NetCDF response, got {content_type!r}. The server "
                        "returns HTML when the constraint expression is malformed or "
                        f"the login failed.\nRequest: {url}"
                    )
                partial.write_bytes(response.read())
            break
        except urllib.error.HTTPError as error:
            message = _server_message(error)
            if attempt == attempts:
                partial.unlink(missing_ok=True)
                raise SystemExit(
                    f"Request failed {attempts} times with HTTP {error.code}.\n"
                    f"Server said: {message}\nRequest: {url}"
                ) from error
            print(f"    HTTP {error.code} on attempt {attempt}; retrying")
            time.sleep(3 * attempt)

    partial.replace(destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(f"  wrote {destination.name}  ({destination.stat().st_size / 1e6:.1f} MB)")
    print(f"    sha256: {digest}")
    return destination


def main() -> None:
    try:
        opener = earthdata_opener()
    except (FileNotFoundError, ValueError) as error:
        raise SystemExit(str(error)) from error
    print(f"CMS California Current System subsets -> {RAW_ROOT}\n")

    month = month_index(VOLUME_YEAR, VOLUME_MONTH)
    print(f"single-month volume ({VOLUME_YEAR}-{VOLUME_MONTH:02d}, {VOLUME_LEVELS} levels)")
    for variable in VOLUME_VARIABLES:
        url = dap4_subset_url(
            variable, first_month=month, last_month=month, depth_levels=VOLUME_LEVELS
        )
        acquire(
            opener,
            url,
            RAW_ROOT / f"ccs_{VOLUME_YEAR}-{VOLUME_MONTH:02d}_{variable}.nc4",
        )

    first, last = month_index(SEASONAL_YEAR, 1), month_index(SEASONAL_YEAR, 12)
    print(f"\nseasonal cycle ({SEASONAL_YEAR}, 12 months, {SEASONAL_LEVELS} levels)")
    acquire(
        opener,
        dap4_subset_url(
            SEASONAL_VARIABLE,
            first_month=first,
            last_month=last,
            depth_levels=SEASONAL_LEVELS,
        ),
        RAW_ROOT / f"ccs_{SEASONAL_YEAR}_{SEASONAL_VARIABLE}_monthly.nc4",
    )

    print("\nRecord every file in data/manifest.yml before analyzing it.")
    print("Each response carries the exact request in its `history` attribute.")


if __name__ == "__main__":
    main()
