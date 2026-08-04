import numpy as np
import pytest

from climate_course.statistics import bootstrap_mean_interval


def test_bootstrap_mean_interval_is_reproducible_and_ordered():
    result = bootstrap_mean_interval([1.0, 2.0, 3.0, 4.0], n_resamples=2_000, seed=7)

    assert result["estimate"] == pytest.approx(2.5)
    assert result["lower"] < result["estimate"] < result["upper"]
    assert result["n_units"] == 4
    assert result == bootstrap_mean_interval(
        [1.0, 2.0, 3.0, 4.0], n_resamples=2_000, seed=7
    )


@pytest.mark.parametrize(
    "values, message",
    [
        ([1.0], "at least two"),
        ([1.0, np.nan], "finite"),
        ([1.0, np.inf], "finite"),
    ],
)
def test_bootstrap_mean_interval_rejects_ambiguous_inputs(values, message):
    with pytest.raises(ValueError, match=message):
        bootstrap_mean_interval(values)


def test_bootstrap_mean_interval_validates_options():
    with pytest.raises(ValueError, match="confidence"):
        bootstrap_mean_interval([1.0, 2.0], confidence=1.0)
    with pytest.raises(ValueError, match="n_resamples"):
        bootstrap_mean_interval([1.0, 2.0], n_resamples=10)
