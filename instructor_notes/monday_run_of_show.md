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

## Session 1: Python as a scientific calculator

**Minimum viable takeaway:** Values live in named objects; arrays transform collections; every result
needs a shape/unit/known-value check.

**Core checkpoint by minute 36:** each pair has created/inspected an array, selected values with a
Boolean mask, and explained why missing is not zero.

**Final product:** `celsius_to_fahrenheit`, a Boolean selection, and at least one explicit check.

| Time | Lead | Students | Rover / observer |
|---|---|---|---|
| 0–8 | Welcome; show notebook state and prediction routine | Predict expression results individually, then compare | Identify kernel/setup failures; move them to rejoin copy if diagnosis exceeds 3 minutes |
| 8–20 | Variables, units, types; 0 °C known-value demonstration | Modify Celsius value and explain naming | Listen for `temperature` without units and notebook cells run out of order |
| 20–36 | Lists versus arrays; `shape`, indexing, Boolean mask, `NaN` | Driver/navigator pair tasks; report missing count and selection | Checkpoint ten pairs; record list-multiplication and `NaN == 0` misconceptions |
| 36–40 | Debrief one misconception | Explain to partner | Observer gives room-level signal |
| 40–44 | Screen/cognitive break | Switch driver/navigator | Reset and resolve one remaining setup cluster |
| 44–54 | Read explicit conversion loop aloud | Predict each iteration/output | Ask quieter partner to narrate one iteration |
| 54–67 | Show vectorized equivalent and function; narrate inputs/outputs/docstring | Modify/call function; test freezing/boiling values | Open continuation only after core check |
| 67–77 | Launch core challenge; then compare checks | Complete inspect/convert/select/check task; peer audit | Require shape + units + known value, not only correct output |
| 77–80 | Collect exit ticket; preview acquisition | Individual response | Photograph/export anonymous response distribution |

### Tiered hints

1. Concept: “Does this operation apply to the whole collection or to one position?”
2. Method: `array[condition]`, `np.isnan`, or `np.nanmean`.
3. Skeleton: `selected = values[values > threshold]`.
4. Recovery: use the completed checkpoint cell through Boolean selection; student still writes the
   explanation and completes the function/check.

### Anticipated stuck points

| Symptom | First response | Do not do |
|---|---|---|
| `NameError` after jumping to a cell | Ask which earlier cell defines the name; restart/run in order | Reinstall Python |
| List multiplication surprises | Ask whether the object is a list or NumPy array | Declare lists “wrong” |
| Mean is `NaN` | Ask how many values are missing and compare `mean`/`nanmean` | Automatically fill with zero |
| Boolean mask length mismatch | Compare mask and data shapes aloud | Take over keyboard |
| Student finishes at minute 45 | Open sub-daily continuation | Turn student into assigned tech support |

### Cut order if behind

1. Do not live-code the continuation.
2. Shorten types discussion to `float`/`str`/`bool` recognition.
3. Provide the explicit loop and ask students only to trace it.
4. Preserve Boolean selection, missingness, function, and check.

---

## Session 2: from source to figure

**Minimum viable takeaway:** Loading starts at the authoritative source; preserve raw bytes and
metadata, then make the parsing decision explicit.

**Core checkpoint by minute 39:** each pair has a ZIP or recovery copy, has listed its contents, and
has identified the temperature CSV's real header plus two metadata facts.

**Final product:** a manifest entry, inspected DataFrame, labeled surface/bottom plot, and two-sentence
caption.

| Time | Lead | Students | Rover / observer |
|---|---|---|---|
| 0–7 | Draw source → acquisition → raw → load → validate → plot | Name which step `read_csv` belongs to | Check that downloads will go to the project, not disappear in Downloads |
| 7–18 | Demonstrate how to distinguish collection page/component/file | Pairs find newest component, DOI, date, format, license | Verify each pair can state why it chose that component |
| 18–29 | Show raw-folder contract and ZIP listing | Download/move ZIP, list contents, extract once | Three-minute diagnostic rule; then authorized recovery/rejoin path |
| 29–39 | Model first-55-lines inspection | Find true header, flags, units, time-zone note | Checkpoint all pairs; ask what a tidy DataFrame would lose |
| 39–43 | Break | Switch driver/navigator | Confirm every pair has the same rejoin point |
| 43–57 | Work one parsing decision: discovered header + first nine columns | Predict naive load, then load and construct dates | Look for hard-coded Downloads paths and mutated raw files |
| 57–69 | Introduce six inspection questions | Shape/coverage/units/missingness/flags/plausibility check | Assign one question per partner, then swap explanations |
| 69–77 | Audit one plot/caption | Plot short window; peer audit title/axes/units/source/limitation | Extension: reusable loader and checksum only after core |
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
   loads locally, validates, plots, and records provenance.

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
2. Plot one instructor-chosen six-month window.
3. Complete the manifest after class but record provider/URL/date/filename before leaving.
4. Preserve source discovery, text inspection, explicit load, one validation check, and labeled plot.

## End-of-day instructor debrief (10 minutes)

- How many pairs used recovery, and at which acquisition stage?
- Which setup failures should be fixed before Tuesday rather than retaught?
- Did the room reach Boolean selection and header discovery?
- Which code/wording change is required before releasing the completed references?
- Were both sessions inside 80 minutes? If not, use the stated cut order rather than speeding up.
