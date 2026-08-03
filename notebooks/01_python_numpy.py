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
# # Python as a scientific calculator
#
# This session introduces the small amount of Python vocabulary we need to work with climate data: named values, arrays, missing values, selections, loops, and functions.
#
# **Minimum viable takeaway:** put values in clearly named objects, transform collections of values, and check that the result has the expected shape, units, and one known value.
#
# We will repeatedly use: **Predict → Run → Explain → Modify → Check**.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - run notebook cells deliberately and recognize when order matters;
# - use variables, numbers, strings, booleans, lists, and NumPy arrays;
# - inspect an array's shape, data type, values, and missingness;
# - read a short `for` loop and make the same calculation with an array;
# - call and modify a small function;
# - check a result using units, shape, and a known answer.

# %% [markdown]
# ## 1. Notebook state: predict before running
#
# What will each expression return? Commit to an answer before running the cell.
#
# - `2 + 3 * 4` → **TODO**
# - `(2 + 3) * 4` → **TODO**
# - `10 / 4` → **TODO**

# %%
print(2 + 3 * 4)
print((2 + 3) * 4)
print(10 / 4)

# %% [markdown]
# Python follows an order of operations, and parentheses make your intent visible. In scientific code, readable intent is more important than squeezing an expression onto one line.

# %% [markdown]
# ## 2. Variables carry values; names should carry meaning
#
# A variable is a name referring to a value. Include the quantity and often the unit in the name.

# %%
surface_temperature_c = 18.0
station_name = "Scripps Pier"
is_quality_checked = True

surface_temperature_f = surface_temperature_c * 9 / 5 + 32
surface_temperature_k = surface_temperature_c + 273.15

print(station_name)
print("Celsius:", surface_temperature_c)
print("Fahrenheit:", surface_temperature_f)
print("Kelvin:", surface_temperature_k)
print("Quality checked:", is_quality_checked)

# %% [markdown]
# ### Pair task: modify and check
#
# 1. Change the Celsius value to `0.0` and rerun. What known Fahrenheit and Kelvin values should appear?
# 2. Change it back to `18.0`.
# 3. Explain why a name like `surface_temperature_c` is safer than `x` or `temperature`.
#
# **Explanation:** TODO

# %%
print(type(surface_temperature_c))
print(type(station_name))
print(type(is_quality_checked))

# %% [markdown]
# `float`, `str`, and `bool` describe different kinds of values. Types affect which operations make sense. Multiplying a temperature by a number is meaningful; multiplying a station name produces repeated text, not science.

# %% [markdown]
# ## 3. Lists and arrays are not interchangeable
#
# Predict the two results below. Will both multiply every temperature by two?

# %%
import numpy as np

temperature_list = [15.0, 15.4, 16.1]
temperature_array = np.array([15.0, 15.4, 16.1])

print("list * 2 :", temperature_list * 2)
print("array * 2:", temperature_array * 2)

# %% [markdown]
# A Python list is a general container. A NumPy array represents a regularly structured collection and supports element-by-element scientific calculations. We will use both, but for different jobs.
#
# **Explain the difference in your own words:** TODO

# %%
pier_temperature_c = np.array([15.0, 15.4, np.nan, 16.1, 16.8, 17.0])

print("values:", pier_temperature_c)
print("shape:", pier_temperature_c.shape)
print("number of dimensions:", pier_temperature_c.ndim)
print("data type:", pier_temperature_c.dtype)
print("number of values:", pier_temperature_c.size)

# %% [markdown]
# `shape` answers how many entries lie along each dimension. Here `(6,)` means one dimension containing six positions. The comma distinguishes a one-dimensional shape from an ordinary number in Python.

# %% [markdown]
# ## 4. Index, slice, and select
#
# Python counts positions from zero. A slice includes its start and excludes its end. Predict each result before running.

# %%
print("first value:", pier_temperature_c[0])
print("last value:", pier_temperature_c[-1])
print("positions 1 through 3:", pier_temperature_c[1:4])
print("every second position:", pier_temperature_c[::2])

# %% [markdown]
# ### Boolean selection
#
# A comparison against an array creates one `True`/`False` value per position. The Boolean array can then select matching values.

# %%
warm = pier_temperature_c > 16.0
print("mask:", warm)
print("selected values:", pier_temperature_c[warm])

# %% [markdown]
# Modify the threshold to answer: which recorded temperatures are at least 15.5 °C?
#
# **Code/result:** TODO

# %% [markdown]
# ## 5. Missing is not zero
#
# `NaN` means a numeric value is missing or unavailable. It does not mean the measured temperature was zero. Predict the two means below.

# %%
print("ordinary mean:", np.mean(pier_temperature_c))
print("NaN-aware mean:", np.nanmean(pier_temperature_c))
print("missing mask:", np.isnan(pier_temperature_c))
print("number missing:", np.isnan(pier_temperature_c).sum())

# %% [markdown]
# A missing-aware function can be appropriate, but it is a scientific choice—not a ritual. Always inspect how much is missing and whether the missingness has a pattern before summarizing.

# %% [markdown]
# ## 6. Quality flags: keep values and evidence together
#
# Suppose `0` means good and nonzero values require attention. Predict which temperatures the next cell retains.

# %%
temperature_c = np.array([15.0, 15.4, 15.7, 16.1, 16.8, 17.0])
quality_flag = np.array([0, 0, 3, 0, 1, 0])

good = quality_flag == 0
print("good mask:", good)
print("good temperatures:", temperature_c[good])
print("flagged temperatures:", temperature_c[~good])

# %% [markdown]
# Selecting `flag == 0` is only defensible after reading the provider's flag definitions. A flag may mean questionable, a different collection method, or simply not evaluated. Never invent the meaning from the number.

# %% [markdown]
# ## 7. An explicit loop and an array calculation
#
# A loop makes repeated steps visible. Read the loop aloud: “for each value in the Celsius array, calculate Fahrenheit and append it to the output list.”

# %%
celsius_values = np.array([0.0, 10.0, 20.0, 30.0])
fahrenheit_loop = []

for value in celsius_values:
    converted = value * 9 / 5 + 32
    fahrenheit_loop.append(converted)

fahrenheit_loop = np.array(fahrenheit_loop)
print(fahrenheit_loop)

# %%
fahrenheit_array = celsius_values * 9 / 5 + 32
print(fahrenheit_array)

np.testing.assert_allclose(fahrenheit_loop, fahrenheit_array)
print("CHECK PASSED: the loop and array calculation agree.")


# %% [markdown]
# The array expression is shorter and closely states the mathematical transformation. Loops remain useful when each iteration requires different logic or when clarity improves. “Never use loops” is not the lesson.

# %% [markdown]
# ## 8. Put a named transformation in a function
#
# A function makes inputs, outputs, and intent visible. This one accepts a number, list, or array because `np.asarray` gives the calculation a consistent representation.

# %%
def celsius_to_fahrenheit(values):
    """Convert temperature values from degrees Celsius to Fahrenheit."""
    values = np.asarray(values)
    return values * 9 / 5 + 32

converted = celsius_to_fahrenheit([0.0, 10.0, 20.0])
print(converted)

# %% [markdown]
# ### Check more than “it ran”
#
# We know water freezes at 0 °C = 32 °F and boils near standard pressure at 100 °C = 212 °F. We also expect one output per input.

# %%
known_celsius = np.array([0.0, 100.0])
known_fahrenheit = np.array([32.0, 212.0])
result = celsius_to_fahrenheit(known_celsius)

assert result.shape == known_celsius.shape
np.testing.assert_allclose(result, known_fahrenheit)
print("CHECK PASSED: shape and two known values are correct.")

# %% [markdown]
# ### Pair modification
#
# Modify the function so its docstring states the accepted input and returned unit. Then test it on `[-40, np.nan, 37]`. Explain what happens to `NaN` and why.
#
# **Explanation:** TODO

# %% [markdown]
# ## Core challenge: inspect, convert, select, check
#
# The array below represents six daily surface temperatures with one missing observation.
#
# 1. Print its shape, data type, and missing count.
# 2. Convert it to Fahrenheit using the function.
# 3. Select the recorded Celsius values greater than 16 °C.
# 4. Calculate a missing-aware mean in Celsius.
# 5. Add one check that would catch a clearly wrong conversion.

# %%
daily_surface_c = np.array([15.2, 15.8, np.nan, 16.4, 17.1, 16.7])

# TODO: change or add to this scaffold as needed.
print("shape:", daily_surface_c.shape)
print("dtype:", daily_surface_c.dtype)
print("missing:", np.isnan(daily_surface_c).sum())

daily_surface_f = celsius_to_fahrenheit(daily_surface_c)
warm_days_c = daily_surface_c[daily_surface_c > 16.0]
mean_c = np.nanmean(daily_surface_c)

print("Fahrenheit:", daily_surface_f)
print("recorded values > 16 °C:", warm_days_c)
print("mean °C:", mean_c)

assert daily_surface_f.shape == daily_surface_c.shape
assert celsius_to_fahrenheit(0.0) == 32.0
print("CHECK PASSED")

# %% [markdown]
# ## Exit ticket
#
# Without running code, predict the output and explain whether the input changes:
#
# ```python
# original = np.array([0.0, 10.0])
# converted = celsius_to_fahrenheit(original)
# ```
#
# - `original` is: **TODO**
# - `converted` is: **TODO**
# - The input did/did not change because: **TODO**

# %% [markdown]
# ## Continuation lane: sub-daily to daily means
#
# The 12 values below contain four measurements on each of three days.
#
# 1. Reshape them to `(3, 4)`.
# 2. Calculate one missing-aware mean per day using `axis=1`.
# 3. Write a loop that produces the same result.
# 4. Check that both approaches agree.
# 5. Explain why `axis=1` is the correct direction.

# %%
subdaily_c = np.array([
    15.0, 15.2, 15.4, 15.3,
    15.5, np.nan, 15.9, 15.8,
    16.0, 16.1, 16.4, 16.3,
])

# TODO: implement the five continuation steps.
subdaily_2d = subdaily_c.reshape(3, 4)
daily_means_array = np.nanmean(subdaily_2d, axis=1)

daily_means_loop = []
for day in subdaily_2d:
    daily_means_loop.append(np.nanmean(day))
daily_means_loop = np.array(daily_means_loop)

np.testing.assert_allclose(daily_means_array, daily_means_loop)
print(subdaily_2d)
print(daily_means_array)
