# Wednesday instructor run-of-show

Assumption: approximately 20 students, ten pairs, three instructors. Wednesday uses a novice-first
pattern: every session is **worked example → core path → Go further**, and the core path is genuinely
finishable by someone who first opened a notebook this week.

**The two things that must happen on Wednesday, whatever else is cut:** every student reads a real
traceback without panic, and every student writes and calls one function.

## What changed from v0.4, and why

- Wednesday 1 **introduces functions from first principles** rather than assuming they were taught
  earlier. The vehicle is repeated plotting code, not the Pier loader.
- The Pier loader, `pytest`, and `src/` layout moved into **Go further**. They are still built and
  still taught — as the deeper version, not the entry point.
- Session 1 does not fail if the Pier download is missing: `example_pier_frame()` provides a
  provider-shaped teaching table. Prefer the instructor recovery file first; this is the last
  resort, and it is labeled in the notebook as invented values.
- Session 2 gains `.gitignore` (Friday's submission depends on it) and a fourth, unguided commit as
  the checkpoint.

## Preflight

- If the Pier acquisition path is part of an earlier lesson, confirm `data/raw/pier/` contains an untouched provider
  archive plus an extracted CSV. Then **also** run session 1 with that folder empty and confirm the
  notebook falls back to the teaching example and says so.
- From the course root, run `pytest -q`; verify all tests pass without provider data or network.
- Run `notebooks/05_reliable_code.ipynb` from a fresh kernel. Its three deliberate-failure cells
  print full tracebacks through `traceback.print_exc()`, so the notebook still runs top to bottom.
  If a cell stops execution, something is genuinely wrong.
- Run `scripts/setup_git_practice.py --name git_practice_preflight`, then walk the full command
  sequence: `git init -b main`, four commits, `.gitignore`, `git restore --staged`. Delete it after.
- Confirm `git --version` on the room's machines. On a machine that has never set
  `init.defaultBranch`, plain `git init` prints a five-line hint and creates `master`; the lesson
  uses `git init -b main` to avoid both. Watch for students who type it without `-b main`.
- Prepare a local-only identity card for students whose commits are blocked by missing `user.name`
  or `user.email`.
- Do not require GitHub authentication in the core lane. Use projected screenshots or an instructor
  repository for the shared-workflow demonstration.

## Session 1: errors, functions, and one honest check

**Minimum viable takeaway:** read the last line of an error first, write and call one function, add
one check that would catch a real mistake.

**Core checkpoint by minute 64:** every pair has a working `plot_pier_temperature_checked`, has
called it more than once, and has watched it reject the Fahrenheit series.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–6 | Show the two near-identical plot cells; "what differs, and which differences are accidents?" | Read before running; name the copy damage | Triage missing Pier files; announce fallback if needed |
| 6–18 | Traceback lab: last line first | Run three failing cells; name each failure **before** editing | Ask "what is the last line?" and nothing else at first |
| 18–26 | Anatomy of a function; `def` runs nothing | Predict both printed values; modify to round | Watch for "I ran it and nothing happened" |
| 26–39 | Core task A: fill in `plot_pier_temperature` | Move plotting lines into the body; call it twice | Catch hard-coded columns left in the body |
| 39–43 | Break | Switch driver/navigator | Resolve only blockers |
| 43–52 | One check that fails loudly; run the Fahrenheit demo | Predict the message; read the `AssertionError` | Tie back to Tuesday's unit-confusion critique |
| 52–64 | **Core checkpoint:** three panels from one function | Decide what to do about the difference panel's range | Push for "what does this number physically mean?" |
| 64–72 | Four-question figure check; two pairs show a panel | Write one interpretation and one limitation | Use the in-notebook solution-shaped hint if needed |
| 72–77 | Go further opens (`src/`, `pytest`) | Ready students continue; others polish labels | Extension coach takes the Go-further table |
| 77–80 | Exit ticket | Individual response | Collect conceptual gaps |

### Anticipated stuck points

- **"Nothing happened when I ran the `def` cell."** Correct — defining is not calling. Have them add
  the call line themselves rather than doing it for them.
- **Hard-coded column left inside the function.** The tell is two identical figures with different
  legends. Ask "which line still says `SURF_TEMP_C`?"
- **`return` omitted.** `ax` becomes `None`, and `difference_axes.set_ylabel(...)` fails with
  `AttributeError: 'NoneType' object has no attribute 'set_ylabel'`. This is a good failure — let
  them read it.
- **The difference-panel decision.** Some pairs will widen the shared range to −10 to 10. Do not
  correct it immediately; ask what a −10 to 10 range would fail to catch. The intended answer is a
  separate range for a separate physical quantity.

### Recovery and cut order

- If Pier data are unavailable after a three-minute focused diagnostic, use the exact instructor
  recovery file and record the route. Only if that also fails, let the notebook fall back to the
  teaching example and say aloud that the values are invented.
- If imports fail, verify project root, environment, and `src/` layout before copying code into the
  notebook.
- **Cut in this order:** the gallery walk (64–72), then the Fahrenheit failure demo (keep the
  assertion, drop the demonstration), then the third panel. Never cut the traceback lab or the
  function.

## Session 2: version control

**Minimum viable takeaway:** `status → diff → add → commit → log`; look at exactly what you are
about to record before recording it.

**Core checkpoint by minute 60:** each pair has four focused commits in a disposable repository, a
`.gitignore` that excludes the generated figure, and can explain `git diff --cached`.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–8 | Worked example: read a five-commit history nobody wrote | Answer the four questions in pairs | Check `git --version` while they read |
| 8–15 | Generate the practice folder; four-places diagram | `cd`, `pwd`, say the folder aloud, `git init -b main` | Enforce the disposable-folder boundary |
| 15–26 | Commit 1: add → status → `diff --cached` → commit → log | Commit README; switch roles | Identity card if needed; watch for the editor trap |
| 26–38 | Run `analysis.py`; `figures/` appears; write `.gitignore` | Commits 2 and 3 as separate changes | Ask why generated files stay out |
| 38–42 | Break | Switch roles | Reset explanations, never repository history |
| 42–50 | Commit-message ranking (five candidates) | Rank, then say what separates top from bottom | Push past "it's longer" |
| 50–60 | **Core checkpoint:** fourth commit, unguided | Edit interpretation, partner reviews `git diff`, commit | Do not supply the commands again |
| 60–70 | Collaboration map: issue → branch → PR → review → merge | Label which actions are local and which are GitHub | Projected example; no login bottleneck |
| 70–77 | Undo-safely table and the five scenario cards | Choose stop / inspect / ask for each | No force-push, no history rewriting |
| 77–80 | Exit ticket | Individual response | Record GitHub access follow-up |

### Anticipated stuck points

- **The editor trap.** Someone will run `git commit` without `-m` and land in Vim. `Esc`, `:q!`,
  Enter. Say this out loud *before* it happens; it costs ten seconds and saves three minutes of
  quiet panic.
- **Wrong directory.** Any Git command outside the practice folder. Re-establish `pwd` before
  anything else; never run `git init` to clear the error message.
- **`git add .`** — intercept it. It is the habit that later commits a 40 MB archive.
- **"But I committed it, so it's saved."** Local only. Ask what would happen if the laptop were
  stolen tonight.

### Recovery and cut order

- If Git identity is missing, set the student's own name and email for the disposable repository
  only.
- If a pair leaves the generated folder, stop and re-establish `pwd` before any Git command.
- **Cut in this order:** the scenario cards, then the collaboration map (keep a 60-second verbal
  version), then the message-ranking exercise. Preserve the four commits, the staged-diff
  inspection, and `.gitignore`.
- Never repair the class by force-pushing, rewriting student history, or deleting a repository.

## Wednesday debrief

- How many students could name a failure before editing code? That is session 1's real measure.
- How many wrote a function that actually removed repetition, versus a function with a hard-coded
  column inside?
- Did the difference-panel decision produce the intended argument about physical quantities?
- How many pairs completed four commits, and did anyone commit `figures/`?
- Which Git term remained ambiguous: stage, commit, branch, push, or pull request?
- Who still needs GitHub or Copilot access support before Friday?
