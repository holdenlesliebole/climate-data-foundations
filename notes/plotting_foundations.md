# Choosing and improving a plot

A plot is not decoration added after analysis. It is a way to ask a particular question of data.
Start with the question, choose a format whose geometry matches it, and then make the scientific
meaning readable.

## The six-question figure check

Use this every time you make a figure, in every session of the week. It takes about a minute and it
is the habit this course is actually trying to install.

1. **What question does this figure answer?**
2. **What does each axis represent, including units?**
3. Is a line, scatterplot, histogram, or field plot the right format for that question?
4. Are missing or flagged values being hidden?
5. **What is the one-sentence interpretation?**
6. **What can this figure *not* establish?**

Questions 1, 2, 5, and 6 are asked every time. Questions 3 and 4 rotate as the focus of the day —
your instructor will name which one is in play, and they become automatic soon enough.

Question 6 is the one worth protecting when time is short. A figure that shows a relationship
between two series cannot by itself establish which caused which, whether a third factor drives
both, or whether the pattern holds outside the plotted window. Saying so out loud is not hedging; it
is the difference between a result and a claim.

## Match the format to the question

| Question | Useful first format | What each mark means | Common mistake |
|---|---|---|---|
| How did a quantity change through time? | Line plot | A position in time joined to neighboring observations | Connecting categories or unrelated samples as though time were continuous |
| Which values are common or unusual? | Histogram | The count of observations inside a numeric interval | Treating bin boundaries as natural categories |
| Do two measured quantities vary together? | Scatterplot | One paired observation | Drawing a causal conclusion from an association |
| How do named groups compare? | Bar chart | A summary for one category | Using bars for a continuous time series |
| How does a field vary across two coordinates? | Image or `pcolormesh` | A value represented by color at each coordinate pair | Using color without units, a colorbar, or readable limits |
| Which directions occur? | Polar plot or directional histogram | An angle and often a magnitude or count | Averaging directions as ordinary linear numbers |

These are starting points, not laws. More elaborate graphics are useful only when they make the
question easier to answer.

## The minimum viable scientific figure

Before sharing a figure, check that it has:

- a title that states the subject rather than “My plot”;
- an x-axis label and y-axis label;
- units for every physical quantity;
- a legend when more than one series or group appears;
- a source note or a nearby caption;
- a visible treatment of missing or flagged values;
- a caption that says one thing the figure shows and one thing it cannot establish.

## One dataset, three different questions

Suppose `pier` is a pandas DataFrame with `date`, `SURF_TEMP_C`, and `BOT_TEMP_C` columns.

### Change through time: line plot

```python
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(pier["date"], pier["SURF_TEMP_C"], label="Surface")
ax.set(xlabel="Date", ylabel="Temperature (°C)", title="Scripps Pier surface temperature")
ax.legend()
```

The horizontal position represents time, so connecting successive observations helps the eye follow
change. A line does not prove that values between observations were measured.

### Common and unusual values: histogram

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(pier["SURF_TEMP_C"].dropna(), bins=20, edgecolor="white")
ax.set(xlabel="Surface temperature (°C)", ylabel="Number of observations",
       title="Distribution of Scripps Pier surface temperature")
```

Changing `bins` changes the visible shape. Try 5, 20, and 60 bins before deciding what features are
stable enough to describe.

### Paired variation: scatterplot

```python
paired = pier.dropna(subset=["SURF_TEMP_C", "BOT_TEMP_C"])
fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(paired["SURF_TEMP_C"], paired["BOT_TEMP_C"], alpha=0.5)
ax.set(xlabel="Surface temperature (°C)", ylabel="Bottom temperature (°C)",
       title="Paired Scripps Pier temperatures")
```

Each point must represent a surface and bottom value from the same row. The scatterplot can show an
association; it cannot by itself explain the process that produced it.

## A useful plotting routine

Use the same short loop throughout the course:

```text
state the question
→ predict the useful format
→ make the simplest version
→ label quantities and units
→ inspect missingness and flags
→ change one design choice
→ write one finding and one limitation
```

When a plot is confusing, return to the question before adding colors, panels, fitted lines, or other
features.

## When the plotting code repeats

By the middle of the week you will have copied a plotting block more than once. That is the signal
to give it a name:

```python
def plot_series(dates, values, label, title, ax=None, ylabel="Temperature (°C)"):
    """Plot one labeled series, creating a figure only when no axes are supplied."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 3))
    ax.plot(dates, values, lw=1.2, label=label)
    ax.set(title=title, xlabel="Date", ylabel=ylabel)
    ax.legend()
    ax.grid(alpha=0.25)
    return ax
```

The reason is consistency, not elegance. Copied blocks drift — one loses its unit label, another
loses its grid — and the drift is invisible in the figure. One definition cannot disagree with
itself, and one edit changes every panel.

The `ax=None` default lets the same function make a standalone figure or draw into a panel of a
larger one. See [errors, functions, and checks](functions_and_errors.md) for the anatomy of a
function and for the checks worth putting inside a plotting helper.
