import numpy as np
import pytest
import xarray as xr

from climate_course.ccs import (
    dap4_subset_url,
    hypoxic_boundary_depth,
    month_index,
)


def oxygen_column(profile: list[float], depths: list[float]) -> xr.DataArray:
    """One synthetic profile broadcast onto a 1x1 horizontal grid."""
    values = np.array(profile, dtype=float).reshape(len(depths), 1, 1)
    return xr.DataArray(
        values,
        dims=("depth", "lat", "lon"),
        coords={"depth": depths, "lat": [33.0], "lon": [-120.0]},
    )


def test_month_index_counts_from_january_2007() -> None:
    assert month_index(2007, 1) == 0
    assert month_index(2010, 7) == 42
    assert month_index(2010, 12) == 47


@pytest.mark.parametrize("year,month", [(2006, 12), (2011, 1), (2010, 13)])
def test_month_index_rejects_dates_outside_the_record(year: int, month: int) -> None:
    with pytest.raises(ValueError):
        month_index(year, month)


def test_dap4_url_ranges_are_inclusive_and_coordinates_match_the_array() -> None:
    url = dap4_subset_url("O2", first_month=42, last_month=42, depth_levels=45)
    assert "/O2[42][0:44][0:170][0:239]" in url
    assert "/depth[0:44]" in url  # same depth extent as the data array
    assert "/time[42]" in url
    assert url.startswith("https://acdisc.gesdisc.eosdis.nasa.gov/opendap/")


def test_dap4_url_spans_a_month_range() -> None:
    url = dap4_subset_url("O2", first_month=36, last_month=47, depth_levels=37)
    assert "/O2[36:47][0:36][0:170][0:239]" in url
    assert "/time[36:47]" in url


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(first_month=47, last_month=36, depth_levels=45),
        dict(first_month=0, last_month=48, depth_levels=45),
        dict(first_month=0, last_month=0, depth_levels=0),
    ],
)
def test_dap4_url_rejects_impossible_requests(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        dap4_subset_url("O2", **kwargs)


def test_boundary_is_the_first_crossing_not_the_minimum() -> None:
    depths = [10.0, 20.0, 30.0, 40.0]
    # Dips below 0.06 at 20 m, recovers, then drops again. The first crossing wins.
    oxygen = oxygen_column([0.20, 0.05, 0.09, 0.01], depths)
    result = hypoxic_boundary_depth(oxygen)
    assert result.values[0, 0] == 20.0


def test_column_that_never_crosses_is_nan_not_the_deepest_level() -> None:
    oxygen = oxygen_column([0.25, 0.22, 0.20, 0.18], [10.0, 20.0, 30.0, 40.0])
    assert np.isnan(hypoxic_boundary_depth(oxygen).values[0, 0])


def test_land_column_stays_nan() -> None:
    oxygen = oxygen_column([np.nan] * 4, [10.0, 20.0, 30.0, 40.0])
    assert np.isnan(hypoxic_boundary_depth(oxygen).values[0, 0])


def test_threshold_is_adjustable() -> None:
    depths = [10.0, 20.0, 30.0, 40.0]
    oxygen = oxygen_column([0.20, 0.15, 0.08, 0.03], depths)
    assert hypoxic_boundary_depth(oxygen, threshold=0.06).values[0, 0] == 40.0
    assert hypoxic_boundary_depth(oxygen, threshold=0.16).values[0, 0] == 20.0


def test_result_keeps_horizontal_coordinates_and_units() -> None:
    oxygen = oxygen_column([0.20, 0.01, 0.01, 0.01], [10.0, 20.0, 30.0, 40.0])
    result = hypoxic_boundary_depth(oxygen)
    assert result.dims == ("lat", "lon")
    assert result.attrs["units"] == "m"
    assert float(result["lat"][0]) == 33.0


def test_rejects_input_without_depth() -> None:
    flat = xr.DataArray(
        np.zeros((1, 1)), dims=("lat", "lon"), coords={"lat": [33.0], "lon": [-120.0]}
    )
    with pytest.raises(ValueError):
        hypoxic_boundary_depth(flat)
