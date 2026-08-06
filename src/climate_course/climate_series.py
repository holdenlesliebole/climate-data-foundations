"""Load and annualize the public climate series used in Friday's relationship lesson."""

from pathlib import Path

import pandas as pd


MLO_COLUMNS = [
    "year",
    "month",
    "excel_date",
    "decimal_date",
    "co2_ppm",
    "seasonally_adjusted_co2_ppm",
    "fit_ppm",
    "seasonally_adjusted_fit_ppm",
    "filled_co2_ppm",
    "seasonally_adjusted_filled_co2_ppm",
    "station",
]


def _unique_header_index(path: str | Path, starts_with: str) -> int:
    """Find one provider header by content rather than a hard-coded line number."""

    path = Path(path)
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    matches = [
        index
        for index, line in enumerate(lines)
        if line.lstrip().startswith(starts_with)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one header beginning {starts_with!r} in {path}; "
            f"found rows {matches}."
        )
    return matches[0]


def load_gistemp_annual(path: str | Path) -> pd.DataFrame:
    """Load NASA GISTEMP global annual anomalies from the provider CSV.

    The returned anomaly is the ``J-D`` annual Land-Ocean Temperature Index in degrees Celsius,
    relative to NASA's stated 1951--1980 baseline. Incomplete annual values marked ``***`` are
    excluded.
    """

    path = Path(path)
    header_index = _unique_header_index(path, "Year,Jan,")
    frame = pd.read_csv(path, skiprows=header_index, na_values=["***"])
    required = {"Year", "J-D"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing expected GISTEMP columns: {sorted(missing)}")

    result = frame[["Year", "J-D"]].rename(
        columns={"Year": "year", "J-D": "global_temp_anomaly_c"}
    )
    result["year"] = pd.to_numeric(result["year"], errors="coerce")
    result["global_temp_anomaly_c"] = pd.to_numeric(
        result["global_temp_anomaly_c"], errors="coerce"
    )
    result = result.dropna().astype({"year": int}).reset_index(drop=True)
    if result.empty or result["year"].duplicated().any():
        raise ValueError("GISTEMP annual table must contain one finite value per year.")
    return result


def load_scripps_mlo_monthly(path: str | Path) -> pd.DataFrame:
    """Load the Scripps monthly in-situ Mauna Loa CO2 provider CSV.

    The provider file has a descriptive preamble and three header rows. Missing measurements use
    ``-99.99``. The function preserves measured, adjusted, fitted, and filled columns so the caller
    must choose which product answers the question.
    """

    path = Path(path)
    header_index = _unique_header_index(path, "Yr, Mn,")
    frame = pd.read_csv(
        path,
        skiprows=header_index + 3,
        names=MLO_COLUMNS,
        na_values=[-99.99, "-99.99"],
        skipinitialspace=True,
    )
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame["month"] = pd.to_numeric(frame["month"], errors="coerce")
    for column in MLO_COLUMNS[2:-1]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["station"] = frame["station"].astype("string").str.strip()
    frame = frame.dropna(subset=["year", "month"]).astype(
        {"year": int, "month": int}
    )
    if frame.empty or not frame["month"].between(1, 12).all():
        raise ValueError("Scripps CO2 table must contain valid year/month rows.")
    if frame[["year", "month"]].duplicated().any():
        raise ValueError("Scripps CO2 table must contain at most one row per year/month.")
    return frame.reset_index(drop=True)


def annual_pier_surface(
    frame: pd.DataFrame,
    *,
    min_days: int = 180,
) -> pd.DataFrame:
    """Return annual mean good-flag Pier surface SST with an explicit coverage threshold.

    Multiple good observations on one date are first averaged so a date cannot receive extra weight
    merely because it has duplicate rows. Flag value 0 is the Shore Stations good-data rule used in
    the course provider file.
    """

    required = {"date", "SURF_TEMP_C", "SURF_FLAG"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required Pier columns: {sorted(missing)}")
    if not isinstance(min_days, int) or not 1 <= min_days <= 366:
        raise ValueError("min_days must be an integer between 1 and 366")

    selected = frame.loc[
        frame["date"].notna()
        & frame["SURF_TEMP_C"].notna()
        & frame["SURF_FLAG"].eq(0),
        ["date", "SURF_TEMP_C"],
    ].copy()
    daily = (
        selected.groupby("date", as_index=False)
        .agg(pier_surface_sst_c=("SURF_TEMP_C", "mean"))
        .assign(year=lambda values: values["date"].dt.year)
    )
    annual = (
        daily.groupby("year", as_index=False)
        .agg(
            pier_mean_sst_c=("pier_surface_sst_c", "mean"),
            n_pier_days=("pier_surface_sst_c", "size"),
        )
        .query("n_pier_days >= @min_days")
        .reset_index(drop=True)
    )
    if annual.empty:
        raise ValueError("No Pier years meet the stated daily-coverage threshold.")
    return annual


def annual_mlo_co2(
    frame: pd.DataFrame,
    *,
    min_months: int = 8,
) -> pd.DataFrame:
    """Return annual means of measured monthly Mauna Loa CO2 values."""

    required = {"year", "month", "co2_ppm"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required Mauna Loa columns: {sorted(missing)}")
    if not isinstance(min_months, int) or not 1 <= min_months <= 12:
        raise ValueError("min_months must be an integer between 1 and 12")

    annual = (
        frame.dropna(subset=["co2_ppm"])
        .groupby("year", as_index=False)
        .agg(
            mlo_co2_ppm=("co2_ppm", "mean"),
            n_co2_months=("month", "nunique"),
        )
        .query("n_co2_months >= @min_months")
        .reset_index(drop=True)
    )
    if annual.empty:
        raise ValueError("No Mauna Loa years meet the stated monthly-coverage threshold.")
    return annual
