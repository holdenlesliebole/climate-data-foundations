# Monday instructor run-of-show

Planning assumption: approximately 20 students, ten pairs, three instructors, two 80-minute
sessions. The afternoon is self-contained and does not depend on the morning curriculum.

## Before Monday

- Ask students to complete `00_setup_check.ipynb`; sort reports into environment, path, and access
  issues rather than answering them ad hoc.
- Hold a setup clinic and keep a list of students who need the Codespaces/browser route.
- Confirm GitHub Copilot entitlement and sign-in without making AI access a prerequisite for Monday.
- Open every notebook from a clean checkout and the documented course environment.
- Verify the current Pier archive component, filename pattern, header discovery, citation, license,
  and download behavior on the classroom network.
- Decide whether a Pier recovery ZIP can legally be redistributed. If not, hold only an authorized
  temporary in-room contingency and do not commit it.
- Put the guided notebooks, reference-notebook release time, cheatsheet, and help channel in one
  visible location.

## Shared room roles

- **Lead:** teaches and controls time; does not become the primary setup troubleshooter.
- **Rover:** starts with pairs 1–5, diagnoses setup/path failures, and uses the rejoin checkpoint.
- **Observer/extension coach:** starts with pairs 6–10, records misconceptions, supports continuation,
  and signals when one-third or one-half of the room is stuck.

Rotate driver/navigator after the first pair task and after the break. Experienced students may
choose peer review but are not assigned as permanent tutors.

---

## Session 1: Python from zero—values, arrays, and a first plot

**Minimum viable takeaway:** A student can run and modify a notebook cell, explain a named value and
a one-dimensional array, and make a plot with a meaningful title, axes, units, and legend.

**Core checkpoint by minute 70:** each pair has modified a worked line plot and added a second
temperature series to the scaffold without losing labels or units.

**Final product:** a labeled two-series temperature plot plus a one-sentence finding. Indexing,
missingness, loops, functions, and assertions are explicitly optional **Go further** work.

| Time | Lead | Students | Rover / observer |
|---|---|---|---|
| 0–10 | Welcome; define cell, code, output, error, and restart/run-all | Predict expression results individually, run, and compare | Identify kernel/setup failures; use a prepared rejoin notebook after three focused minutes |
| 10–23 | Variables, strings, numbers, and names that carry units | Change one value, rerun, and explain what changed | Listen for students treating cell order or output as permanent state |
| 23–36 | Contrast a list and NumPy array; introduce values, `shape`, and `NaN` recognition | Predict list/array multiplication and inspect the example array | Keep indexing and Boolean selection closed until the core plot is complete |
| 36–40 | Debrief one misconception | Explain to partner | Observer gives room-level signal |
| 40–44 | Screen/cognitive break | Switch driver/navigator | Reset and resolve one remaining setup cluster |
| 44–56 | Build the first line plot; point from every figure element back to one code line | Predict the missing-value gap, run, and identify title/axes/units/line/markers/legend | Ask students what question the line format answers |
| 56–70 | Demonstrate one bounded design change; launch two-series scaffold | Add bottom series, repair title/legend, and state one visible difference | Use copy/change/run/explain as the success criterion, not memorized syntax |
| 70–77 | Pair plot audit; open **Go further** only after core checkpoint | Audit another pair's labels and choose an extension if ready | Offer indexing, missingness, loops, or functions as choices rather than a race |
| 77–80 | Collect exit ticket; preview real-data acquisition | Individual response | Record how many pairs reached core without recovery |

### Tiered hints

1. Concept: “Which part is the data, and which part tells Matplotlib how to display it?”
2. Method: point to the existing `ax.plot(x, y, label=...)` pattern.
3. Skeleton: copy the surface line, change only the y values and label, then rerun.
4. Recovery: provide the completed first plot; the student still adds or modifies one series, audits
   labels, and writes the finding.

### Anticipated stuck points

| Symptom | First response | Do not do |
|---|---|---|
| `NameError` after jumping to a cell | Ask which earlier cell defines the name; restart/run in order | Reinstall Python |
| List multiplication surprises | Ask whether the object is a list or NumPy array | Declare lists “wrong” |
| Plot cell runs but no second line appears | Compare the two `ax.plot` calls and their y arrays | Rewrite the entire cell for the student |
| Axis says only `Temperature` | Ask which unit is encoded in the variable name | Treat labels as cosmetic |
| Student finishes at minute 45 | Open one selected **Go further** section | Turn student into assigned tech support |

### Cut order if behind

1. Keep all **Go further** sections asynchronous.
2. Shorten types discussion to number/text recognition.
3. Supply the complete single-series plot and ask students to add only the second line.
4. Preserve variables, array recognition, figure anatomy, units, and the two-series checkpoint.

---

## Session 2: from source to figure

**Minimum viable takeaway:** Loading starts at the authoritative source; preserve raw bytes and
metadata, then make the parsing decision explicit.

**Core checkpoint by minute 39:** each pair has a ZIP or recovery copy, has listed its contents, and
has identified the temperature CSV's real header plus two metadata facts.

**Final product:** a minimum provenance entry, inspected DataFrame, labeled surface/bottom time
series, and either a histogram or scatterplot with a finding and limitation.

| Time | Lead | Students | Rover / observer |
|---|---|---|---|
| 0–7 | Draw source → acquisition → raw → load → validate → plot | Name which step `read_csv` belongs to | Check that downloads will go to the project, not disappear in Downloads |
| 7–18 | Demonstrate how to distinguish collection page/component/file | Pairs find newest component, DOI, date, format, license | Verify each pair can state why it chose that component |
| 18–29 | Show raw-folder contract and ZIP listing | Download/move ZIP, list contents, extract once | Three-minute diagnostic rule; then authorized recovery/rejoin path |
| 29–39 | Model first-55-lines inspection | Find true header, flags, units, time-zone note | Checkpoint all pairs; ask what a tidy DataFrame would lose |
| 39–43 | Break | Switch driver/navigator | Confirm every pair has the same rejoin point |
| 43–57 | Work one parsing decision: discovered header + first nine columns | Predict naive load, then load and construct dates | Look for hard-coded Downloads paths and mutated raw files |
| 57–65 | Introduce the minimum inspection questions | Use `head`, shape, coverage, columns/units, and missing counts; inspect rather than filter flags | Treat detailed flag rules as later work unless required for the selected window |
| 65–72 | Work the time-series example and connect format to question | Plot a short window; audit title/axes/units/source/limitation | Check that students can say why time belongs on the x-axis |
| 72–77 | Open the visualization studio | Choose histogram or scatterplot, modify one design choice, and state what one mark represents | Open checksum/loader only after a second labeled format exists |
| 77–80 | Exit ticket and Tuesday preview | Individual response | Record which acquisition step consumed time |

### Network/recovery protocol

1. Pair reads the error and identifies the failed stage.
2. Rover checks network, browser download status, destination, filename, and permissions—one at a
   time—for no more than three focused minutes.
3. If the problem is external or environment-level, give the authorized recovery route.
4. Student copies the recovery file into `data/raw/pier/`, records
   `acquisition_method: instructor_recovery`, and continues with inspection/loading.
5. Recovery use receives the same course credit.

### Tiered hints

1. Concept: “Before pandas, can ordinary text reveal where the table begins?”
2. Method: `Path.glob`, `read_text`, `enumerate`, `line.startswith`.
3. Skeleton: `[i for i, line in enumerate(lines) if line.startswith("YEAR,")]`.
4. Recovery: completed acquisition/header-discovery checkpoint; student still explains metadata,
   loads locally, makes two plotting formats, and records provenance.

### Anticipated stuck points

| Symptom | First response | Scientific lesson |
|---|---|---|
| ZIP remains in Downloads | Resolve project-relative destination | acquisition and local organization are separate choices |
| `read_csv` makes one strange column | inspect first 55 lines | parsers need explicit file-structure decisions |
| Many trailing unnamed columns | inspect raw delimiters; use meaningful `usecols` | provider formats can carry empty fields |
| Bottom missing early in record | check stated coverage | structural missingness is not zero or random |
| Flags filtered immediately | read definitions and state rule first | QC decisions require metadata |
| Plot “looks right” but lacks units | audit labels and column names | appearance is not validation |

### Cut order if behind

1. Move SHA-256 to the reference/continuation lane.
2. Use one instructor-chosen six-month window.
3. Let pairs choose only one additional format rather than both histogram and scatterplot.
4. Complete the manifest after class but record provider/URL/date/filename before leaving.
5. Preserve source discovery, text inspection, explicit load, the time series, and one format-choice
   explanation.

## End-of-day instructor debrief (10 minutes)

- How many pairs used recovery, and at which acquisition stage?
- Which setup failures should be fixed before Tuesday rather than retaught?
- Did the room reach a labeled two-series plot and header discovery?
- Which code/wording change is required before releasing the completed references?
- Were both sessions inside 80 minutes? If not, use the stated cut order rather than speeding up.
