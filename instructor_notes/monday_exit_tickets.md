# Monday exit tickets and interpretation guide

Collect individually in the final three minutes. Names are optional for the concept result; provide a
separate private route for students requesting help.

## Session 1 primary ticket

Suppose this code makes a plot:

```python
ax.plot(day, surface_c, label="Surface")
```

1. What scientific question is a line plot useful for here?
2. Name three labels or annotations required before sharing the figure.
3. What change is needed to compare `bottom_c` on the same axes?

**Expected:** the line format supports a question about change across the ordered days. Required
elements include a descriptive title, x-axis meaning, y-axis quantity plus °C, and a legend if both
depths appear. A second `ax.plot(day, bottom_c, label="Bottom")` pattern plus `ax.legend()` makes the
comparison visible.

**Use the responses:**

- If fewer than half connect a line to an ordered x-axis, begin Monday 2 by contrasting a time series
  with a histogram before loading the Pier data.
- If labels are treated as decoration, audit quantity and units before interpreting any Pier plot.
- If most answers are correct but code confidence is low, keep the worked plotting pattern visible
  during Monday 2 rather than asking students to recreate it from memory.

### Alternate Session 1 ticket

Which format would you choose for each question: (a) change through time, (b) which temperatures are
common, and (c) whether paired surface and bottom values vary together?

**Expected:** line plot, histogram, and scatterplot respectively, with a short explanation tied to
what one mark and each axis represent.

## Session 2 primary ticket

What scientifically useful information from today's Pier archive would have been lost if you
received only an already-loaded tidy DataFrame? Give one concrete example and say where you found it.
Then name one question answered more directly by your histogram or scatterplot than by the time
series.

**Strong examples:** citation/archive date, provider, flag meanings, time-zone caveat, sampling depth,
different start dates, collection-method note, or the fact that the file is versioned. The response
must connect the fact to the preamble, landing page, or methods—not merely say “metadata.”

**Use the responses:**

- If students name only column names, begin Tuesday 2 by contrasting values, attributes, and
  provenance.
- If many cannot identify the raw file, repeat project-relative path and manifest checks before the
  MOP request.
- If responses are scientifically rich but syntax remained difficult, keep Tuesday's request
  scaffolded and preserve the same six inspection questions.

### Alternate Session 2 ticket

Put these in defensible order and explain one dependency: plot, download, inspect flags, load local
file, record source, choose archive component.

**Expected:** choose component/record source → download → load local file, with raw/text/metadata
inspection before or alongside parsing → inspect flags/structure → plot. Provenance recording starts
at discovery and is completed after acquisition; accept answers that make this iterative nature
explicit.
