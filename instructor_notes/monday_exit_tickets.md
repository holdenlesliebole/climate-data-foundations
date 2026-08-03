# Monday exit tickets and interpretation guide

Collect individually in the final three minutes. Names are optional for the concept result; provide a
separate private route for students requesting help.

## Session 1 primary ticket

Without running code:

```python
original = np.array([0.0, 10.0])
converted = celsius_to_fahrenheit(original)
```

1. What are `original` and `converted` afterward?
2. Did the function mutate `original`? Explain using one line of the function.

**Expected:** `original` remains `[0., 10.]`; `converted` is `[32., 50.]`. `np.asarray` may return a
view/reference when the input is already an array, but the arithmetic expression creates a new result
and no assignment writes into `values` or `original`.

**Use the responses:**

- If fewer than half distinguish input/output, begin Monday 2 with a two-minute variable-state trace.
- If most values are correct but explanations are weak, ask students to point to assignment versus
  mutation in Tuesday's debugging task.
- Do not spend Tuesday teaching NumPy memory/view details unless they caused an actual error.

### Alternate Session 1 ticket

Why does `np.mean([15.0, np.nan, 17.0])` return `NaN`, and when would `np.nanmean` still be a poor
scientific choice?

**Expected:** ordinary mean propagates missingness; `nanmean` excludes missing positions, but can be
misleading if much data are missing or missingness is patterned/non-random.

## Session 2 primary ticket

What scientifically useful information from today's Pier archive would have been lost if you
received only an already-loaded tidy DataFrame? Give one concrete example and say where you found it.

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
