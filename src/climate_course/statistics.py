"""Small, explicit statistical helpers used by the course notebooks."""

from collections.abc import Iterable

import numpy as np


def bootstrap_mean_interval(
    values: Iterable[float],
    *,
    confidence: float = 0.95,
    n_resamples: int = 5_000,
    seed: int = 2026,
) -> dict[str, float | int]:
    """Return a percentile bootstrap interval for a one-dimensional sample mean.

    The caller chooses what one value represents before calling this function. For example, passing
    one summer mean per year resamples years, whereas passing daily values resamples days. Missing or
    infinite values are rejected so the caller must make the missing-data policy visible.
    """

    sample = np.asarray(list(values), dtype=float)
    if sample.ndim != 1:
        raise ValueError("values must be one-dimensional")
    if sample.size < 2:
        raise ValueError("at least two values are required")
    if not np.isfinite(sample).all():
        raise ValueError("values must be finite; handle missing values before resampling")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    if not isinstance(n_resamples, int) or n_resamples < 100:
        raise ValueError("n_resamples must be an integer of at least 100")

    rng = np.random.default_rng(seed)
    bootstrap_means = rng.choice(
        sample,
        size=(n_resamples, sample.size),
        replace=True,
    ).mean(axis=1)
    tail = (1 - confidence) / 2
    lower, upper = np.quantile(bootstrap_means, [tail, 1 - tail])

    return {
        "estimate": float(sample.mean()),
        "lower": float(lower),
        "upper": float(upper),
        "confidence": float(confidence),
        "n_units": int(sample.size),
        "n_resamples": int(n_resamples),
        "seed": int(seed),
    }
