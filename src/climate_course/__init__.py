"""Reusable course helpers.

The Pier, climate-series, and statistics helpers come from Wednesday's reliability
session. The ``ccs``, ``lorenz``, and ``mandelbrot`` modules back the three visualisation
projects and are imported by notebooks 045 to 047.
"""

from .ccs import (
    CITATION as CMS_CCS_CITATION,
    DEFAULT_HYPOXIC_THRESHOLD,
    dap4_subset_url,
    earthdata_opener,
    hypoxic_boundary_depth,
    load_ccs_subset,
    month_index,
)
from .climate_series import (
    annual_mlo_co2,
    annual_pier_surface,
    load_gistemp_annual,
    load_scripps_mlo_monthly,
)
from .lorenz import (
    CITATION as LORENZ_CITATION,
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
from .mandelbrot import (
    DEEPEST_USEFUL_SPAN,
    MISIUREWICZ_POINT,
    REGIONS,
    in_set,
    iterations_for_span,
    region,
    render,
    smallest_reliable_span,
    to_rgb,
    zoom_spans,
)
from .pier import (
    EXAMPLE_PIER_NOTE,
    EXPECTED_PIER_COLUMNS,
    discover_pier_header,
    example_pier_frame,
    load_pier_temperature,
    surface_bottom_difference,
)

__all__ = [
    "CLASSIC_BETA",
    "CLASSIC_RHO",
    "CLASSIC_SIGMA",
    "CMS_CCS_CITATION",
    "DEEPEST_USEFUL_SPAN",
    "DEFAULT_HYPOXIC_THRESHOLD",
    "EXAMPLE_PIER_NOTE",
    "EXPECTED_PIER_COLUMNS",
    "LORENZ_CITATION",
    "MISIUREWICZ_POINT",
    "REFERENCE_LYAPUNOV",
    "REGIONS",
    "annual_mlo_co2",
    "annual_pier_surface",
    "dap4_subset_url",
    "discover_pier_header",
    "earthdata_opener",
    "example_pier_frame",
    "fixed_points",
    "hypoxic_boundary_depth",
    "in_set",
    "integrate",
    "iterations_for_span",
    "largest_lyapunov",
    "load_ccs_subset",
    "load_gistemp_annual",
    "load_pier_temperature",
    "load_scripps_mlo_monthly",
    "lorenz_derivative",
    "month_index",
    "perturbed_pair",
    "region",
    "render",
    "separation",
    "smallest_reliable_span",
    "surface_bottom_difference",
    "to_rgb",
    "zoom_spans",
]
