from pathlib import Path

import pandas as pd
import pytest

from climate_course.climate_series import (
    annual_mlo_co2,
    annual_pier_surface,
    load_gistemp_annual,
    load_scripps_mlo_monthly,
)


GISTEMP_FIXTURE = """Land-Ocean: Global Means
Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
1958,.39,.39,.40,.30,.30,.20,.20,.20,.20,.20,.20,.20,.27,***,***,.33,.20,.20
1959,.10,.10,.10,.10,.10,.10,.10,.10,.10,.10,.10,.10,.10,.20,.20,.10,.10,.10
1960,.20,.20,.20,.20,.20,.20,.20,.20,.20,.20,.20,.20,***,.15,.15,.20,.20,.20
"""

MLO_FIXTURE = """\"provider preamble\"
  Yr, Mn,    Date,      Date,     CO2,seasonally,        fit,  seasonally,      CO2, seasonally, Sta
    ,   ,        ,          ,        ,  adjusted,           ,adjusted fit,   filled,adjusted filled
    ,   ,   Excel,          ,   [ppm],    [ppm] ,      [ppm],    [ppm],       [ppm],    [ppm]
1958, 01, 21200, 1958.04, -99.99, -99.99, 316.20, 314.90, 316.20, 314.90, MLO
1958, 03, 21259, 1958.20, 315.71, 314.43, 316.20, 314.90, 315.71, 314.43, MLO
1958, 04, 21290, 1958.29, 317.45, 315.15, 317.30, 314.98, 317.45, 315.15, MLO
1959, 01, 21565, 1959.04, 315.58, 315.52, 315.64, 315.57, 315.58, 315.52, MLO
"""


def test_load_gistemp_discovers_header_and_drops_incomplete_year(tmp_path: Path):
    path = tmp_path / "gistemp.csv"
    path.write_text(GISTEMP_FIXTURE, encoding="utf-8")

    result = load_gistemp_annual(path)

    assert result.to_dict("records") == [
        {"year": 1958, "global_temp_anomaly_c": pytest.approx(0.27)},
        {"year": 1959, "global_temp_anomaly_c": pytest.approx(0.10)},
    ]


def test_load_mlo_preserves_measured_and_filled_products(tmp_path: Path):
    path = tmp_path / "mlo.csv"
    path.write_text(MLO_FIXTURE, encoding="utf-8")

    result = load_scripps_mlo_monthly(path)

    assert pd.isna(result.loc[0, "co2_ppm"])
    assert result.loc[0, "filled_co2_ppm"] == pytest.approx(316.20)
    assert result.loc[1, "station"] == "MLO"


def test_annual_pier_surface_uses_good_unique_days_and_threshold():
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2000-01-01", "2000-01-01", "2000-01-02", "2001-01-01"]
            ),
            "SURF_TEMP_C": [10.0, 12.0, 13.0, 99.0],
            "SURF_FLAG": [0, 0, 0, 3],
        }
    )

    result = annual_pier_surface(frame, min_days=2)

    assert result.loc[0, "year"] == 2000
    assert result.loc[0, "n_pier_days"] == 2
    assert result.loc[0, "pier_mean_sst_c"] == pytest.approx(12.0)


def test_annual_mlo_co2_applies_observed_month_threshold(tmp_path: Path):
    path = tmp_path / "mlo.csv"
    path.write_text(MLO_FIXTURE, encoding="utf-8")
    monthly = load_scripps_mlo_monthly(path)

    result = annual_mlo_co2(monthly, min_months=2)

    assert result["year"].tolist() == [1958]
    assert result.loc[0, "mlo_co2_ppm"] == pytest.approx((315.71 + 317.45) / 2)


def test_annual_helpers_validate_coverage_thresholds():
    pier = pd.DataFrame(
        {
            "date": pd.to_datetime(["2000-01-01"]),
            "SURF_TEMP_C": [12.0],
            "SURF_FLAG": [0],
        }
    )
    mlo = pd.DataFrame({"year": [2000], "month": [1], "co2_ppm": [370.0]})

    with pytest.raises(ValueError, match="min_days"):
        annual_pier_surface(pier, min_days=0)
    with pytest.raises(ValueError, match="min_months"):
        annual_mlo_co2(mlo, min_months=13)


@pytest.mark.parametrize(
    ("function", "frame", "keyword", "value", "message"),
    [
        (annual_pier_surface, pd.DataFrame(), "min_days", 0, "Missing required"),
        (annual_mlo_co2, pd.DataFrame(), "min_months", 0, "Missing required"),
    ],
)
def test_annual_helpers_reject_missing_columns(function, frame, keyword, value, message):
    with pytest.raises(ValueError, match=message):
        function(frame, **{keyword: value})
