# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Reference: Python as a scientific calculator
#
# This completed notebook records Monday's core path. It is intentionally concise: use the guided notebook for prompts and this version later as a working example.
#
# Recurring check: **What is the shape? What are the units? What is one known answer?**

# %%
import numpy as np

# %% [markdown]
# ## Variables, expressions, and types
#
# Python evaluates multiplication before addition: `2 + 3 * 4` is 14, while `(2 + 3) * 4` is 20. `/` produces a floating-point result, so `10 / 4` is 2.5.

# %%
surface_temperature_c = 18.0
station_name = "Scripps Pier"
is_quality_checked = True

surface_temperature_f = surface_temperature_c * 9 / 5 + 32
surface_temperature_k = surface_temperature_c + 273.15

print(surface_temperature_f, surface_temperature_k)
print(type(surface_temperature_c), type(station_name), type(is_quality_checked))

# %% [markdown]
# Names such as `surface_temperature_c` preserve the quantity, context, and unit. A bare name such as `x` makes unit mistakes easier. At 0 °C, the known checks are 32 °F and 273.15 K.

# %% [markdown]
# ## Lists, arrays, indexing, and Boolean selection

# %%
temperature_list = [15.0, 15.4, 16.1]
temperature_array = np.array([15.0, 15.4, 16.1])
print(temperature_list * 2)   # repeat the list
print(temperature_array * 2)  # multiply each numeric value

# %%
pier_temperature_c = np.array([15.0, 15.4, np.nan, 16.1, 16.8, 17.0])
print("shape/dtype:", pier_temperature_c.shape, pier_temperature_c.dtype)
print("first/last:", pier_temperature_c[0], pier_temperature_c[-1])
print("positions 1–3:", pier_temperature_c[1:4])
print("at least 15.5 °C:", pier_temperature_c[pier_temperature_c >= 15.5])

# %% [markdown]
# The one-dimensional shape is `(6,)`. Index zero is the first value; a slice such as `[1:4]` includes positions 1, 2, and 3. A comparison creates a Boolean mask with one truth value per array position. `NaN >= 15.5` is false, so that selection omits the missing value.

# %% [markdown]
# ## Missing values and flags

# %%
print("ordinary mean:", np.mean(pier_temperature_c))
print("missing-aware mean:", np.nanmean(pier_temperature_c))
print("number missing:", np.isnan(pier_temperature_c).sum())

temperature_c = np.array([15.0, 15.4, 15.7, 16.1, 16.8, 17.0])
quality_flag = np.array([0, 0, 3, 0, 1, 0])
good = quality_flag == 0
print("good values:", temperature_c[good])
print("flagged values:", temperature_c[~good])

# %% [markdown]
# `NaN` means missing, not zero. The ordinary mean propagates the missing result; `nanmean` excludes missing positions. That exclusion is appropriate only after inspecting the amount and pattern of missingness. Flag `0` can be treated as good here because the hypothetical documentation defined it that way—not because zero always means good.

# %% [markdown]
# ## Loop, vectorized calculation, and function

# %%
celsius_values = np.array([0.0, 10.0, 20.0, 30.0])
fahrenheit_loop = []
for value in celsius_values:
    fahrenheit_loop.append(value * 9 / 5 + 32)
fahrenheit_loop = np.array(fahrenheit_loop)

fahrenheit_array = celsius_values * 9 / 5 + 32
np.testing.assert_allclose(fahrenheit_loop, fahrenheit_array)
print(fahrenheit_array)


# %%
def celsius_to_fahrenheit(values):
    """Convert a number or array-like Celsius input to a NumPy array in °F."""
    values = np.asarray(values)
    return values * 9 / 5 + 32

result = celsius_to_fahrenheit([0.0, 100.0])
assert result.shape == (2,)
np.testing.assert_allclose(result, [32.0, 212.0])
print(result)

# %% [markdown]
# The function does not mutate its input: the expression creates and returns a new array. For `original = np.array([0.0, 10.0])`, `original` remains `[0., 10.]` and the converted result is `[32., 50.]`. A loop is useful when each step needs distinct logic; the vectorized expression is clearer for one mathematical transformation applied to every value.

# %% [markdown]
# ## Core challenge solution

# %%
daily_surface_c = np.array([15.2, 15.8, np.nan, 16.4, 17.1, 16.7])
print("shape/dtype/missing:", daily_surface_c.shape, daily_surface_c.dtype, np.isnan(daily_surface_c).sum())
daily_surface_f = celsius_to_fahrenheit(daily_surface_c)
warm_days_c = daily_surface_c[daily_surface_c > 16.0]
mean_c = np.nanmean(daily_surface_c)
assert daily_surface_f.shape == daily_surface_c.shape
assert celsius_to_fahrenheit(0.0) == 32.0
print(daily_surface_f, warm_days_c, mean_c)

# %% [markdown]
# ## Continuation solution: sub-daily to daily means

# %%
subdaily_c = np.array([
    15.0, 15.2, 15.4, 15.3,
    15.5, np.nan, 15.9, 15.8,
    16.0, 16.1, 16.4, 16.3,
])
subdaily_2d = subdaily_c.reshape(3, 4)
daily_means_array = np.nanmean(subdaily_2d, axis=1)
daily_means_loop = np.array([np.nanmean(day) for day in subdaily_2d])
np.testing.assert_allclose(daily_means_array, daily_means_loop)
print(subdaily_2d)
print(daily_means_array)

# %% [markdown]
# After reshaping, axis 0 identifies the three days and axis 1 contains the four measurements within each day. Reducing with `axis=1` combines the four within-day positions and leaves one mean for each day.
