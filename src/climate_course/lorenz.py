"""Lorenz's 1963 convection model, integrated with an explicit Runge-Kutta scheme.

Edward Lorenz reduced a model of a convecting fluid layer to three ordinary differential
equations and found that two runs started from almost identical states diverged until they
had nothing in common. That result is why weather forecasts have a horizon, why forecast
centres run ensembles instead of single trajectories, and why a climate projection is a
statement about a distribution rather than about a particular day.

The equations are

    dx/dt = sigma * (y - x)
    dy/dt = x * (rho - z) - y
    dz/dt = x * y - beta * z

where ``x`` is convective overturning, ``y`` the horizontal temperature contrast, and ``z``
the departure of the vertical temperature profile from linear. The classic parameters put
the system in its chaotic regime.
"""

import numpy as np


CLASSIC_SIGMA = 10.0
CLASSIC_RHO = 28.0
CLASSIC_BETA = 8.0 / 3.0

# Benettin et al. and every textbook since put the largest Lyapunov exponent of the
# classic parameter set near this value. It is the number the notebook checks against.
REFERENCE_LYAPUNOV = 0.906

CITATION = (
    "Lorenz, E. N. (1963), Deterministic Nonperiodic Flow, Journal of the Atmospheric "
    "Sciences, 20(2), 130-141, doi:10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2"
)


def lorenz_derivative(
    state: np.ndarray,
    *,
    sigma: float = CLASSIC_SIGMA,
    rho: float = CLASSIC_RHO,
    beta: float = CLASSIC_BETA,
) -> np.ndarray:
    """Time derivative at one state, or at a stack of states shaped ``(..., 3)``."""

    state = np.asarray(state, dtype=float)
    if state.shape[-1] != 3:
        raise ValueError(f"state must end in a length-3 axis, got shape {state.shape}")

    x, y, z = state[..., 0], state[..., 1], state[..., 2]
    return np.stack(
        [sigma * (y - x), x * (rho - z) - y, x * y - beta * z],
        axis=-1,
    )


def fixed_points(
    *,
    sigma: float = CLASSIC_SIGMA,
    rho: float = CLASSIC_RHO,
    beta: float = CLASSIC_BETA,
) -> np.ndarray:
    """The three steady states, as rows.

    The origin is always one. For ``rho > 1`` two more appear, one in the centre of each
    wing of the attractor. A trajectory never settles onto either: they are unstable for
    the classic parameters, which is precisely why the solution keeps switching wings.
    """

    origin = np.zeros(3)
    if rho <= 1:
        return origin[np.newaxis, :]

    offset = np.sqrt(beta * (rho - 1))
    return np.array(
        [origin, [offset, offset, rho - 1], [-offset, -offset, rho - 1]],
        dtype=float,
    )


def _rk4_step(state, dt, sigma, rho, beta):
    """One classical fourth-order Runge-Kutta step."""
    k1 = lorenz_derivative(state, sigma=sigma, rho=rho, beta=beta)
    k2 = lorenz_derivative(state + 0.5 * dt * k1, sigma=sigma, rho=rho, beta=beta)
    k3 = lorenz_derivative(state + 0.5 * dt * k2, sigma=sigma, rho=rho, beta=beta)
    k4 = lorenz_derivative(state + dt * k3, sigma=sigma, rho=rho, beta=beta)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate(
    initial_state,
    *,
    sigma: float = CLASSIC_SIGMA,
    rho: float = CLASSIC_RHO,
    beta: float = CLASSIC_BETA,
    dt: float = 0.005,
    steps: int = 8000,
) -> np.ndarray:
    """Integrate forward and return every state, including the initial one.

    ``initial_state`` may be a single point of shape ``(3,)`` or a stack shaped
    ``(n, 3)``; a stack is advanced together, which is how the ensemble figure stays fast.
    The result has shape ``(steps + 1, 3)`` or ``(steps + 1, n, 3)``.

    Euler would be simpler, but it drifts off the attractor badly enough to be visible at
    this step size. Fourth-order Runge-Kutta costs four derivative evaluations per step
    and stays on it.
    """

    state = np.asarray(initial_state, dtype=float)
    if state.shape[-1] != 3:
        raise ValueError(f"initial_state must end in a length-3 axis, got {state.shape}")
    if steps < 1:
        raise ValueError(f"steps must be at least 1, got {steps}")
    if dt <= 0:
        raise ValueError(f"dt must be positive, got {dt}")

    trajectory = np.empty((steps + 1,) + state.shape, dtype=float)
    trajectory[0] = state
    for index in range(steps):
        trajectory[index + 1] = _rk4_step(trajectory[index], dt, sigma, rho, beta)
    return trajectory


def perturbed_pair(
    initial_state,
    *,
    offset: float = 1e-9,
    axis: int = 0,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray]:
    """Two trajectories whose starting points differ by ``offset`` along one axis.

    ``offset`` defaults to a nanometre-scale difference in dimensionless units: far below
    any measurement precision, and still enough to destroy agreement within a few tens of
    time units.
    """

    first = np.asarray(initial_state, dtype=float)
    second = first.copy()
    second[axis] += offset
    return integrate(first, **kwargs), integrate(second, **kwargs)


def separation(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    """Euclidean distance between two trajectories at each step."""
    first, second = np.asarray(first), np.asarray(second)
    if first.shape != second.shape:
        raise ValueError(f"shapes differ: {first.shape} vs {second.shape}")
    return np.linalg.norm(first - second, axis=-1)


def largest_lyapunov(
    initial_state=(1.0, 1.0, 1.0),
    *,
    sigma: float = CLASSIC_SIGMA,
    rho: float = CLASSIC_RHO,
    beta: float = CLASSIC_BETA,
    dt: float = 0.005,
    renormalisations: int = 2000,
    steps_between: int = 20,
    offset: float = 1e-8,
    discard: int = 200,
) -> float:
    """Estimate the largest Lyapunov exponent by repeated renormalisation.

    Separation grows exponentially only while it stays small; once two trajectories are
    on opposite wings the distance saturates at the size of the attractor and says nothing
    about growth rate. The standard fix, due to Benettin and colleagues, is to let the gap
    grow for a short interval, record how much it grew, then shrink it back to its original
    size along the same direction and continue.

    The first ``discard`` intervals are thrown away so the estimate is not contaminated by
    the transient approach to the attractor.
    """

    if renormalisations <= discard:
        raise ValueError("renormalisations must exceed discard")

    reference = np.asarray(initial_state, dtype=float)
    separated = reference.copy()
    separated[0] += offset

    kwargs = dict(sigma=sigma, rho=rho, beta=beta, dt=dt, steps=steps_between)
    growth = []
    for index in range(renormalisations):
        reference = integrate(reference, **kwargs)[-1]
        separated = integrate(separated, **kwargs)[-1]

        difference = separated - reference
        distance = np.linalg.norm(difference)
        if distance == 0:
            raise FloatingPointError("trajectories coincided; increase offset")

        if index >= discard:
            growth.append(np.log(distance / offset))
        separated = reference + difference * (offset / distance)

    return float(np.mean(growth) / (steps_between * dt))
