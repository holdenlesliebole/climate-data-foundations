# Thursday instructor run-of-show

Assumption: approximately 20 students, ten pairs, and three instructors. Mark leads the theory
session. The application session uses each student's untouched Pier temperature file acquired on
Monday; it does not depend on the morning mathematics curriculum.

## Preflight

- Mark reviews `notes/statistics_foundations_1.md` and confirms notation, confidence-interval
  language, and the intended bootstrap depth.
- Run `notebooks/07_data_health.ipynb` and `notebooks/08_uncertainty.ipynb` from a fresh kernel using
  the current provider Pier CSV.
- Confirm at least ten complete years have paired, good-flag June–August observations. If not, widen
  the season or reduce the minimum-year assertion and document the change.
- Prepare one clearly labeled generated error card; never place an altered file in `data/raw/`.
- Confirm the instructor recovery route and redistribution permission. Offer it only after the
  acquisition/path checkpoint.
- Put the theory symbol-to-code table on the board before Session 2.

## Session 1: distributions, sampling, and uncertainty theory

**Minimum viable takeaway:** a statistic estimates a target from a sample; its uncertainty depends
on observed variability and assumptions about how the sample/resampling units relate to the target.

**Core checkpoint by minute 72:** students can distinguish observation spread from uncertainty of a
mean and can name a defensible Pier resampling unit.

| Time | Mark | Students | Supporting instructors |
|---|---|---|---|
| 0–8 | Show two distributions with the same mean; elicit missing information | Commit to a prediction | Collect responses without correcting |
| 8–25 | Population/sample, center, spread, quantiles, units | Calculate/check four-value example | Listen for variance-unit confusion |
| 25–36 | Work the Pier difference summary; distinguish mean/median and SD/IQR | Fill one formula step and interpret units | Novice proxy restates terms plainly |
| 36–40 | Concept poll: SD versus SE | Vote, explain to neighbor, revote | Report reasoning pattern to Mark |
| 40–44 | Break | Reset | Triage only setup for next session |
| 44–60 | Sampling distributions, SE, interval coverage | Label observation distribution versus sampling distribution | Flag “95% of data” misconception |
| 60–72 | Bootstrap diagram and repeated-sample example | Identify statistic and resampling unit | Ask why daily rows may not be independent |
| 72–77 | Map notation to Thursday notebooks | Name code object for each symbol | Display written mapping |
| 77–80 | Exit ticket | Individual response | Sort by misconception, not score |

### Theory cut order

- Cut the $1/\sqrt{n}$ derivation and bootstrap implementation details first.
- Preserve units, SD-versus-SE, interval interpretation, resampling unit, and dependence.
- If fewer than half distinguish SD and SE at minute 40, replace the first post-break example with a
  second concrete repeated-sampling diagram.

## Session 2: Pier data health and uncertainty

**Minimum viable takeaway:** uncertainty is the final step in a visible chain of choices about the
target, usable observations, grouping, statistic, and resampling unit.

**Core checkpoint by minute 60:** every pair has a data-health table, a plotted paired difference,
and a year-level bootstrap interval with its resampling unit written down.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–8 | Translate $x_i,n,\bar{x},s$ into code names; predict ranges | Annotate symbol map | Resolve only missing-file blockers |
| 8–22 | Guide data-health notebook | Inspect source, dates, missingness, flags, duplicates | Require evidence before filtering |
| 22–36 | Compare surface/bottom distributions and paired differences | Plot and describe center/spread/shape | Ask for units and observational unit |
| 36–40 | Extreme versus injected-error card | Choose investigate/retain/exclude with reason | Prevent editing raw data |
| 40–44 | Break | Switch driver/navigator | Check pair progress |
| 44–60 | Guide annual summer means and year bootstrap | Calculate interval; label estimate/unit/assumption | Help with grouping, not interpretation text |
| 60–71 | Compare iid-day and year-resampling sensitivity | Explain why widths/estimates differ | Connect dependence to Mark's diagram |
| 71–77 | Data-health and three-sentence uncertainty statement | Peer check against four required ingredients | Open continuation only after core |
| 77–80 | Exit ticket | Individual response | Record Friday follow-up needs |

### Recovery and cut order

- After a three-minute focused path/header diagnostic, use the authorized recovery file and record
  `instructor_recovery` in the manifest.
- If too few valid years remain, use all months while preserving the year as the resampling unit;
  state the changed target.
- Cut the iid-versus-year comparison and continuation block bootstrap first. Preserve data health,
  a distribution/time view, annual grouping, one interval, and a bounded interpretation.
- Do not label an unusual provider value “bad” without flag/metadata/context evidence. Investigate
  the injected 180 °C value separately and keep altered teaching data out of raw storage.

## Anticipated stuck points

| Stuck point | First response | Fallback |
|---|---|---|
| Students report `describe()` without units | Ask what one row represents and write the unit beside every number | Give the symbol-to-code card |
| SD and SE are interchanged | Ask whether the number describes days or repeated estimated means | Return to the two-distribution diagram |
| `groupby("year")` feels magical | Have students write one row/year on paper before code | Display the first three annual groups |
| Bootstrap is treated as “more data” | Ask how many original independent units exist | Draw repeated reuse of the same year cards |
| Narrow daily interval is called better | Ask which dependence assumption created the width | Require a sensitivity sentence, not a winner |

## Thursday debrief

- Which notation needs changing before Friday?
- Could students name the estimate, observation unit, resampling unit, and limitation?
- How many pairs reached the year-level interval by minute 60?
- Which data issue dominated: missing Pier file, header, flags, dates, or grouping?
- Should Friday begin with another dependence example?
