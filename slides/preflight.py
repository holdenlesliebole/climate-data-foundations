"""Pre-class check. Run this from the course root before you present.

    python3 slides/preflight.py

Checks the things that would only surface in front of the room: the kernel, the
packages, the data the notebooks read, the files you present from, whether the
live download still works, and whether a rehearsal clone is in the way.
"""
import json
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent.parent
KERNEL = Path.home() / "Library/Jupyter/kernels/climate-data-foundations/kernel.json"

GREEN, RED, YELLOW, DIM, OFF = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
results = []


def check(label, ok, detail="", fatal=True):
    mark = f"{GREEN}PASS{OFF}" if ok else (f"{RED}FAIL{OFF}" if fatal else f"{YELLOW}WARN{OFF}")
    print(f"  [{mark}] {label}" + (f"{DIM}  {detail}{OFF}" if detail else ""))
    results.append((ok, fatal))
    return ok


print(f"\n{'=' * 62}\n  Pre-class check\n{'=' * 62}\n")

# ---------------------------------------------------------------- kernel
print("Kernel and packages")
kernel_python = None
if check("course kernel is registered", KERNEL.exists(), str(KERNEL.parent.name)):
    kernel_python = json.loads(KERNEL.read_text())["argv"][0]
    check("its interpreter exists", Path(kernel_python).exists(), kernel_python)

if kernel_python and Path(kernel_python).exists():
    for package in ("numpy", "pandas", "xarray", "matplotlib", "plotly"):
        probe = subprocess.run(
            [kernel_python, "-c", f"import {package}; print({package}.__version__)"],
            capture_output=True, text=True)
        check(f"{package} importable in the kernel",
              probe.returncode == 0, probe.stdout.strip() or probe.stderr.strip()[:40],
              fatal=(package != "plotly"))

# ---------------------------------------------------------------- data
print("\nData the notebooks read")
pier = sorted((ROOT / "data/raw/pier").glob("LaJolla_TEMP_*.csv"))
check("Pier temperature CSV present", bool(pier),
      pier[-1].name if pier else "notebook 05 falls back to invented example data")
mop = sorted((ROOT / "data/raw/mop").glob("*.nc"))
check("MOP NetCDF already downloaded", bool(mop),
      f"{len(mop)} file(s) — notebook 04 will reuse, not re-download", fatal=False)

# ---------------------------------------------------------------- files
print("\nFiles you present from")
for rel in ("notebooks/04_remote_data.ipynb", "notebooks/05_reliable_code.ipynb",
            "notebooks/045_3d_ccs.ipynb", "notebooks/046_lorenz.ipynb",
            "notebooks/047_mandelbrot.ipynb", "slides/wednesday_deck.html"):
    check(rel, (ROOT / rel).exists())

for rel in ("reference/04_remote_data_complete.ipynb",
            "reference/05_reliable_code_complete.ipynb"):
    path = ROOT / rel
    if check(rel, path.exists()):
        nb = json.loads(path.read_text())
        code = [c for c in nb["cells"] if c["cell_type"] == "code"]
        with_output = sum(1 for c in code if c.get("outputs"))
        check(f"  └─ outputs stored (never needs running)",
              with_output >= len(code) - 2, f"{with_output}/{len(code)} cells")

# ---------------------------------------------------------------- network
print("\nLive dependencies")
try:
    socket.setdefaulttimeout(20)
    params = [("var", v) for v in
              ("waveHs", "waveTp", "waveDp", "waveFlagPrimary", "waveFlagSecondary")]
    params += [("stns", "all"), ("time_start", "2026-07-01T00:00:00Z"),
               ("time_end", "2026-07-07T23:00:00Z"), ("timeStride", "1"),
               ("accept", "netcdf4")]
    url = ("https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/"
           "MOP_alongshore/D0513_nowcast.nc?" + urlencode(params))
    with urllib.request.urlopen(url, timeout=25) as response:
        magic = response.read(4)
    check("CDIP returns real NetCDF", magic[:3] == b"CDF" or magic[:4] == b"\x89HDF",
          "notebook 04 section 3 will work", fatal=False)
except (urllib.error.URLError, socket.timeout, OSError) as error:
    check("CDIP reachable", False, f"{type(error).__name__} — use reference/04 instead",
          fatal=False)

# ---------------------------------------------------------------- demo hygiene
print("\nLive demo hygiene")
stale = Path.home() / "Desktop/course-reference"
check("no rehearsal clone on the Desktop", not stale.exists(),
      "delete it or the live git clone will refuse" if stale.exists() else "")
check("git is on PATH", shutil.which("git") is not None,
      "students without git use the ZIP route on slide 32", fatal=False)

# ---------------------------------------------------------------- verdict
failed = [fatal for ok, fatal in results if not ok]
print(f"\n{'=' * 62}")
if not failed:
    print(f"  {GREEN}Everything checks out. Go teach.{OFF}")
elif not any(failed):
    print(f"  {YELLOW}Warnings only — nothing that stops the session.{OFF}")
else:
    print(f"  {RED}{sum(1 for f in failed if f)} blocking problem(s) above.{OFF}")
print(f"{'=' * 62}\n")
sys.exit(1 if any(failed) else 0)
