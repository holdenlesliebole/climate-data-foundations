# Final assignment: one small climate-data story

## Purpose

Use the workflow from this week to ask and answer one small question with climate or ocean data. This
is a low-stakes assignment. We are looking for a good-faith, reproducible attempt—not a novel result,
a perfect statistical model, or a polished research paper.

Choose the smallest version that interests you. The small prompts can receive full credit.

## Format and collaboration

- Complete the provided starter notebook.
- Plan for approximately 35–60 minutes of focused work. Class time will be provided on Friday.
- You may use the course notes, completed reference notebooks, documentation, classmates, instructors,
  and GitHub Copilot.
- You may discuss and pair-program, but submit your own notebook and write your own interpretation.
- Include one sentence saying how Copilot or another person helped, or that you completed the work
  without that help. This is context, not a penalty.

## Choose one direction

### A. Scripps Pier surface and bottom temperature

The Pier record contains long-running daily surface and near-bottom observations. Choose a time
window, month, or season.

**Small prompt:** Compare surface and bottom temperature for one month or season. Plot both records or
their distributions, calculate `surface temperature - bottom temperature` for paired observations,
and summarize the typical difference and its spread.

**Medium variation:** Compare the surface-bottom difference between two seasons or two time periods.
Include an interval or sensitivity check taught on Thursday.

**Open variation:** Ask another similarly sized question using surface temperature, bottom
temperature, or salinity from the archive you acquired in class.

### B. CDIP MOP waves

Use significant wave height (`waveHs`), peak period (`waveTp`), and/or peak direction (`waveDp`) from
the NetCDF file you acquired in Tuesday's MOP exercise. A documented recovery copy is equally
acceptable if the live request failed.

**Small prompt:** Using the assignment-sized MOP file acquired after Tuesday's core exercise, compare
January and July `waveHs` or `waveTp` with a time series, histogram/boxplot, and a numerical summary.
If the rolling source coverage required different months, state and use those instead.

**Medium variation:** Examine the relationship between `waveHs` and `waveTp` with a scatterplot,
correlation or fitted line, and a short residual/sensitivity check.

**Open variation:** Plot how `waveDp` is distributed or how it changes with wave height. Direction is
circular: 1° and 359° are neighbors. Do not use an ordinary arithmetic mean of directions near the
0°/360° boundary, and state the direction convention from the file metadata.

### C. ERA5

Use the supplied Southern California/eastern Pacific subset.

**Small prompt:** Compare one field or regional mean between two seasons.

**Medium variation:** Compare a selected point with a regional average or compare two locations using
the same time period and color/axis scale.

**Open variation:** Ask another similarly sized question using the variables in the course file.

### D. Your variation

Propose an equally small question using one of the course datasets and obtain instructor approval
before investing substantial time.

## Notebook checklist

Your notebook should contain these sections:

1. **Question and source**
   - What is your specific question?
   - Which dataset are you using?
   - Give its provider, landing page or exact request URL, access date, local raw filename, and
     whether you acquired it from the provider or used the recovery copy.
2. **Load and inspect**
   - Use a relative project path.
   - Display columns or dimensions, time coverage, units, flags, and missingness.
3. **Choose and transform**
   - Make at least one choice of time window, season, location, comparison, variable, or derived
     quantity.
4. **Visualize**
   - Make one relevant figure with a descriptive title, axis labels, and units.
5. **Summarize**
   - Calculate one appropriate statistic: center/spread, group difference and interval,
     correlation/regression, or another method taught this week.
6. **Interpret**
   - In four to eight sentences, describe the result, one assumption, and one limitation.
7. **Check and submit**
   - Complete a peer check and attempt one revision.
   - Restart the kernel and run the notebook from top to bottom.
   - Make a final Git commit.
   - Include your one-sentence collaboration/Copilot note.

If something still fails, do not hide it. Leave a short Markdown note explaining what you tried,
where the failure occurs, and what you think the next diagnostic step would be.

## Rubric: 10 points

| Criterion | Points |
|---|---:|
| Participated in class checkpoints and made a good-faith attempt | 2 |
| Completed a peer check and attempted a revision | 1 |
| Stated a question/source, recorded acquisition provenance, and inspected the data | 1 |
| Made one personal subset, comparison, or derived-variable choice | 1 |
| Produced a relevant, labeled figure | 2 |
| Calculated and identified one numerical summary/method | 1 |
| Wrote a bounded interpretation with an assumption or limitation | 1 |
| Submitted a notebook that substantially reruns plus a final commit | 1 |

A correctable coding or statistical mistake will not erase credit for an honest, documented attempt.
Extensions do not receive more base credit than a well-executed small prompt.

## Before submitting

- [ ] My question is small enough to answer with one main figure.
- [ ] I recorded the provider, URL, access date, local filename, and acquisition/recovery method.
- [ ] I recorded data structure, units, flags, time coverage, and missingness.
- [ ] My figure has a title, labels, and units.
- [ ] I named and interpreted my numerical summary.
- [ ] I stated at least one assumption or limitation.
- [ ] I completed a peer check and attempted a revision.
- [ ] I restarted and ran the notebook from top to bottom.
- [ ] I made a final commit and included my collaboration/Copilot note.
