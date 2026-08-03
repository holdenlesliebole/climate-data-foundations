from pathlib import Path

import pandas as pd
import pytest

from climate_course.pier import (
    discover_pier_header,
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
