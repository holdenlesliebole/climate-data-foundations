# Friday instructor run-of-show

Assumption: approximately 20 students, ten pairs, and three instructors. Mark leads theory. The
application connects annual Scripps Pier surface SST with NASA global temperature anomaly, then
transitions into individual final-analysis work. The Scripps Mauna Loa CO₂ comparison is the
continuation lane, not a hidden core requirement.

## Preflight

- Mark reviews `notes/statistics_foundations_2.md` and confirms notation, regression-assumption
  depth, and treatment of common trends/first differences.
- Run `notebooks/09_relationships.ipynb` from a fresh kernel with the current Pier archive and fresh
  NASA/Scripps downloads.
- Verify the official NASA GISTEMP and Scripps Mauna Loa URLs, current file headers, citation notes,
  and licenses. Preserve authorized recovery copies outside Git.
- Confirm that the Pier archive contains enough good surface observations for at least 20 years to
  meet the stated 180-day threshold; prepare a documented threshold adjustment only if needed.
- Open `notebooks/10_final_analysis.ipynb` and verify every assignment route has an accessible source
  or authorized recovery path.
- Decide the submission route and deadline; put both in writing before class.
- Prepare a scope board with small Pier, Pier/global-climate, MOP-distribution, and ERA5 prompts.
  Small prompts can earn full credit.

## Session 1: relationships, regression, trend, and time dependence theory

**Minimum viable takeaway:** correlation and a line summarize a selected relationship; slope units,
residual patterns, shared trend, dependence, and study design bound what can be claimed.

**Core checkpoint by minute 75:** students can interpret a slope with units, define a residual, and
explain why two trending records can correlate without establishing causation.

| Time | Mark | Students | Supporting instructors |
|---|---|---|---|
| 0–8 | Compare scatterplots with similar $r$ but different time order | Predict what $r$ misses | Collect reasoning |
| 8–24 | Covariance, standardization, correlation | Track sign/units under conversion | Surface unit confusion |
| 24–36 | Least-squares Pier/GISTEMP worked example | Calculate fitted value and residual | Check observed-minus-fitted sign |
| 36–40 | Unit-conversion concept poll | Vote/explain/revote | Report pattern |
| 40–44 | Break | Reset | Confirm Pier and NASA files for next session |
| 44–56 | Residual patterns and inference assumptions | Diagnose residual gallery | Separate raw normality misconception |
| 56–68 | Shared trend, first differences, autocorrelation | Compare levels/change questions | Emphasize that differencing is not magic |
| 68–75 | Confounding, CO₂, and causal attribution | Rewrite an overclaim | Connect statistical and physical evidence |
| 75–80 | Notebook bridge and exit ticket | Name supported and unsupported claim | Collect individual responses |

### Theory cut order

- Cut the least-squares derivation first.
- Preserve slope units, residual definition, plots before coefficients, shared-trend caution,
  dependence, and association-versus-causation.
- If first differences are unclear, calculate one two-year difference by hand before discussing the
  correlation comparison.
- If residual sign is unclear, use one observed/fitted number before moving to assumptions.

## Session 2: Pier/global-temperature relationship and final-analysis studio

**Minimum viable takeaway:** a credible small analysis is a transparent chain from question/source
through inspection and matching to evidence, sensitivity, and a bounded claim.

**Core checkpoint by minute 38:** pairs have two annual series, a verified year merge, a colored
scatterplot and fitted slope with units, a residual view, and a levels-versus-changes statement.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–8 | Map Mark's symbols to global anomaly, Pier SST, fitted values, residuals | Audit source files/metadata | Recovery only after focused check |
| 8–17 | Guide annual coverage rule and one-to-one year merge | Build/verify matched table | Ask what one row means |
| 17–27 | Guide time plots, scatter, $r$, line, slope units | Predict, fit, interpret | Require time plot before coefficient |
| 27–38 | Residual/time view and first-difference sensitivity | Diagnose and compare | Ask what scientific question changed |
| 38–42 | Partner rubric check | One question and one required fix | Approve small scope |
| 42–46 | Break | Transition to own notebook | Form support zones |
| 46–63 | Assignment studio | Work individually; may discuss/pair-code | Approve question, unblock data/code |
| 63–72 | Structured peer check | Run/inspect; leave question + required fix | Match peers across datasets if possible |
| 72–78 | Revision and restart/run | Implement one fix; final Git commit | Help preserve evidence if failure remains |
| 78–80 | Submit and reflect | One choice + one limitation | Confirm receipt, not polish |

### Recovery and cut order

- If NASA download fails, copy the dated recovery response to `data/raw/climate/` and record
  `instructor_recovery`; do not pretend it came from the live provider.
- If the Pier archive is absent after focused diagnosis, use the recovery archive with its original
  preamble intact.
- Cut the Mauna Loa CO₂ continuation first. Preserve annualization/coverage, matching, time plot,
  slope units, residual inspection, levels-versus-changes comparison, limitation, and studio time.
- If the 180-day threshold leaves too few years, inspect the coverage plot before adopting a lower
  threshold and label the change as a sensitivity/teaching decision.
- Do not let a student spend the whole studio acquiring a novel dataset. Reduce scope to one
  existing course route and one main figure.

## Studio support zones

- Instructor 1: Pier loading, flags, annual coverage, paired differences, intervals.
- Instructor 2: NASA/Scripps text formats, annual year merges, correlation/regression.
- Instructor 3: MOP distributions, ERA5/prepared subset, notebook execution, Git/submission rover.
- Regroup after ten minutes if one queue is empty or overloaded.

## Friday debrief

- Did theory vocabulary appear correctly in student interpretations?
- Did students distinguish global anomaly from local absolute SST?
- How many students compared levels with changes without calling differencing a causal correction?
- Which source/loading step generated the most setup time?
- Which claims most often exceeded the evidence?
- What must change before the next course offering?
