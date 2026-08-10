# Contributing to Climate Data Foundations

This course is co-authored. Changes should be easy for another instructor to understand, test, and
reverse. The default unit of work is one lesson or one tightly related improvement—not an entire
week in one pull request.

## First-time collaborator setup

1. Accept the repository invitation and confirm you can see
   [`holdenlesliebole/climate-data-foundations`](https://github.com/holdenlesliebole/climate-data-foundations).
2. Clone your own local working copy:

   ```bash
   git clone https://github.com/holdenlesliebole/climate-data-foundations.git
   cd climate-data-foundations
   ```

3. Create the supported environment and run the setup check:

   ```bash
   conda env create --file environment.yml
   conda activate climate-data-foundations
   jupyter lab notebooks/00_setup_check.ipynb
   ```

4. If you will open pull requests from the terminal, install/authenticate GitHub CLI and verify with
   `gh auth status`. The web interface is also sufficient for issues, review, and merging.
5. Do not begin lesson work on `main`. Claim the lesson/issue, update local `main`, and create a
   short-lived branch:

   ```bash
   git switch main
   git pull --ff-only
   git switch -c lesson/short-description
   ```

Every pull request receives two automated checks: **Course checks** runs focused Python tests;
**build** renders the complete student site. Merging to `main` publishes Pages.

## Before editing

1. Find or create a GitHub issue describing the student outcome and affected files.
2. Claim the lesson in `planning/lesson_owners.md`.
3. Confirm that nobody else is actively editing the same notebook.
4. Update local `main`, then create a short branch such as:

```text
lesson/tue-tools-copilot
lesson/wed-reliable-code
fix/pier-header-message
docs/stats-notation
```

Never use a shared long-lived “instructor changes” branch. Small branches reduce conflicts and make
review meaningful.

## Notebook authoring rule

Only one person is the active editor of a given notebook at a time. Other instructors review its
pull request, comment, or edit a different file. Notebooks are JSON documents, and simultaneous edits
to nearby cells are difficult to merge safely.

The `.ipynb` file is the only source for each course notebook. Edit it in JupyterLab or VS Code; do
not hand-edit its JSON. Before committing, restart the kernel, run the notebook top-to-bottom, and
clear incidental outputs or execution counters that are not part of the lesson.

If a notebook conflict occurs, stop and coordinate ownership rather than choosing one whole side.
`nbdime` is available for content-aware inspection:

```bash
nbdiff-web main...HEAD -- notebooks/03_tools_llms.ipynb
```

Run the same core checks used by GitHub before requesting review:

```bash
pytest -q
BASE_URL=/climate-data-foundations npm run site:check
```

## Required lesson pieces

A core lesson pull request should normally include:

- guided notebook;
- completed help, either inside the notebook or in a separate reference when useful;
- concise student notes or cheatsheet update;
- instructor timing, checkpoints, hints, recovery, and cut order;
- exit ticket plus expected reasoning;
- environment/data changes if required;
- a clean top-to-bottom execution report.

Use the shared `lesson_template.md` and the PR checklist. Extensions deepen the same question and do
not become hidden requirements.

## Outputs and data

- Guided notebooks are committed without execution outputs.
- Reference outputs are committed only when needed for the published site and after path, privacy,
  attribution, and data-license review.
- Never commit provider raw files, recovery files, credentials, student work, usernames in paths, or
  unpublished/restricted data.
- Acquisition changes must document provider, URL/request, date/window, variables, local filename,
  flags/units, and an offline recovery route.
- Deliberately broken teaching data must never be placed beside untouched raw data.

## Pull requests and review

Open a draft pull request early for direction; mark it ready only when the core path runs. Every
ready PR needs at least one co-instructor review. The lesson owner cannot provide the only approval
for their own change.

Review in this order:

1. Is the learning target appropriate for the cohort and 80-minute limit?
2. Can a novice rejoin after a setup problem?
3. Are scientific units, metadata, assumptions, and flags correct?
4. Does the core notebook run top-to-bottom in the supported environment?
5. Are extension, reference, instructor notes, and attribution consistent?
6. Is the change safe to publish to students now?

Use suggestions/comments for discussion. Push directly to another instructor's branch only after
asking; otherwise make a follow-up PR.

## Merge and release

- Merge only after required review and automated checks pass.
- Use squash merge for a focused lesson PR unless preserving distinct commits adds real value.
- Delete the merged topic branch.
- Keep `main` deployable; GitHub Pages should deploy only from reviewed `main`.
- Tag the exact release taught in class, for example `2026-bootcamp-v1`.
- Completed references/solutions may have a scheduled release time even when their source exists in
  the private authoring repository.
