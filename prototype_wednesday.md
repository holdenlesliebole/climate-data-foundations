# Wednesday novice-first prototype

This branch applies the Monday prototype's structure to Wednesday, and adds the pieces that the
Monday branch deliberately left open. It is the second test of the pattern described in the
[Monday prototype guide](prototype_monday.md), not a separate curriculum.

Every session is now three layers:

1. **Worked example** — complete code the class reads, predicts, and modifies.
2. **Core path** — a short scaffolded exercise every beginner can finish.
3. **Go further** — most of the previous material, retained for students who are ready.

## What changed

### Wednesday 1 — errors, functions, and one honest check

- The session now **introduces** functions instead of refactoring toward them. Monday's core no
  longer teaches `def`, so Wednesday cannot assume it.
- The vehicle is the repeated plotting code students have actually written, which is also this day's
  contribution to the week's visualization spine: *turn repeated plotting code into a function*.
- A traceback lab comes first. Three failures — `NameError`, `FileNotFoundError`, `KeyError` — each
  read last-line-first, each answered by one print. These are the three errors that will otherwise
  cost students hours in the fall.
- The check students add is a **plausible-range assertion** on sea temperature. The notebook then
  passes it a Fahrenheit series so the class watches it reject a figure that is clean, labeled, and
  wrong by thirty degrees.
- The core checkpoint ends with a decision rather than an answer: the surface-minus-bottom panel
  legitimately fails the −2 to 40 °C check. Widen the range, or write a separate one? The intended
  argument is that a temperature and a temperature difference are different physical quantities.
- The Pier loader, `ValueError` versus `assert`, known-value tests, and the `pytest` suite all moved
  into **Go further**. They are unchanged, just no longer the entry point.

### Wednesday 2 — version control

- Opens by **reading a five-commit history nobody wrote**, before any command is typed. The
  questions are about scientific decisions, not syntax.
- Core is `status → diff → add → commit → log`, four times, in a disposable project.
- The practice project now mirrors session 1: a script with a plotting function that writes a
  figure. Running it makes an untracked `figures/` folder appear, which motivates `.gitignore` from
  evidence rather than from a rule. Friday's submission depends on this habit.
- The fourth commit is the **core checkpoint** and comes with no commands — the loop, unaided.
- A commit-message ranking exercise replaces exhortation about good messages.
- Branches, pull requests, notebook diffs, and conflict scenarios moved into **Go further**.
- The reference gained a **common problems and fixes** section, including the editor trap: `git
  commit` without `-m` drops a novice into Vim, and nothing in the previous material mentioned it.

### Supporting changes

- New [errors, functions, and checks](notes/functions_and_errors.md) note: a traceback field guide,
  a table of the errors students will actually hit, function anatomy, and what a check does and does
  not establish.
- [Git and GitHub](notes/git_and_github.md) gained a safe-undo table, `.gitignore`-before-first-commit
  guidance, and the common-problems section.
- [Choosing and improving a plot](notes/plotting_foundations.md) gained the **six-question figure
  check** used in every session, and a short section on turning repeated plotting code into a
  function.
- `git init -b main` throughout. On a machine that has never set `init.defaultBranch`, plain
  `git init` prints a five-line hint and creates `master`, which then disagrees with every other
  mention of `main` in the course.
- `example_pier_frame()` in `src/climate_course/pier.py` gives Wednesday 1 a provider-shaped
  fallback so a failed Monday download cannot cost a student the whole session. The instructor
  recovery file remains the preferred route; this is the last resort, and the notebook prints which
  source it used.
- Completed references appear **beside** their student notebooks in the Wednesday navigation, and
  each core section of the reference ends with a **common mistakes** box describing what actually
  goes wrong.

## Suggested review route

1. Read [Code you can trust](notebooks/05_reliable_code.ipynb) and stop at the core checkpoint.
   Would a student who first opened a notebook on Monday get there?
2. Read the [annotated reference](reference/05_reliable_code_complete.ipynb), especially the
   **common mistakes** boxes. Do they describe your students?
3. Read [Version control](notebooks/06_git_workflow.ipynb), particularly the worked history in
   section 1 and the `.gitignore` moment in section 6.
4. Check the [Wednesday run-of-show](https://github.com/holdenlesliebole/climate-data-foundations/blob/lesson/wed-novice-core/instructor_notes/wednesday_run_of_show.md)
   timings against your experience of an 80-minute session.

## Questions for the teaching team

- Wednesday 1 assumes Monday's core did **not** teach functions. If Monday keeps them in the core,
  this session should change. Which is it?
- Is the traceback lab worth twelve minutes, or should it be eight and the function get more?
- Four commits in session 2, or three? The fourth is the unguided one, which is the part that
  actually tests the loop.
- The plausible-range check bakes a Celsius assumption into a plotting helper. That is deliberate
  and it is discussed in the reference — but is it teaching a habit we would want them to keep?
- Should the six-question figure check be adopted across all five days, and are 1/2/5/6 the right
  four to make mandatory?
- What gets cut first if the room is slower than planned? The run-of-show proposes an order.

:::{note}
Like the Monday branch, this is a pedagogical prototype. If both work, the same pattern should be
applied to Tuesday, Thursday, and Friday before either branch merges.
:::
