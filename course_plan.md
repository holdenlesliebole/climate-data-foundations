# Climate Data Foundations Bootcamp — course plan v0.4

## Purpose and working assumptions

This week is a bridge into graduate climate-science coursework, not a compressed computer-science
or statistics degree. A successful student finishes the week able to open an unfamiliar dataset,
ask sensible questions about it, make a defensible plot, perform a modest analysis, explain what
they did, and recover when something goes wrong.

This draft assumes:

- two 80-minute afternoon sessions each day;
- approximately 20 students, with final enrollment still uncertain;
- three instructors available across the week, with Mark leading Thursday and Friday;
- students bring their own laptops;
- students receive access to GitHub Copilot;
- VS Code, Python, and the course environment are installed before Monday where possible;
- students acquire the core Pier and MOP files themselves during class, while instructors keep
  clearly labeled recovery copies so a transient network problem does not consume the lesson;
- students submit one short, low-stakes analysis at the end of Friday;
- grading rewards attendance, engagement, a good-faith attempt, and a minimally reproducible result
  more than polish or statistical sophistication.

The afternoon curriculum is self-contained and does not assume any specific content taught elsewhere
during the week. Instructors can add an informal callback when useful, but the notebooks and notes
must make sense without it.

## Design decisions

1. **Teach a workflow, not a package tour.** The recurring workflow is: question → load → inspect →
   clean → visualize → summarize/model → check → communicate.
2. **Use one coherent data story.** Scripps Pier surface and bottom temperature is the welcoming
   first dataset; MOP wave height, peak period, and peak direction add metadata and quality-control
   questions; a small ERA5 subset adds labeled spatial dimensions.
3. **Keep a visible core path and extension lane.** Every session has a complete novice-accessible
   product. Faster students move to an independent continuation without waiting or becoming the
   default teaching assistants.
4. **Use modern data models.** NumPy establishes arrays. Pandas represents tables and time series.
   Xarray represents labeled, multidimensional data and opens NetCDF. The first day should not teach
   low-level `netCDF4` indexing as a separate framework.
5. **Treat acquisition as part of research.** Students discover the authoritative source, make a
   bounded request or download, preserve the untouched result, and record provenance before loading
   it. A recovery copy is available after a troubleshooting checkpoint, but it is not the default
   starting point.
6. **Teach LLM use as a verification loop.** Generated code is an untrusted draft. Students must be
   able to state the request, inspect the change, run it, test it, and explain the result.
7. **Pair statistical theory with immediate use.** Mark leads the first session on both Thursday and
   Friday, including the mathematical ideas and assumptions. The second session turns that theory
   into a guided analysis of the Pier and MOP data.
8. **Leave a durable reference set.** Each class notebook is accompanied by concise notes,
   common-error guidance, and links to primary documentation so students can reuse the material
   during the rest of the program. Completed examples may be built into the lesson or supplied as a
   separate reference when that genuinely improves navigation.

## End-of-week outcomes

Every student should be able to:

- navigate a project folder in VS Code and with a few safe terminal commands;
- read Python and modify short scripts or notebook cells using variables, conditionals, loops, and
  functions;
- distinguish a NumPy array, pandas `DataFrame`, and xarray `Dataset` and select the right one for a
  simple task;
- locate an authoritative data source, distinguish a landing page from a file URL, acquire a small
  file manually and programmatically, and record enough provenance to repeat the acquisition;
- open CSV and NetCDF data, inspect shape/dimensions, coordinates, variables, units, missing values,
  and metadata;
- make and label line, histogram, scatter, and two-dimensional field plots;
- distinguish an unusual observation from an erroneous one and use quality flags without silently
  discarding data;
- calculate and interpret descriptive summaries, anomalies, correlations, a simple linear trend,
  and an uncertainty interval;
- explain why independence, seasonality, autocorrelation, and confounding matter for climate data;
- turn repeated code into a function and add at least one assertion or test;
- use `git status`, `git diff`, `git add`, `git commit`, and `git log` in a small repository;
- use an LLM for a bounded coding task and verify its output rather than accepting it on appearance;
- produce a notebook that runs top-to-bottom and states its data source, assumptions, and limitations.

## Week at a glance

| Day | Afternoon session 1 | Afternoon session 2 | Daily product |
|---|---|---|---|
| Monday | Python as a scientific calculator: variables, arrays, control flow, functions | From source to figure: acquire, unpack, inspect, and plot the Pier archive | A provenance record and labeled Pier temperature figure |
| Tuesday | Working environment: terminal, VS Code, GitHub Copilot, and LLM-assisted coding | Reproducible remote data: construct, save, and inspect a CDIP MOP request | A MOP manifest entry and four-box data field note |
| Wednesday | Errors, functions, and one honest check: read a traceback, write a plotting function, add a plausible-range assertion | Version control with Git: four focused commits in a disposable project | Three panels from one function, plus a readable commit history |
| Thursday | **Mark:** statistics foundations I—distributions, sampling, estimators, variability, uncertainty | Apply the theory—inspect Pier data, summarize variability, and estimate uncertainty | A one-page data health report and uncertainty statement |
| Friday | **Mark:** statistics foundations II—covariance, correlation, regression, assumptions, time dependence | Apply the theory—Pier/MOP analysis and final-assignment studio | A short, reproducible climate-data analysis |

## Shared 80-minute session rhythm

| Time | Activity |
|---|---|
| 0–5 min | Retrieval question, backward link, and minimum viable takeaway |
| 5–17 min | Short explanation plus a live worked example |
| 17–32 min | Guided pair task with a checkpoint |
| 32–40 min | Compare results and diagnose one common misconception |
| 40–44 min | Screen and cognitive break |
| 44–56 min | Second short explanation or faded example |
| 56–71 min | Core challenge; extension lane opens as students finish |
| 71–77 min | Peer explanation, gallery walk, or whole-class debrief |
| 77–80 min | Exit ticket and preview |

Aim for students to spend at least half of Monday through Wednesday and the Thursday/Friday
application sessions typing, predicting, discussing, checking, or explaining. Mark's theory sessions
can contain more sustained exposition, but should still include prediction questions, a worked
example, a short break, and a final bridge to the afternoon notebook.

## Detailed session plans

### Monday 1 — Python as a scientific calculator

**Minimum viable takeaway:** Scientific Python mostly means putting values in clearly named objects,
transforming collections of values, and checking that the result has the shape and units expected.

**Learning objectives**

- Run and rerun notebook cells deliberately.
- Use variables, numbers, strings, booleans, lists, and NumPy arrays.
- Index and slice an array and interpret `shape`, `dtype`, and `NaN`.
- Read a short `for` loop and `if` statement.
- Write and call a small function with a docstring.

**Flow**

- 0–8: orientation, kernel/cell state, and a prediction about `2 + 3 * 4` versus `(2 + 3) * 4`.
- 8–20: variables, units, types, and a temperature-conversion worked example.
- 20–36: pair task—convert a small list of ocean temperatures, locate a missing value, and explain
  one surprising result.
- 36–40: break.
- 40–54: arrays, slicing, Boolean selection, and one explicit loop.
- 54–67: replace the loop with an array operation; compare readability rather than speed alone.
- 67–77: write `celsius_to_fahrenheit(values)` and check one known answer.
- 77–80: exit ticket—predict the output and explain whether the input is mutated.

**Core product:** one function, one Boolean selection, and one written check.

**Continuation:** calculate a daily mean from sub-daily data first with a loop and then with
`reshape`/`mean`; compare results when a `NaN` is present.

### Monday 2 — From source to figure

**Minimum viable takeaway:** Loading begins before `read_csv`: find the authoritative source, save an
untouched raw file, read its documentation, and verify what each row and column represents.

**Learning objectives**

- Distinguish a dataset landing page, an archive component, a download URL, and a local file path.
- Download the current Pier ZIP, extract it into `data/raw/pier/`, and leave the contents unchanged.
- Inspect file suffix, size, the CSV preamble, true header row, missing-value marker, and flag notes.
- Open the surface/bottom temperature CSV with pandas and construct a real date column.
- Inspect with `head`, `info`, `describe`, ranges, flags, and missingness.
- Make a line plot with a useful title, labeled axes, units, and source.
- Label axes with quantity and units and write a one-sentence interpretation.

**Flow**

- 0–7: trace the chain from a published dataset page to a file on disk; distinguish source,
  acquisition, loading, and analysis.
- 7–18: pairs inspect the [Pier collection](https://library.ucsd.edu/dc/object/bb4003017c), identify
  the newest archive component, capture its date/DOI/citation, and predict what the ZIP contains.
- 18–29: students download and extract the ZIP into `data/raw/pier/`, then use `pathlib` to list the
  files, suffixes, and sizes. Instructors troubleshoot before offering a recovery copy.
- 29–39: open the first 50 lines of the temperature CSV as text, find the real header on line 47,
  and record the metadata and flag meanings that a naive `read_csv` call would lose.
- 39–43: break.
- 43–57: pairs make a prediction, then load with pandas using an explicit header/skip decision,
  retain the first nine meaningful columns, and construct a date from year/month/day.
- 57–69: answer the six inspection questions: source, shape, time coverage, variables/units,
  missingness, and quality flags; include at least one plausibility check.
- 69–77: make a short-period surface/bottom plot and trade notebooks to audit the title, axes, units,
  source, and whether missing/flagged data were handled visibly.
- 77–80: exit ticket: “What information would have been lost if you had only been handed a tidy
  DataFrame?”

**Core product:** an acquisition/provenance entry plus a labeled Pier time-series plot with a
two-sentence caption.

**Continuation:** discover the header row without hard-coding 46, calculate the ZIP or CSV SHA-256,
and write a `load_pier_temperature(path)` function that checks the expected columns before returning
a DataFrame.

### Tuesday 1 — Terminal, VS Code, and LLM-assisted coding

**Minimum viable takeaway:** An LLM can propose code; the scientist remains responsible for the
question, assumptions, execution, validation, and interpretation.

**Learning objectives**

- Explain working directory, absolute/relative path, environment, interpreter, and notebook kernel.
- Use `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `head`, and command history safely.
- Open a project folder in VS Code, select the course interpreter, and use its integrated terminal.
- Give an LLM a bounded task with context and acceptance checks.
- Review a proposed diff or cell and test it before adopting it.

**Flow**

- 0–17: terminal scavenger hunt inside a disposable practice folder. Discuss destructive commands,
  but do not make recursive deletion part of the required exercise.
- 17–30: open the same folder in VS Code; identify explorer, editor, terminal, interpreter/kernel,
  problems, and source-control panels.
- 30–38: pairs diagnose three common setup failures: wrong directory, wrong interpreter, missing file.
- 38–42: break.
- 42–54: demonstrate the LLM loop: context → small request → proposed check → run → inspect → revise.
- 54–67: pairs critique intentionally plausible but wrong climate code (wrong dimension, Celsius/Kelvin
  confusion, or silently skipped missing values).
- 67–77: use GitHub Copilot to add a plot title and input validation to a
  known function; students must explain every accepted line.
- 77–80: exit ticket—name one failure the test catches and one it does not.

**Core product:** a short prompt, the resulting change, a validation check, and a written explanation.

**Continuation:** ask two tools or models for the same bounded task, define comparison criteria before
seeing the answers, and document which response is safer and why.

**LLM guardrails to state explicitly**

- Do not paste credentials, unpublished data, personally identifiable information, reviewer material,
  or restricted code into an external service.
- Never run an unfamiliar command without reading it; pause especially for deletion, permissions,
  installation, network upload, and credential requests.
- Require small changes and visible checks. “It ran” is not the same as “it is scientifically right.”
- Cite and read the primary documentation for scientific and statistical claims.

### Tuesday 2 — Reproducible remote data: CDIP MOP safari

**Minimum viable takeaway:** A remote data request is part of the scientific method: choose a small
space/time/variable subset deliberately, save the exact request and untouched response, then analyze
the local file.

**Learning objectives**

- Compare a manual archive download with a parameterized remote request.
- Inspect metadata and quality flags before choosing a variable.
- Explain resolution, coverage, units, and one limitation of a dataset.
- Construct a small THREDDS NCSS request, save its NetCDF response, and reopen it locally.
- Recognize a URL download, an API request, an OPeNDAP endpoint, and a local raw-data cache.

**Flow**

- 0–10: compare Monday's manual archive path with a programmatic request; mark which choices belong
  in a script and which facts belong in the manifest.
- 10–23: read the MOP/NCSS page and variable metadata; pairs choose a seven-day window and request
  `waveHs`, `waveTp`, `waveDp`, `waveFlagPrimary`, and `waveFlagSecondary` from the selected site.
- 23–39: build the query parameters in Python, print and read the resulting URL, and choose an
  informative destination such as `data/raw/mop/D0513_2026-07-01_2026-07-07.nc`.
- 39–43: break.
- 43–53: run the request, inspect HTTP/file-size evidence, refuse silent overwrites, and add the URL,
  access time, selection, and local filename to the manifest. After a brief diagnostic checkpoint,
  students with genuine network failures copy the identical instructor recovery file and record that.
- 53–66: open the local NetCDF with xarray; inspect dimensions, coordinates, variable attributes,
  units, valid ranges, and primary/secondary flags before extracting values.
- 66–76: select by time label and make a plot or height-period scatter; add a source and one
  limitation noting that MOP output is model-derived rather than a direct buoy observation.
- 76–80: field-note share and exit ticket: “What would another researcher need to repeat this
  request next month?”

**Core product:** a manifest entry, locally saved NetCDF file, xarray inspection, and one MOP field
note.

**Continuation:** wrap the request in a reusable command-line script, calculate and verify its
checksum, compare two windows, or inspect a small prepared ERA5 field and explain why credentialed,
queued data systems require a different acquisition plan. ERA5 credential setup remains post-class.

### Wednesday 1 — Errors, functions, and one honest check

**Minimum viable takeaway:** Read the last line of an error message first, write and call one
function, and add one check that would catch a real mistake.

This session **introduces** functions rather than assuming students have already learned them. The
vehicle is repeated plotting code, which is also this day's contribution to the visualization spine.

**Learning objectives**

- Read a traceback from its last line upward and name the failure before changing anything.
- Recognize `NameError`, `FileNotFoundError`, and `KeyError` and state the first thing to print.
- Write a function with parameters, a docstring, a body, and a return value, and call it repeatedly.
- Replace repeated plotting code with one function call per panel.
- Add one assertion that catches a wrong unit before it reaches a figure.

**Flow**

- 0–6: worked example—two near-identical copied plotting cells; find the intended differences and
  the copy damage.
- 6–18: traceback lab. Three deliberate failures, each read last-line-first and answered by one
  diagnostic print.
- 18–26: worked example—the anatomy of a function; predict, call, and modify.
- 26–39: core task—move the plotting lines into `plot_pier_temperature` and call it twice.
- 39–43: break.
- 43–52: add a plausible-range assertion, then watch it reject a Fahrenheit series that would
  otherwise produce a clean, labeled, wrong figure.
- 52–64: **core checkpoint**—three panels from one function, including the decision about what
  plausible range a *difference* deserves.
- 64–72: four-question figure check, interpretation, and use of the in-notebook hint if needed.
- 72–77: **Go further** opens; others polish labels and interpretations.
- 77–80: exit ticket—one mistake the check catches and one it cannot.

**Core product:** one function that removes real repetition, one assertion with a useful message,
three labeled panels, and one bounded interpretation.

**Go further:** `ax=None` and a shared-axis multi-panel figure; reading `src/climate_course/pier.py`;
`assert` versus `ValueError`; a summary function with a known-value test; running the `pytest` suite
and stating what passing does not establish; type hints and `pytest.mark.parametrize`.

**Recovery:** `example_pier_frame()` supplies a provider-shaped teaching table so a missing Pier
download cannot cost a student the session. The instructor recovery file remains the preferred route;
the notebook prints which source produced the figures.

### Wednesday 2 — Version control with Git

**Minimum viable takeaway:** `status → diff → add → commit → log`. Look at exactly what you are about
to record before recording it.

**Learning objectives**

- Read a short project history and say what happened and which commits recorded decisions.
- Distinguish working tree, staging area, local history, and remote.
- Use `status`, `diff`, `add`, `commit`, and `log` as a deliberate loop, unaided.
- Write a commit message that says why the change exists.
- Keep generated files, raw data, and secrets out of a repository with `.gitignore`.

**Flow**

- 0–8: worked example—read a five-commit history nobody wrote; identify the scientific decisions.
- 8–15: generate the disposable project, confirm `pwd`, and run `git init -b main`.
- 15–26: commit 1 (purpose), with `git diff --cached` inspected before committing.
- 26–38: run the analysis; an untracked `figures/` folder appears; commit the code and the
  `.gitignore` as two separate coherent changes.
- 38–42: break.
- 42–50: rank five candidate commit messages for the same change and say what separates them.
- 50–60: **core checkpoint**—a fourth commit with no commands supplied.
- 60–70: collaboration map: issue → branch → draft pull request → review → QA → merge.
- 70–77: safe-undo commands and five scenario cards answered with stop / inspect / ask.
- 77–80: exit ticket—distinguish `git add`, commit, and push, and name a pre-merge check.

**Core product:** four focused commits in a disposable local repository, a `.gitignore` that excludes
the generated figure, and a clean final `git status` the student can interpret.

**Go further:** `git restore --staged` and `commit --amend`; branches and pull requests; how to review
notebook JSON with notebook-aware tools; conflict, secret, large-data, and force-push scenarios
discussed rather than performed.

### Thursday 1 — Statistics foundations I: distributions, sampling, and uncertainty

**Lead:** Mark

**Minimum viable takeaway:** A statistic is an estimate calculated from a sample; its uncertainty
depends on both the variability in the data and assumptions about how the sample was obtained.

This session is intentionally more mathematical and lecture-centered than Monday through Wednesday.
The goal is not to derive a catalog of tests, but to give students a durable mental model for the
quantities the Thursday notebook will calculate.

**Learning objectives**

- Distinguish population, sample, random variable, distribution, statistic, and estimator.
- Interpret mean, median, variance, standard deviation, quantiles, and interquartile range.
- Explain the difference between the spread of observations and the uncertainty of an estimate.
- Describe a sampling distribution and the logic of a standard error or confidence interval.
- State why independence is an assumption rather than an automatic property of a dataset.

**Mathematical spine**

- mean and sample variance, including the units of each;
- median and quantiles as order-based summaries;
- repeated samples and the sampling distribution of an estimator;
- the standard error of a mean under an iid model;
- confidence-interval logic and a conceptual introduction to bootstrap resampling;
- why many daily observations do not necessarily equal many independent observations.

**Flow**

- 0–8: prediction—two datasets have the same mean but different shapes; what information is missing?
- 8–25: lecture I—distributions, center, spread, quantiles, and units.
- 25–36: worked Pier-temperature example calculating and interpreting summaries by hand/diagram.
- 36–40: individual concept check followed by neighbor discussion.
- 40–44: break.
- 44–60: lecture II—samples, estimators, sampling distributions, standard error, and interval logic.
- 60–72: repeated-sampling worked example and the bootstrap idea; identify the resampling unit.
- 72–77: dependence thought experiment using a smooth daily temperature record.
- 77–80: notebook bridge—map notation to the specific pandas/NumPy operations used next.

**Reference product:** Mark's annotated notes should include a symbol glossary, the small set of
formulas used, diagrams of observation versus sampling distributions, two worked examples, and a
“what this formula assumes” box beside each result.

**Continuation:** derive the usual standard-error formula or use a simulation to test its
approximately $1/\sqrt{n}$ behavior under independent sampling.

### Thursday 2 — Apply distributions and uncertainty to Pier data

**Minimum viable takeaway:** The theory becomes a sequence of visible choices in code: what counts as
an observation, how values are grouped, which summary is used, and what unit is resampled.

**Learning objectives**

- Build a compact data health report before calculating statistics.
- Compare surface and bottom temperature distributions and their difference.
- Distinguish missing, invalid, extreme, and merely unusual observations.
- Calculate descriptive summaries, climatologies/anomalies, and an uncertainty interval.
- Write an interpretation that names the estimate, interval, sampling unit, and limitation.

**Flow**

- 0–8: translate Mark's notation into named code objects and predict plausible temperature ranges.
- 8–22: load the Pier record and inspect provenance, coverage, sampling, units, duplicates,
  missingness, and available quality information.
- 22–36: plot surface and bottom distributions and calculate
  `surface_temperature - bottom_temperature` for paired observations.
- 36–40: “Would you delete this point?” check using one real extreme and one injected error.
- 40–44: break.
- 44–60: calculate monthly/seasonal summaries and bootstrap a selected mean difference using annual
  or seasonal summaries as the resampling units.
- 60–71: compare iid daily resampling with the more defensible grouped analysis; discuss dependence.
- 71–77: complete a one-page data health report and three-sentence uncertainty statement.
- 77–80: exit ticket—identify the observational unit and the assumption most likely to be violated.

**Core product:** inspection table, two diagnostic plots, one interval plot, and a bounded
interpretation.

**Continuation:** compare mean versus median, alternative seasons/baselines, or an iid bootstrap with
a moving-block bootstrap; report whether the conclusion is sensitive to the choice.

### Friday 1 — Statistics foundations II: relationships, regression, and time dependence

**Lead:** Mark

**Minimum viable takeaway:** Correlation and regression summarize relationships under assumptions;
the slope has physical units, residuals reveal missing structure, and association alone is not cause.

**Learning objectives**

- Explain covariance and correlation and what standardization changes.
- Interpret a least-squares line, slope, intercept, and residual in physical terms.
- Name the assumptions needed for a simple regression uncertainty statement.
- Recognize nonlinearity, unequal variance, influential years, confounding, shared trend, and
  autocorrelation.
- Explain what comparing annual levels with year-to-year changes can and cannot diagnose.

**Mathematical spine**

- covariance and the correlation coefficient;
- least squares as minimizing the sum of squared residuals;
- slope units and the distinction between prediction and explanation;
- residuals as observed minus fitted values;
- independence and autocorrelation in a time series;
- shared trend and the changed scientific question created by first differences;
- why a local contemporaneous Pier–CO₂ regression is not a causal attribution model.

**Flow**

- 0–8: compare scatterplots with similar correlations and predict what the coefficient misses.
- 8–24: lecture I—covariance, standardization, correlation, and their geometry.
- 24–36: worked least-squares example with slope units and residual calculation.
- 36–40: concept check—what changes under a unit conversion, and what does not?
- 40–44: break.
- 44–58: lecture II—residual patterns, assumptions, uncertainty, and model checking.
- 58–68: shared trend, first differences, autocorrelation, and why differencing is not a magic fix.
- 68–75: confounding, the Keeling Curve continuation, and why correlation does not establish cause.
- 75–80: notebook bridge and exit ticket—one claim the model supports and one it cannot support.

**Reference product:** annotated notes with one covariance/correlation example, one least-squares
example, a residual-pattern gallery, an assumptions checklist, and a shared-trend/first-difference
box.

**Continuation:** derive the least-squares slope or explore how a single influential point changes
the fitted line, residuals, and correlation.

### Friday 2 — Apply relationships and complete the final analysis

**Minimum viable takeaway:** A credible small analysis is a transparent chain from question and
provenance to inspection, evidence, a checked summary, and an honest limitation.

**Learning objectives**

- Make a scatterplot or grouped comparison before calculating a relationship statistic.
- Fit and interpret a simple relationship in physical units when appropriate.
- Use residuals, grouping, or a sensitivity check to qualify the result.
- Complete and submit a short notebook that runs from a fresh kernel.

**Flow**

- 0–8: instructor maps Mark's equations to annual NASA global temperature anomaly and annual Pier
  surface SST; pairs audit preserved source files and metadata.
- 8–17: pairs construct quality-screened annual Pier means and verify a one-to-one year merge.
- 17–27: plot both series in time, then calculate/interpret the year-colored scatterplot, $r$, line,
  and slope units.
- 27–38: inspect residuals in time and compare annual levels with consecutive-year changes.
- 38–42: partner check using the final-assignment rubric.
- 42–46: break.
- 46–63: individual or pair assignment studio; instructors approve scope and circulate.
- 63–72: structured peer check—run/inspect the notebook and leave one question and one required fix.
- 72–78: implement a fix, restart-and-run, and make a final Git commit.
- 78–80: submit plus a brief individual reflection: “one choice I made and one limitation.”

**Core product:** the submitted final analysis described below.

**Continuation:** add the Scripps Mauna Loa CO₂ record, compare annual levels with year-to-year
changes, test the Pier completeness threshold, or investigate a physically motivated lag.

## Differentiation without labeling students

### The core path

- Starter notebooks use a repeating rhythm: **Predict → Run → Explain → Modify → Check**.
- Every activity has a visible checkpoint and a small expected output (shape, value range, or plot
  feature) so novices know whether they are still on the road.
- Hints are tiered: conceptual cue, method name, then code skeleton. Solutions are released after the
  activity rather than displayed beside it.
- New syntax is introduced only when it serves the current scientific question.
- Glossaries define both computing terms and statistical terms in ordinary language.

### The extension lane

- Put a clearly marked continuation after every core checkpoint, never in a separate “advanced
  lecture” that forces experienced students to wait.
- Extensions should deepen the same question—robustness, scale, alternate visualization, tests,
  vectorization, or collaboration—rather than introduce unrelated packages.
- Faster students can act as peer reviewers by choice, but should not be assigned as permanent tutors.
  They also deserve technically meaningful work.

### Pairing and participation

- Rotate driver and navigator every 10–15 minutes.
- Use individual prediction before pair discussion so the most experienced voice does not always go
  first.
- Change pairs periodically and avoid public “beginner/advanced” grouping.
- Allow students to use completed checkpoint notebooks if setup problems have consumed the learning
  time; troubleshooting should not erase the scientific objective.

## Durable student reference set

The materials should be useful six months later, when a student remembers the task but not the
syntax. An activity notebook full of blanks is not enough. Release the following after each class:

- **Guided notebook:** the version used in class, retaining prompts and students' own work.
- **Completed reference notebook:** a clean version that runs top-to-bottom, includes expected
  outputs, and labels the core path separately from extensions.
- **Concept notes:** a concise Markdown/HTML or PDF explanation of the ideas, terminology, formulas,
  assumptions, and one or two worked examples. Thursday and Friday theory notes are especially
  important and should stand on their own without the lecture.
- **Acquisition/loading guide:** the reusable [data-loading notes](notes/data_loading.md) separate
  manual archives, programmatic subsets, provenance, local loading, and validation, with Pier and MOP
  examples students can adapt in later courses.
- **Common-errors box:** recognizable symptoms, likely cause, and first diagnostic step—wrong path,
  wrong kernel, unexpected dimension, missing value, wrong units, invalid comparison, or bad Git
  state.
- **Recipe index:** short links such as “open a CSV,” “inspect an xarray Dataset,” “select dates,”
  “make a labeled plot,” “calculate an anomaly,” “fit a line,” and “start a Git repository.”
- **Primary documentation links:** pandas, xarray, Matplotlib, SciPy/statsmodels, Git, VS Code, and
  GitHub Copilot pages used by the course.

Keep the environment file, data manifest, and tested course release together. Export the concept
notes and reference notebooks to static HTML as well as distributing `.ipynb` files; students can
then read them even when their Python environment is temporarily broken.

## Assessment and feedback

### Before the course

Use a non-graded survey plus a 15-minute diagnostic. Ask about operating system, installation status,
Python/notebook/terminal/Git experience, prior statistics, accessibility needs, and one climate topic
of interest. The diagnostic should ask students to run a cell, interpret a tiny plot, and say what
they would inspect in an unfamiliar dataset. It should not be used to rank students.

### During the week

- one three-minute exit ticket per session;
- one daily artifact, listed in the week-at-a-glance table;
- introduce the final-analysis notebook after Tuesday's remote-data session so students can notice possible
  questions during the week;
- instructors record common stuck points and adjust the next day's opening minutes;
- a simple confidence check: green = can repeat alone, yellow = can repeat with notes, red = cannot
  yet locate the first step.

### Final assignment — “A small climate-data story”

The separate [student-facing assignment draft](final_assignment_draft.md) can be revised and released
with the starter notebook. Students choose one dataset plus one bounded question. The
assignment should take roughly 35–60 focused minutes after the relevant class exercises, with most of
that time available during Friday's second session. Collaboration and Copilot use are allowed, but
each student should submit their own notebook and write their own interpretation. If time or setup
problems make individual submission unreasonable, allow a pair notebook plus a short individual
reflection.

The assignment is not a search for a novel climate result. It demonstrates that the student can
complete the course workflow and explain a few choices.

**Required elements**

1. State one specific question and identify the dataset/source.
2. Load a raw file acquired during the class using a relative project path; include the source URL,
   access date, local filename, and acquisition method. A documented recovery copy is acceptable.
3. Display and interpret basic structure: columns/dimensions, time coverage, units, flags, and
   missingness.
4. Make one personal analytical choice: time window, month/season, location, comparison, variable,
   or derived quantity.
5. Create one clear, labeled figure that addresses the question.
6. Calculate one numerical summary appropriate to the question: center/spread, a group difference
   with an interval, correlation/regression, or another method taught in class.
7. Write four to eight sentences describing the result, one assumption, and one limitation.
8. Restart and run the notebook top-to-bottom, then make a final Git commit.

**Suggested directions**

- **Pier surface/bottom temperature:** choose a month or season and examine the distribution of
  `surface - bottom` temperature; compare surface and bottom variability; or compare two periods
  without claiming that time alone establishes a cause.
- **Pier/global climate:** compare quality-screened annual mean Pier surface SST with NASA global
  temperature anomaly; compare levels with year-to-year changes; or add the Scripps Mauna Loa CO₂
  record while explicitly avoiding a causal attribution claim.
- **MOP waves:** compare significant wave height (`waveHs`) or peak period (`waveTp`) between two
  seasons; compare a distribution or group summary; or plot the distribution of peak direction
  (`waveDp`). Treat direction as circular and do not take an ordinary mean across 0°/360°.
- **ERA5:** compare one field or regional mean between two seasons, or compare a selected point with
  a regional average.
- **Student variation:** an equally small instructor-approved question using a course-acquired or
  documented recovery dataset.

Provide “small,” “medium,” and “open” versions of the prompts. The small version should be fully
acceptable for full credit; the alternatives create autonomy, not a hidden difficulty ladder.

### Assignment rubric (10 points, deliberately generous)

| Criterion | Points |
|---|---:|
| Participated in class checkpoints and made a good-faith attempt | 2 |
| Completed a peer check and attempted a revision | 1 |
| Stated a question/source, recorded acquisition provenance, and inspected structure/units/missingness | 1 |
| Made one personal subset, comparison, or derived-variable choice | 1 |
| Produced a relevant, labeled figure | 2 |
| Calculated and identified one numerical summary/method | 1 |
| Wrote a bounded interpretation with an assumption or limitation | 1 |
| Submitted a notebook that substantially reruns plus a final commit | 1 |

Apply the rubric for encouragement rather than fine discrimination. A notebook with a correctable
coding or statistical mistake should still earn substantial credit when the student engaged,
documented the attempt, and explained where they became uncertain. Extensions do not earn more base
credit than a well-executed small prompt.

## Three-instructor operating model

Rotate the roles each session:

- **Lead:** teaches short segments, manages timing, and conducts the debrief.
- **Rover:** handles quiet questions, accessibility needs, and technical triage without taking over a
  student's keyboard.
- **Observer/extension coach:** watches for common misconceptions, supports the continuation lane,
  records where the room is stuck, and signals the lead when to pause or cut.

With approximately 20 students, plan for about ten pairs. During lab sessions, each instructor can
initially monitor three or four pairs, while the rover crosses zones for setup failures. Mark remains
the lead for both Thursday and Friday theory sessions; the other instructors can collect questions,
watch concept-check responses, and identify which point needs a second explanation.

Before each session, agree on the minimum viable takeaway, the one checkpoint everyone should reach,
which block will be cut first, and what counts as a setup issue versus a content issue.

## Technical and data plan

### Proposed repository shape

```text
Climate_science_bootcamp/
├── README.md
├── environment.yml
├── data/
│   ├── README.md
│   ├── manifest_template.yml
│   ├── raw/                 # immutable files acquired by each student
│   │   ├── pier/
│   │   └── mop/
│   ├── recovery/            # instructor fallback; same bytes, clearly labeled
│   └── processed/           # generated; usually ignored by Git
├── notebooks/
│   ├── 00_setup_check.ipynb
│   ├── 01_python_numpy.ipynb
│   ├── 02_source_to_figure.ipynb
│   ├── 03_tools_llms.ipynb
│   ├── 04_remote_data.ipynb
│   ├── 05_reliable_code.ipynb
│   ├── 06_git_workflow.ipynb
│   ├── 07_data_health.ipynb
│   ├── 08_uncertainty.ipynb
│   ├── 09_relationships.ipynb
│   └── 10_final_analysis.ipynb
├── notes/                   # concepts, formulas, assumptions, worked examples
├── reference/               # completed notebooks plus static HTML exports
├── cheatsheets/             # recipe index, inspection checklist, Git/terminal reference
├── scripts/                 # optional fetch and preprocessing scripts
├── src/                     # reusable course functions by Wednesday
├── tests/
├── figures/                 # generated; ignored by Git
└── solutions/               # instructor/release copies
```

### Environment

Keep one supported environment. A likely starting set is Python, Jupyter/IPython, NumPy, pandas,
xarray, Matplotlib, SciPy, statsmodels, `netcdf4` or `h5netcdf`, and pytest. Add Cartopy only if the
ERA5 core activity truly needs a coastline; its installation and data downloads are not worth making
the first plotting success depend on it. Pin and test the environment on macOS, Windows, and Linux.

### Student acquisition and recovery bundle

The student path should begin at the provider and end with an untouched file in `data/raw/`.
Instructors should independently preflight the same request and keep a recovery bundle comfortably
below roughly 50 MB if licensing permits. Release a recovery file only after students can explain
the step that failed; they still complete the local loading, provenance, and validation work.

Use these acquisition routes:

- **Pier surface/bottom record—manual archive route:** students start at the [UC San Diego Library
  collection](https://library.ucsd.edu/dc/object/bb4003017c), select the newest component, download
  its ZIP, and extract it locally. As of 2026-06-30 the archive contains temperature and salinity in
  both CSV and XLS formats; the temperature CSV is `LaJolla_TEMP_1916-202603.csv`, with a descriptive
  preamble followed by the actual header on line 47. Students retain the preamble, units, missing
  values, and flags rather than receiving a tidy derivative. The program reports surface data from
  1916 and bottom data from 1926; current methods describe sampling at approximately 0.5 m and 5 m.
- **Selected MOP site—programmatic subset route:** students construct a small NCSS request for the
  selected site containing time, significant wave height (`waveHs`), peak period (`waveTp`), peak
  direction (`waveDp`), and primary/secondary flags. A tested seven-day request for near-Pier site
  `D0513_nowcast.nc` is about 44 KB, small enough for the exercise. Preserve the full request URL and
  attributes defining units, direction convention, valid ranges, location, flags, and the fact that
  MOP values are model outputs rather than direct observations. Recheck the rolling nowcast coverage
  and choose a recent teaching interval immediately before the course.
- **NASA GISTEMP—programmatic CSV route:** students locate the global Land–Ocean Temperature Index
  table from the official download page, preserve the CSV in `data/raw/climate/`, inspect its title
  and header, record the 1951–1980 anomaly baseline, and load the annual `J-D` column. Recheck the
  URL and dated response immediately before class because the provider updates the table.
- **Scripps Mauna Loa CO₂—continuation CSV route:** students preserve the official monthly in-situ
  response, inspect the scientific preamble and three-row header, interpret `-99.99` as missing, and
  distinguish measured, adjusted, fitted, and filled products. Retain the stated citation and CC BY
  attribution and record that values are subject to revision.
- **ERA5:** a small Southern California or eastern Pacific monthly subset with time, latitude,
  longitude, 2 m temperature, and optionally `u`/`v` wind components;
- **teaching variants:** clearly marked copies with one injected unit error, duplicate timestamp,
  impossible value, and missing block for inspection exercises.

Each student manifest entry should record the landing page and/or exact request URL, dataset
title/provider, archive or component date, access timestamp, license/terms, requested variables and
time window, local filename, acquisition method, and SHA-256 when introduced. Never edit a raw file
in place or mix deliberately corrupted teaching data with the untouched raw sample.

Confirm and include the Shore Stations requested credit statement in the data README, notebook,
notes, and final-assignment starter. Confirm redistribution terms before placing a Pier recovery copy
in the course repository; if redistribution is not authorized, let students use the Library download
and keep only instructor instructions plus a temporary in-room contingency.

Peak direction is an angular variable: 1° and 359° are close, not far apart. Verify and teach the
CDIP direction convention before students interpret `waveDp`; use time series, directional bins, or
a polar histogram on the core path rather than an ordinary arithmetic mean of degrees.

Do not perform a live ERA5 Climate Data Store request in the core lesson: accounts, credentials,
queues, GRIB engines, and file sizes distract from the learning target. Demonstrate a tiny request,
provide the script, and analyze a prepared NetCDF subset.

## Resource adaptation map

| Resource | Best use here | Adaptation needed |
|---|---|---|
| [SIO Python for Earth Science](https://github.com/eldavenport/SIO-PythonEarthScience) | Main source for beginner Python/plotting activities, Unix/Git framing, xarray, and Earth-science examples | Split its broad modules across the week; open NetCDF with xarray on the core path; trim advanced Dask/EOF/xgcm material; preserve its MIT notice for copied/adapted material |
| [CSP Data Workshop](https://connorjmack.github.io/csp-data-workshop/) | Concise OS-specific setup, VS Code, first repository, and terminal reference | Move most installation before Monday; expand its very short terminal pacing; link to living setup pages instead of relying on screenshots; replace tool-specific AI content with the verification loop |
| [Scientific Python Lectures](https://lectures.scientific-python.org/) | Reference and extension material for NumPy, Matplotlib, debugging, and statistics | Its chapters are roughly one-to-two-hour tutorials and the statistics chapter is broader than this bootcamp; link selected sections instead of assigning it linearly |
| [Python for Climate Scientists](https://github.com/duncanwp/python_for_climate_scientists) | Exercise ideas for NumPy, Matplotlib, testing, and atmospheric data | The repository is largely from 2017; use concepts, not its older Python/Iris/CIS stack; follow GPL requirements if adapting covered code directly |
| [UCSD Library Scripps Pier collection](https://library.ucsd.edu/dc/object/bb4003017c), [Shore Stations data access](https://shorestations.ucsd.edu/publications/data/), and [methods](https://shorestations.ucsd.edu/methods/) | Primary Pier surface/bottom data, access/credit instructions, and sampling context | Complete the access form; preserve the requested credit, archive citation/DOI, observation depth, method changes, units, missing values, and redistribution terms in the manifest and notes |
| [CDIP MOP documentation](https://cdip.ucsd.edu/documents/index/product_docs/mops/mop_intro.html) | Scientific context, metadata, and public MOP data for the wave-data station | Have students construct a small request and define model-derived versus observed quantities carefully; preflight the same request for recovery |
| [CDIP THREDDS NCSS page for D0513](https://thredds.cdip.ucsd.edu/thredds/ncss/point/cdip/model/MOP_alongshore/D0513_nowcast.nc/dataset.html) | Request interface and attributes for the near-Pier instructional site, including `waveHs`, `waveTp`, `waveDp`, and flags | Recheck rolling coverage before class; preserve each student's exact query and analyze the saved local NetCDF rather than repeatedly reading the live endpoint |
| [Xarray tutorial datasets](https://docs.xarray.dev/en/stable/generated/xarray.tutorial.load_dataset.html) | Backup dataset and xarray extension | Cache locally; tutorial downloads still require network on first use |
| [VS Code getting started](https://code.visualstudio.com/docs/getstarted/overview) and [GitHub Copilot getting started](https://docs.github.com/en/copilot/get-started) | Living pre-course setup links | Recheck immediately before teaching because the UI changes; verify student Copilot entitlement and sign-in during the setup check |

The course should include an attribution file from the beginning. Link or ideas alone do not require
pretending the material was created from scratch, and direct adaptation must follow each source's
license.

## Scope controls: deliberately defer these

- object-oriented programming;
- Dask/distributed computation as a required topic;
- EOF/PCA, machine learning, Bayesian modeling, ANOVA, and a catalog of hypothesis tests;
- full Git branching strategies, rebase, or command-line conflict surgery for everyone;
- environment-manager comparisons;
- live ERA5 credential setup and large downloads;
- publication-quality cartography;
- “prompt engineering” as a collection of magic phrases;
- optimizing code before it is correct and clear.

Mention these as destinations and provide follow-up links, but protect the core outcomes.

## Build order

### Priority 0 — unblock the course

- Confirm dates, room/internet/power, final enrollment, and laptop policy; design room logistics around
  roughly ten pairs for now.
- Send the background/setup survey at least two weeks in advance.
- Choose one environment and test it on all three operating systems.
- Verify the current Pier component and MOP time coverage, license-check recovery copies, dry-run both
  student acquisition paths, checksum the instructor results, and document the three core datasets.
- Schedule a setup clinic and provide a browser/hosted fallback if possible.
- Verify that every student can activate GitHub Copilot and agree on the institution's policy for AI
  tools, privacy, and unpublished data.
- Mark selects the exact theory depth, notation, and formulas for Thursday and Friday so the
  application notebooks use the same language.

### Priority 1 — build and dry-run the core

- Build `00_setup_check`, Monday's two notebooks, and their solution copies first.
- Then build the common data-inspection helper/checklist used Tuesday through Friday.
- Build the deliberately broken examples and their expected failure checks.
- Build a reference-notes skeleton and HTML export workflow at the same time as the notebooks rather
  than reconstructing documentation after the course.
- Dry-run the acquisition notebooks on the classroom network and dry-run every downstream notebook
  from the recovered local files with the network disabled.
- Have a novice proxy and an experienced proxy attempt the core and extension lanes.
- Time each activity; mark a cut point before class rather than improvising one under pressure.

### Priority 2 — finish the week

- Build Git collaboration and statistics notebooks around the same cached data and Mark's notation.
- Prepare the final-analysis starter notebook, generous rubric, and small/medium/open prompt cards.
- Create instructor notes with anticipated stuck points and tiered hints.
- Create a one-page command/data-inspection reference and post-course learning map.

## Decisions still to make

- Final class size and room layout; current planning estimate is approximately 20.
- Whether a managed JupyterHub/Codespace fallback is available.
- Whether the current UCSD Pier archive may be redistributed as a recovery copy; the student route
  itself uses the public Library download.
- Whether near-Pier MOP site `D0513` is the final choice and which recent seven-day nowcast interval
  to use; the instructional variable set is `waveHs`, `waveTp`, `waveDp`, and the two flag variables.
- Mark's preferred balance among analytic standard errors, bootstrap intervals, regression
  uncertainty, and time-series dependence within two theory sessions.
- Whether final submissions are individual by default or paired with an individual reflection.
- Whether ERA5 remains a core data-safari station or becomes an extension so the Pier/MOP sequence
  can receive more time.
