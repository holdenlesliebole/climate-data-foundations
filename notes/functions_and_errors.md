# Errors, functions, and checks

A reference for the two skills that determine whether you can work alone: getting unstuck when
something breaks, and packaging work so you stop retyping it. Written to be useful in March, when
you remember the task but not the syntax.

## Part 1 — Reading an error message

### The rule: last line first

A traceback is a report, not a verdict. Its **last line** is the finding. Everything above it is the
chain of calls that led there, and much of that chain is inside pandas or matplotlib — not in your
code and not where your bug is.

```text
Traceback (most recent call last):
  File "analysis.py", line 12, in <module>      ← your code: start looking here
    mean = frame["SURFACE_TEMP_C"].mean()
  File ".../pandas/core/frame.py", line 4113    ← library internals: ignore on the first pass
    indexer = self.columns.get_loc(key)
KeyError: 'SURFACE_TEMP_C'                      ← READ THIS FIRST
```

Then work in this order, every time:

1. **Name the error type.** `KeyError` and `FileNotFoundError` are different problems.
2. **Read what Python quoted back.** It is quoting *your* string, not the correct one.
3. **Find the last line that names one of your own files.** That is where to look.
4. **Print one thing** to test your explanation before editing any code.

If you cannot say the failure in a sentence, any edit you make is a guess.

### The errors you will actually hit

| Error | Usually means | First thing to print |
|---|---|---|
| `NameError: name 'x' is not defined` | typo, or the cell defining it never ran | the name, character by character |
| `FileNotFoundError` | wrong working directory, not a missing file | `Path.cwd()` |
| `KeyError: 'COLUMN'` | column name does not match exactly | `list(frame.columns)` |
| `AttributeError: ... has no attribute ...` | wrong type of object, or a misspelled method | `type(thing)` |
| `TypeError: unsupported operand type(s)` | numbers loaded as text | `frame.dtypes` |
| `ValueError: could not convert string to float` | a missing-value marker such as `-99.99` or `NaN` in a numeric column | the raw text of a few rows |
| `IndentationError` / `SyntaxError` | Python could not read the code at all | the line *above* the one reported |
| `ModuleNotFoundError` | wrong environment or kernel selected | `sys.executable` |

Two notes on the last two. A `SyntaxError` often points at the line *after* the real problem —
an unclosed bracket on line 9 is reported on line 10. And `ModuleNotFoundError` for a package you
know is installed is almost always the kernel selector in the top-right of VS Code, not the package.

### What not to do

- Do not read the traceback top-down and panic at the library paths.
- Do not change code before you can name the failure.
- Do not reinstall packages. A `KeyError` is evidence about a string.
- Do not conclude anything about your ability. Everyone produces these daily; the difference
  between a beginner and an expert is how fast they read the last line.

### The three-print diagnostic

Nearly every stuck moment in this course is answered by one of these:

```python
print(Path.cwd())              # where am I?
print(list(frame.columns))     # what is actually in this object?
print(frame.dtypes)            # is this a number or is it text?
```

## Part 2 — Functions

### Anatomy

```python
def surface_minus_bottom(surface_c, bottom_c):   # header: name and parameters
    """Return the surface-minus-bottom difference in °C."""   # docstring
    return surface_c - bottom_c                  # body, and the value handed back
```

- **Defining runs nothing.** `def` creates a name. The body executes only when you *call* it with
  parentheses: `surface_minus_bottom(16.2, 15.1)`.
- **Parameters are placeholders.** `surface_c` exists only inside the function. Printing it
  afterwards raises `NameError`.
- **Without `return`, a function hands back `None`.** This is the most common silent failure in a
  first year of Python: `answer = my_function(x)` puts `None` into `answer`, and the error appears
  three cells later somewhere unrelated.
- **A function should use only what it was given.** If the body mentions a variable that is not a
  parameter, it quietly reaches outside itself and works on whatever that name happens to be at call
  time. This is the real cause of "but it worked yesterday."

### When to write one

Write a function when you have copied a block and changed one or two things in it. Not for elegance
— for **consistency**. A copied block drifts: one copy loses its unit label, another loses its grid,
and the drift is invisible in the output. One definition cannot disagree with itself.

Keep it in the notebook while you are still deciding what it should do. Move it into `src/` when two
different notebooks need it.

### Default arguments

```python
def plot_series(dates, values, label, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 3))
    ...
```

`ax=None` lets simple callers ignore the parameter and lets careful callers control it. This is the
standard way to write a plotting helper that works both as a one-liner and inside a multi-panel
figure.

## Part 3 — Checks

### `assert` for your own reasoning

```python
assert observed.between(-2.0, 40.0).all(), (
    f"Values outside -2 to 40 °C (observed {observed.min():.1f} to {observed.max():.1f}). "
    "Check the units before plotting."
)
```

A good check has three properties:

1. **It encodes physics, not code.** The range comes from what seawater can be, not from anything
   about pandas.
2. **Its message names the evidence.** Print the observed values so the reader diagnoses the problem
   from the message alone.
3. **It could actually fire.** If you cannot describe a value it would reject, it is decoration.
   `assert values.between(-1000, 1000).all()` protects nothing.

A check that fires on legitimate data is worse than no check, because people learn to comment it
out. When one fires, ask what the number physically means — not what range would make the message
go away.

### `assert` versus `ValueError`

| | Use for | Why |
|---|---|---|
| `assert` | checking your own reasoning inside an analysis | compact; can be disabled with `python -O` |
| `raise ValueError(...)` | telling a caller their request was invalid | always runs; part of the function's contract |

Validation that other people depend on should not be written with `assert`.

### What a passing check establishes

Only the one thing it tested. A plausible-range check says nothing about calibration, completeness,
flag handling, representativeness, independence, or whether your interpretation follows. This is not
a caveat to recite — it is the reason a check is worth writing down. A check with a stated boundary
is a claim you can defend.

## Checklist: before you ask for help

Bring these five things and most problems answer themselves on the way:

1. the **last line** of the error, copied exactly;
2. the smallest piece of code that still fails;
3. `Path.cwd()`;
4. which environment/kernel is selected;
5. what you already checked and what you expected instead.
