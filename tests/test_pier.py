from pathlib import Path

import pandas as pd
import pytest

from climate_course.pier import (
    EXPECTED_PIER_COLUMNS,
    discover_pier_header,
    example_pier_frame,
    load_pier_temperature,
    surface_bottom_difference,
)


PIER_FIXTURE = """Archive metadata,not part of table
Flag 0 means good data,

YEAR,MONTH,DAY,TIME_PST,TIME_FLAG,SURF_TEMP_C,SURF_FLAG,BOT_TEMP_C,BOT_FLAG
2026,1,1,08:00,0,16.0,0,15.5,0
2026,1,2,08:00,0,NaN,0,15.7,0
2026,1,3,08:00,0,17.0,3,16.0,0
2026,1,4,08:00,0,17.2,0,16.1,0
"""


@pytest.fixture
def pier_path(tmp_path: Path) -> Path:
    path = tmp_path / "pier.csv"
    path.write_text(PIER_FIXTURE, encoding="utf-8")
    return path


def test_discover_header(pier_path: Path) -> None:
    assert discover_pier_header(pier_path) == 3


def test_load_preserves_missing_values_and_builds_dates(pier_path: Path) -> None:
    frame = load_pier_temperature(pier_path)
    assert frame.shape == (4, 10)
    assert frame.loc[1, "SURF_TEMP_C"] != frame.loc[1, "SURF_TEMP_C"]  # NaN
    assert frame["date"].min() == pd.Timestamp("2026-01-01")


def test_good_only_difference_uses_flags_and_paired_values(pier_path: Path) -> None:
    frame = load_pier_temperature(pier_path)
    result = surface_bottom_difference(frame, "2026-01-01", "2026-01-04")
    assert result["date"].tolist() == [
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-01-04"),
    ]
    assert result["surface_minus_bottom_c"].tolist() == pytest.approx([0.5, 1.1])


def test_invalid_window_fails_loudly(pier_path: Path) -> None:
    frame = load_pier_temperature(pier_path)
    with pytest.raises(ValueError, match="start"):
        surface_bottom_difference(frame, "2026-02-01", "2026-01-01")


def test_empty_window_fails_loudly(pier_path: Path) -> None:
    frame = load_pier_temperature(pier_path)
    with pytest.raises(ValueError, match="No paired"):
        surface_bottom_difference(frame, "1999-01-01", "1999-01-02")


def test_example_frame_matches_provider_shape() -> None:
    frame = example_pier_frame()
    assert EXPECTED_PIER_COLUMNS.issubset(frame.columns)
    assert "date" in frame.columns
    assert frame["date"].is_monotonic_increasing
    assert frame["date"].max() == pd.Timestamp("2026-06-30")


def test_example_frame_is_deterministic_and_teachable() -> None:
    first = example_pier_frame(days=400)
    second = example_pier_frame(days=400)
    pd.testing.assert_frame_equal(first, second)

    # The fallback must exercise the same problems as the provider file.
    assert first["SURF_TEMP_C"].isna().any()
    assert first["BOT_TEMP_C"].isna().any()
    assert (first["SURF_FLAG"] != 0).any()
    # Wednesday's plausible-range assertion must pass on the recorded values.
    assert first["SURF_TEMP_C"].dropna().between(-2.0, 40.0).all()

    paired = first.dropna(subset=["SURF_TEMP_C", "BOT_TEMP_C"])
    assert (paired["SURF_TEMP_C"] > paired["BOT_TEMP_C"]).mean() > 0.8


def test_example_frame_works_with_the_course_helpers() -> None:
    frame = example_pier_frame(days=400)
    result = surface_bottom_difference(frame, "2026-01-01", "2026-06-30", good_only=True)
    assert not result.empty
    assert (result[["SURF_FLAG", "BOT_FLAG"]] == 0).all().all()


def test_example_frame_rejects_a_degenerate_request() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        example_pier_frame(days=1)
