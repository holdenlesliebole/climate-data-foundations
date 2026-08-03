# Wednesday instructor run-of-show

Assumption: approximately 20 students, ten pairs, three instructors. Session 1 uses the Pier files
acquired Monday. Session 2 uses a generated disposable Git repository and never initializes Git in
the course-data or notebook folders.

## Preflight

- Run Monday's Pier acquisition path and confirm `data/raw/pier/` contains an untouched provider
  archive plus an extracted CSV.
- From the course root, run `pytest -q`; verify all tests pass without provider data or network.
- Run `notebooks/05_reliable_code.ipynb` from a fresh kernel against the current Pier archive.
- Run `scripts/setup_git_practice.py --name git_practice_preflight`; initialize and make three local
  commits inside only that generated folder.
- Confirm Git is installed. Prepare a local-only identity card for students whose commits are
  blocked by missing `user.name` or `user.email`.
- Do not require GitHub authentication in the core lane. Use the course pull-request screenshots or
  a projected instructor repository for the shared-workflow demonstration.

## Session 1: reliable, reusable analysis

**Minimum viable takeaway:** separate data loading from scientific selection and interpretation,
then protect one important assumption with a focused test.

**Core checkpoint by minute 50:** each pair has loaded Pier data through the helper, inspected one
intentional failure, and written assertions for its chosen subset.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–7 | Retrieval: what evidence made Tuesday's file trustworthy? | Name source/shape/units/flags checks | Triage missing Pier files |
| 7–18 | Compare exploratory cells with a small loader function | Identify inputs, outputs, and hidden assumptions | Novice proxy translates vocabulary |
| 18–29 | Read `load_pier_temperature`; trace path/header/column checks | Annotate one check and the failure it catches | Rover handles path issues |
| 29–39 | Demonstrate traceback as evidence | Trigger/read/fix one bounded failure | Ask for last line first, then call chain |
| 39–43 | Break | Switch driver/navigator | Resolve only blockers |
| 43–53 | Select surface/bottom rows; add assertions | Predict before running; inspect rows | Protect units, sensor, and flag choices |
| 53–64 | Extract summary function; test known values | Complete function and hand calculation | Require explicit missing-value rule |
| 64–72 | Run `pytest -q`; connect unit test to regression protection | Read one test and change prediction | Explain what passing does not prove |
| 72–77 | Plot difference and write field note | State pattern, limitation, next check | Extension: add focused test |
| 77–80 | Exit ticket | Individual response | Collect conceptual gaps |

### Recovery and cut order

- If Pier data are unavailable after a three-minute focused diagnostic, use the exact instructor
  recovery file and record the recovery route. Preserve the acquisition discussion from Monday.
- If imports fail, verify project root, environment, and `src/` layout before copying code into the
  notebook.
- Cut the extension test and refactoring comparison first. Preserve traceback reading, assertions,
  one known-value test, and the limits of testing.

## Session 2: Git and collaborative review

**Minimum viable takeaway:** distinguish working tree, staging area, commit, push, and pull request;
inspect the exact change before committing it.

**Core checkpoint by minute 53:** each pair has created a disposable local repository with at least
two focused commits and can explain `git diff --cached`.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–8 | Human snapshot analogy; draw four places | Place command/state cards in order | Check Git installation |
| 8–16 | Generate bounded practice folder; say target aloud | Run setup; `cd`; confirm `pwd` | Enforce disposable-folder boundary |
| 16–29 | `git init`, `status`, `add`, `diff --cached`, `commit` | Commit README; switch roles | Identity card if needed |
| 29–39 | Contrast unstaged/staged/committed | Commit analysis as separate change | Rover checks accidental broad staging |
| 39–43 | Break | Switch roles | Reset explanation, not repository history |
| 43–53 | Edit interpretation; inspect before commit | Make third commit; read log/status | Require meaningful message |
| 53–63 | Project issue → branch → draft PR → review → QA → merge | Label local versus GitHub actions | Use projected example, no login bottleneck |
| 63–72 | Demonstrate readable paired `.py` review | Find changed lesson cell in text diff | Explain one-active-editor rule |
| 72–77 | Conflict/safety scenario cards | Choose stop/inspect/ask response | No force-push or history rewrite |
| 77–80 | Exit ticket | Individual response | Record GitHub access follow-up |

### Recovery and cut order

- If Git identity is missing, set the student's own name/email for the disposable repository only.
- If a pair leaves the generated folder, stop and re-establish `pwd` before any Git command.
- Cut live GitHub authentication and branch-protection settings first. Preserve local state changes,
  staged-diff inspection, meaningful commits, and the pull-request concept.
- Never fix the class by force-pushing, rewriting student history, or deleting a repository.

## Wednesday debrief

- Which helper or test needs clarification before release?
- Could students distinguish an error message from its underlying cause?
- How many pairs completed two or three local commits?
- Which Git term remained ambiguous: stage, commit, branch, push, or pull request?
- Who still needs GitHub/Copilot access support?
