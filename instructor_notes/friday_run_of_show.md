# Friday instructor run-of-show

Assumption: approximately 20 students, ten pairs, and three instructors. Mark leads theory. The
application uses the assignment-sized MOP file acquired Tuesday, then transitions into individual
final-analysis work. Students may choose Pier, MOP, or the prepared ERA5 subset for the submission.

## Preflight

- Mark reviews `notes/statistics_foundations_2.md` and confirms notation, regression-assumption
  depth, and circular-data treatment.
- Recheck D0513 coverage and ensure students have a local NetCDF with `waveHs`, `waveTp`, `waveDp`,
  and both flags. Confirm units and the direction convention from the received file attributes.
- Run `notebooks/09_relationships.ipynb` against the current assignment file from a fresh kernel.
- Open `notebooks/10_final_analysis.ipynb` and verify every assignment route has an accessible source
  or authorized recovery path.
- Decide the submission route and deadline; put both in writing before class.
- Prepare a scope board with the small Pier, MOP, and ERA5 prompts. Small prompts can earn full
  credit.

## Session 1: relationships, regression, and time dependence theory

**Minimum viable takeaway:** correlation and a line summarize a selected relationship; slope units,
residual patterns, time dependence, and study design bound what can be claimed.

**Core checkpoint by minute 75:** students can interpret a slope with units, define a residual, and
name one reason correlation does not establish causation.

| Time | Mark | Students | Supporting instructors |
|---|---|---|---|
| 0–8 | Compare scatterplots with similar $r$ but different shapes | Predict what $r$ misses | Collect reasoning |
| 8–24 | Covariance, standardization, correlation | Track sign/units under conversion | Surface unit confusion |
| 24–36 | Least-squares worked example | Calculate fitted value and residual | Check observed-minus-fitted sign |
| 36–40 | Unit-conversion concept poll | Vote/explain/revote | Report pattern |
| 40–44 | Break | Reset | Confirm MOP files for next session |
| 44–58 | Residual patterns and inference assumptions | Diagnose residual gallery | Separate raw normality misconception |
| 58–68 | Confounding, seasonality, autocorrelation, causation | Rewrite an overclaim | Connect to Thursday dependence |
| 68–75 | Circular peak direction | Explain 1°/359° failure; read convention | Display metadata excerpt |
| 75–80 | Notebook bridge and exit ticket | Name supported and unsupported claim | Collect individual responses |

### Theory cut order

- Cut the least-squares derivation and circular-mean formula first.
- Preserve slope units, residual definition, plots before coefficients, dependence, and
  association-versus-causation.
- If residual sign is unclear, use one observed/fitted number before moving to assumptions.

## Session 2: MOP relationship and final-analysis studio

**Minimum viable takeaway:** a credible small analysis is a transparent chain from question/source
through inspection and evidence to a bounded claim and honest limitation.

**Core checkpoint by minute 36:** pairs have a wave-height/period scatterplot, fitted slope with
units, residual view, and one sensitivity/dependence statement.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–8 | Map Mark's symbols to `waveTp`, `waveHs`, fitted values, residuals | Audit local file/metadata | Recovery only after focused check |
| 8–24 | Guide scatter, $r$, line, and slope units | Predict, fit, interpret | Require plot before coefficient |
| 24–36 | Residual/time view and sensitivity subset | Diagnose pattern; compare result | Ask what claim changed |
| 36–40 | Partner rubric check | One question and one required fix | Approve small scope |
| 40–44 | Break | Transition to own notebook | Form support zones |
| 44–62 | Assignment studio | Work individually; may discuss/pair-code | Approve question, unblock data/code |
| 62–71 | Structured peer check | Run/inspect; leave question + required fix | Match peers across datasets if possible |
| 71–77 | Revision and restart/run | Implement one fix; final Git commit | Help preserve evidence if failure remains |
| 77–80 | Submit and reflect | One choice + one limitation | Confirm receipt, not polish |

### Recovery and cut order

- If the longer MOP file is absent, use the seven-day file for learning the relationship workflow,
  but do not describe it as seasonal evidence.
- If MOP loading blocks a student after focused diagnosis, they may begin the Pier small prompt with
  their Monday file.
- Cut the direction plot and trimmed sensitivity first. Preserve scatterplot, slope units, residual
  inspection, limitation, assignment/peer-check time, and submission.
- Do not let a student spend the whole studio obtaining a larger or novel dataset. Reduce scope to
  one existing course file and one main figure.

## Studio support zones

- Instructor 1: Pier loading, paired differences, intervals.
- Instructor 2: MOP/xarray, wave relationships, direction metadata.
- Instructor 3: ERA5/prepared subset, notebook execution, Git/submission rover.
- Regroup after ten minutes if one queue is empty or overloaded.

## Friday debrief

- Did theory vocabulary appear correctly in student interpretations?
- How many students completed the small prompt and peer check?
- Which route generated the most setup time?
- Which claims most often exceeded the evidence?
- What must change before the next course offering?
