# Wednesday exit tickets and interpretation guide

Use these as completion checks, not high-stakes grading. Accept plain language when the distinction
is correct. Follow up on patterns across the class rather than polishing every response.

## Session 1: errors, functions, and checks

### Prompt

Name one mistake today's check would catch. Name one scientifically important mistake it would
**not** catch.

### Strong-response ingredients

- **Caught:** a unit error (Celsius/Fahrenheit/Kelvin), a fill value such as `-99.99` read as a
  temperature, an entirely missing series, or the wrong column selected.
- **Not caught:** sensor calibration or drift, whether the record is complete, whether flagged
  observations were handled appropriately, whether daily sampling is representative, whether
  observations are independent, and whether the interpretation follows from the figure.
- The strongest answers say *why* the second category is out of reach: the check tests one stated
  assumption and is silent about every other one.

### Follow-up cue

If a student writes only "it makes sure the numbers are right," ask: "Give me a specific number the
check would reject, and a specific way the figure could still be wrong."

### Watch for during the session

- **"I ran the `def` cell and nothing happened."** This is the correct behavior and the single most
  common confusion. Defining is not calling.
- **A hard-coded column left inside the function body.** The tell is two identical figures with
  different legend entries.
- **A missing `return`.** `ax` becomes `None` and a later `ax.set_ylabel(...)` raises
  `AttributeError: 'NoneType' object has no attribute 'set_ylabel'`. Let them read it; it is a
  better lesson than the fix.
- **Reading a traceback top-down.** Redirect to the last line, every time, until it is automatic.

### The difference-panel decision

The surface-minus-bottom series legitimately fails the −2 to 40 °C check. Both answers can earn full
credit; the reasoning is what matters.

- **Widening the shared range to −10 to 10** loses the ability to catch a Kelvin mix-up. Ask what
  value that range would now accept that it should not.
- **A separate range passed at the call site** is the intended answer: a temperature and a
  temperature difference are different physical quantities and should not share a validity range.

## Session 2: version control

### Prompt

In one sentence each: what does `git add` do, what does `git commit` do, and what would `git push`
do? Name one reason to inspect `git diff --cached` before committing.

### Strong-response ingredients

- `git add` selects changes for the next snapshot and changes nothing on disk;
- `git commit` records that snapshot in **local** history with a message and an author;
- `git push` would copy local commits to a remote such as GitHub;
- inspecting the staged diff confirms the commit contains what you intend and nothing else — no
  debugging print, no data file, no unrelated edit.

### Common misconceptions to address Thursday

- "Commit uploads the file." A commit is local until pushed.
- "Push merges it." Pushing shares a branch; review and merge are separate.
- "Clean status means correct." It means the working tree matches the last commit.
- "Git saves the data source." Provider data and provenance still follow the course data contract;
  the repository stores the code and the record needed to *reacquire* the data.
- "A readable `.py` diff means the notebook runs." Execution QA is still required.
- "`.gitignore` deletes the file." It tells Git not to track it; the file stays on disk.

### Watch for during the session

- **The editor trap.** Someone runs `git commit` without `-m` and lands in Vim. Announce the escape
  (`Esc`, `:q!`, Enter) *before* it happens.
- **`git add .`** — intercept it every time. It is the habit that later commits a 40 MB archive.
- **Commands run outside the practice folder.** Re-establish `pwd` before anything else; never run
  `git init` to clear a "not a git repository" message.

## Optional confidence pulse

Students mark one item privately: green / yellow / red for (1) reading a traceback, (2) writing and
calling a function, (3) adding a check that fails usefully, (4) making a focused commit, and
(5) explaining `git diff --cached`. Use this to form Thursday pairs and target office-hour support.
