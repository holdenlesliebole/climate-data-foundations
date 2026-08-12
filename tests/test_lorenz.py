import numpy as np
import pytest
from scipy.integrate import solve_ivp

from climate_course.lorenz import (
    CLASSIC_BETA,
    CLASSIC_RHO,
    CLASSIC_SIGMA,
    REFERENCE_LYAPUNOV,
    fixed_points,
    integrate,
    largest_lyapunov,
    lorenz_derivative,
    perturbed_pair,
    separation,
)


def test_origin_is_a_steady_state() -> None:
    assert np.allclose(lorenz_derivative([0.0, 0.0, 0.0]), 0.0)


def test_wing_centres_are_steady_states() -> None:
    for point in fixed_points()[1:]:
        assert np.allclose(lorenz_derivative(point), 0.0, atol=1e-12)


def test_only_the_origin_survives_below_the_critical_rho() -> None:
    assert fixed_points(rho=0.5).shape == (1, 3)
    assert fixed_points(rho=28.0).shape == (3, 3)


def test_derivative_broadcasts_over_a_stack_of_states() -> None:
    states = np.array([[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [-5.0, 2.0, 30.0]])
    stacked = lorenz_derivative(states)
    assert stacked.shape == (3, 3)
    for row, state in zip(stacked, states):
        assert np.allclose(row, lorenz_derivative(state))


def test_derivative_rejects_wrong_trailing_axis() -> None:
    with pytest.raises(ValueError):
        lorenz_derivative([1.0, 2.0])


def test_integration_matches_scipy_over_a_short_horizon() -> None:
    start = np.array([1.0, 1.0, 1.0])
    dt, steps = 0.001, 2000  # 2 time units, before divergence matters

    ours = integrate(start, dt=dt, steps=steps)[-1]
    reference = solve_ivp(
        lambda _, state: lorenz_derivative(state),
        (0.0, dt * steps),
        start,
        rtol=1e-11,
        atol=1e-12,
    ).y[:, -1]

    assert np.allclose(ours, reference, rtol=1e-6, atol=1e-6)


def test_runge_kutta_is_fourth_order() -> None:
    start = np.array([1.0, 1.0, 1.0])
    horizon = 1.0

    reference = solve_ivp(
        lambda _, state: lorenz_derivative(state),
        (0.0, horizon),
        start,
        rtol=1e-13,
        atol=1e-14,
    ).y[:, -1]

    # Steps coarser than about 0.0025 are not yet in the asymptotic regime: leftover
    # higher-order terms cancel and the apparent order climbs above 5.
    coarse_dt = 0.005
    coarse = integrate(start, dt=coarse_dt, steps=int(horizon / coarse_dt))[-1]
    fine = integrate(start, dt=coarse_dt / 2, steps=int(2 * horizon / coarse_dt))[-1]

    coarse_error = np.linalg.norm(coarse - reference)
    fine_error = np.linalg.norm(fine - reference)
    order = np.log2(coarse_error / fine_error)

    assert 3.3 < order < 4.7, f"expected fourth-order convergence, measured {order:.2f}"


def test_trajectory_stays_on_a_bounded_attractor() -> None:
    trajectory = integrate([1.0, 1.0, 1.0], dt=0.005, steps=20000)
    assert np.all(np.isfinite(trajectory))
    assert np.abs(trajectory[:, 0]).max() < 100
    assert np.abs(trajectory[:, 2]).max() < 100
    assert trajectory[:, 2].min() > -1  # z stays positive on the attractor


def test_trajectory_visits_both_wings() -> None:
    trajectory = integrate([1.0, 1.0, 1.0], dt=0.005, steps=20000)
    assert (trajectory[:, 0] > 5).any() and (trajectory[:, 0] < -5).any()


def test_an_ensemble_advances_together_and_matches_individual_runs() -> None:
    cloud = np.array([[1.0, 1.0, 1.0], [1.0, 1.0, 1.001], [2.0, 1.0, 1.0]])
    together = integrate(cloud, dt=0.005, steps=500)
    assert together.shape == (501, 3, 3)

    for column, member in enumerate(cloud):
        alone = integrate(member, dt=0.005, steps=500)
        assert np.allclose(together[:, column, :], alone)


def test_nearby_starts_track_then_separate() -> None:
    first, second = perturbed_pair([1.0, 1.0, 1.0], offset=1e-9, dt=0.005, steps=12000)
    gap = separation(first, second)

    assert gap[0] == pytest.approx(1e-9)
    assert gap[200] < 1e-6            # indistinguishable early on
    assert gap[-1] > 1.0              # and unrecognisable by the end
    assert np.isfinite(gap).all()


def test_separation_rejects_mismatched_shapes() -> None:
    with pytest.raises(ValueError):
        separation(np.zeros((10, 3)), np.zeros((9, 3)))


def test_lyapunov_estimate_matches_the_published_value() -> None:
    estimate = largest_lyapunov(renormalisations=1500, discard=200)
    assert estimate == pytest.approx(REFERENCE_LYAPUNOV, abs=0.06)


def test_lyapunov_is_negative_in_the_steady_regime() -> None:
    # Below rho = 1 the origin is stable, so perturbations decay instead of growing.
    estimate = largest_lyapunov(rho=0.5, renormalisations=600, discard=100)
    assert estimate < 0


@pytest.mark.parametrize("kwargs", [dict(dt=0.0), dict(dt=-0.01), dict(steps=0)])
def test_integrate_rejects_impossible_settings(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        integrate([1.0, 1.0, 1.0], **kwargs)


def test_classic_parameters_are_the_1963_values() -> None:
    assert (CLASSIC_SIGMA, CLASSIC_RHO) == (10.0, 28.0)
    assert CLASSIC_BETA == pytest.approx(8.0 / 3.0)
