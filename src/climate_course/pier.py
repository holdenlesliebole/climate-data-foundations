"""Loading and small validation helpers for the original Scripps Pier temperature CSV."""

from pathlib import Path

import numpy as np
import pandas as pd


EXAMPLE_PIER_NOTE = (
    "built-in teaching example (invented values, not Scripps Pier observations)"
)

EXPECTED_PIER_COLUMNS = {
    "YEAR",
    "MONTH",
    "DAY",
    "TIME_PST",
    "TIME_FLAG",
    "SURF_TEMP_C",
    "SURF_FLAG",
    "BOT_TEMP_C",
    "BOT_FLAG",
}


def discover_pier_header(path: str | Path) -> int:
    """Return the zero-based row containing the Pier CSV table header.

    The original provider file includes a variable-length descriptive preamble. A clear error is
    raised when the expected header is absent or duplicated instead of guessing a row number.
    """

    path = Path(path)
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    matches = [
        index
        for index, line in enumerate(lines)
        if line.startswith("YEAR,MONTH,DAY")
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one Pier header in {path}; found rows {matches}."
        )
    return matches[0]


def load_pier_temperature(path: str | Path) -> pd.DataFrame:
    """Load an original Shore Stations Pier temperature CSV with dates and flags."""

    path = Path(path)
    header_index = discover_pier_header(path)
    frame = pd.read_csv(
        path,
        skiprows=header_index,
        usecols=range(9),
        na_values=["NaN"],
    )

    missing_columns = EXPECTED_PIER_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing expected Pier columns: {sorted(missing_columns)}")

    date_parts = frame[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower)
    frame["date"] = pd.to_datetime(date_parts, errors="coerce")
    if not frame["date"].notna().any():
        raise ValueError("No Pier dates could be parsed.")
    return frame


def example_pier_frame(end: str = "2026-06-30", days: int = 1095) -> pd.DataFrame:
    """Return a provider-shaped teaching table so a lesson can run without the real archive.

    The values are invented. They reproduce the *structure* students must work with—provider column
    names, a constructed ``date``, a seasonal cycle, missing observations, and nonzero quality
    flags—so that loading, plotting, and validation exercises behave realistically. They are never a
    substitute for the acquired archive and must not be cited or analyzed as observations.
    """

    if days < 2:
        raise ValueError("days must be at least 2 to form a time series.")

    dates = pd.date_range(end=pd.Timestamp(end), periods=days, freq="D")
    day_of_year = dates.dayofyear.to_numpy()
    seasonal = np.sin(2 * np.pi * (day_of_year - 100) / 365.25)

    generator = np.random.default_rng(19160101)
    surface = 16.5 + 3.0 * seasonal + generator.normal(0.0, 0.45, days)
    bottom = surface - (1.3 + 0.9 * seasonal) - generator.normal(0.0, 0.25, days)

    surface_flag = np.zeros(days, dtype=int)
    bottom_flag = np.zeros(days, dtype=int)
    surface_flag[::151] = 3
    bottom_flag[::197] = 1

    surface[::73] = np.nan
    bottom[::89] = np.nan

    frame = pd.DataFrame(
        {
            "YEAR": dates.year,
            "MONTH": dates.month,
            "DAY": dates.day,
            "TIME_PST": 745,
            "TIME_FLAG": 0,
            "SURF_TEMP_C": np.round(surface, 1),
            "SURF_FLAG": surface_flag,
            "BOT_TEMP_C": np.round(bottom, 1),
            "BOT_FLAG": bottom_flag,
        }
    )
    frame["date"] = pd.to_datetime(frame[["YEAR", "MONTH", "DAY"]].rename(columns=str.lower))
    return frame


def surface_bottom_difference(
    frame: pd.DataFrame,
    start: str,
    end: str,
    *,
    good_only: bool = True,
) -> pd.DataFrame:
    """Return paired surface/bottom values and ``surface - bottom`` in degrees Celsius.

    When ``good_only`` is true, rows must have provider flag value 0 for both measurements. Missing
    temperature pairs are always excluded because their difference is undefined. The function does
    not infer that unflagged data are representative or independent.
    """

    required = {
        "date",
        "SURF_TEMP_C",
        "BOT_TEMP_C",
        "SURF_FLAG",
        "BOT_FLAG",
    }
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if pd.Timestamp(start) > pd.Timestamp(end):
        raise ValueError("start must be earlier than or equal to end")

    mask = frame["date"].between(start, end)
    if good_only:
        mask &= frame["SURF_FLAG"].eq(0) & frame["BOT_FLAG"].eq(0)

    columns = ["date", "SURF_TEMP_C", "BOT_TEMP_C", "SURF_FLAG", "BOT_FLAG"]
    result = frame.loc[mask, columns].dropna(
        subset=["SURF_TEMP_C", "BOT_TEMP_C"]
    ).copy()
    if result.empty:
        raise ValueError("No paired Pier temperatures remain for this selection.")

    result["surface_minus_bottom_c"] = (
        result["SURF_TEMP_C"] - result["BOT_TEMP_C"]
    )
    return result
