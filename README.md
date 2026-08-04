# Climate Data Foundations Bootcamp

Planning materials for a five-day introductory course for incoming climate-science master's
students. The current design assumes two 80-minute afternoon sessions per day, approximately 20
students, and a cohort with widely varying prior experience.

**Student website:** [holdenlesliebole.github.io/climate-data-foundations](https://holdenlesliebole.github.io/climate-data-foundations/)

## Start here

- [`course_plan.md`](course_plan.md): goals, five-day sequence, detailed session plans, data
  strategy, differentiation, staffing, and build priorities.
- [`notes/setup.md`](notes/setup.md): student installation, kernel, VS Code, and setup-check guide.
- [`lesson_template.md`](lesson_template.md): a shared authoring template for the three instructors.
- [`final_assignment_draft.md`](final_assignment_draft.md): a short, student-facing final analysis
  with Pier, MOP, and ERA5 directions and a completion-oriented rubric.
- [`notes/data_loading.md`](notes/data_loading.md): student-facing guide to finding, acquiring,
  preserving, loading, and validating research data.
- [`data/README.md`](data/README.md): the raw/recovery/processed file contract and the two course
  acquisition routes.
- [`publishing_plan.md`](publishing_plan.md): GitHub Pages/Jupyter Book plus Codespaces publication
  architecture to implement after the notebook set is stable.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): the branch, review, notebook-sync, and release workflow for
  all three instructors.
- [`planning/collaboration_workflow.md`](planning/collaboration_workflow.md): one-time GitHub setup,
  branch protection, lesson ownership, and conflict prevention.

## Built notebook sequence

| Session | Guided notebook | Completed reference | Status |
|---|---|---|---|
| Pre-course | [`00_setup_check.ipynb`](notebooks/00_setup_check.ipynb) | not needed | Executed in clean Python 3.12 test environment |
| Monday 1 | [`01_python_numpy.ipynb`](notebooks/01_python_numpy.ipynb) | [`01_python_numpy_complete.ipynb`](reference/01_python_numpy_complete.ipynb) | Executed in clean Python 3.12 test environment |
| Monday 2 | [`02_source_to_figure.ipynb`](notebooks/02_source_to_figure.ipynb) | [`02_source_to_figure_complete.ipynb`](reference/02_source_to_figure_complete.ipynb) | Executed against the current Pier archive |
| Tuesday 1 | [`03_tools_llms.ipynb`](notebooks/03_tools_llms.ipynb) | [`03_tools_llms_complete.ipynb`](reference/03_tools_llms_complete.ipynb) | Executed with generated terminal-practice files in Python 3.12 |
| Tuesday 2 | [`04_remote_data.ipynb`](notebooks/04_remote_data.ipynb) | [`04_remote_data_complete.ipynb`](reference/04_remote_data_complete.ipynb) | Executed with verified seven-day and assignment-sized MOP files |
| Wednesday 1 | [`05_reliable_code.ipynb`](notebooks/05_reliable_code.ipynb) | [`05_reliable_code_complete.ipynb`](reference/05_reliable_code_complete.ipynb) | Executed against current Pier archive; 5 focused tests pass |
| Wednesday 2 | [`06_git_workflow.ipynb`](notebooks/06_git_workflow.ipynb) | [`06_git_workflow_complete.ipynb`](reference/06_git_workflow_complete.ipynb) | Executed against a disposable three-commit repository |
| Thursday 2a | [`07_data_health.ipynb`](notebooks/07_data_health.ipynb) | [`07_data_health_complete.ipynb`](reference/07_data_health_complete.ipynb) | Executed with provider-shaped Pier QA data |
| Thursday 2b | [`08_uncertainty.ipynb`](notebooks/08_uncertainty.ipynb) | [`08_uncertainty_complete.ipynb`](reference/08_uncertainty_complete.ipynb) | Executed with grouped/year-bootstrap Pier QA data |
| Friday 2a | [`09_relationships.ipynb`](notebooks/09_relationships.ipynb) | [`09_relationships_complete.ipynb`](reference/09_relationships_complete.ipynb) | Executed with provider-shaped MOP QA data |
| Friday 2b | [`10_final_analysis.ipynb`](notebooks/10_final_analysis.ipynb) | individual work; no single solution | Starter executed through its default Pier route |

Monday's instructor timing, roles, hints, recovery protocol, and cut points are in
[`instructor_notes/monday_run_of_show.md`](instructor_notes/monday_run_of_show.md). Exit tickets and
interpretation guidance are in
[`instructor_notes/monday_exit_tickets.md`](instructor_notes/monday_exit_tickets.md). The compact
[`paths_and_data_inspection.md`](cheatsheets/paths_and_data_inspection.md) sheet is intended for
student reuse throughout the program.

Tuesday and Wednesday timing, roles, recovery plans, and cut points are in the corresponding files
under [`instructor_notes/`](instructor_notes/). Durable student notes include
[`verified_ai_coding.md`](notes/verified_ai_coding.md) and
[`git_and_github.md`](notes/git_and_github.md).

Thursday and Friday use Mark's theory-first format. Editable theory notes are
[`statistics_foundations_1.md`](notes/statistics_foundations_1.md) and
[`statistics_foundations_2.md`](notes/statistics_foundations_2.md); the corresponding run-of-show,
cut-order, recovery, and exit-ticket guides are under [`instructor_notes/`](instructor_notes/).

## Local setup

```bash
conda env create --file environment.yml
conda activate climate-data-foundations
```

Then open the project in VS Code or JupyterLab, select the course kernel, and run
`notebooks/00_setup_check.ipynb` from top to bottom.

Provider data are not committed. Students acquire Pier and MOP files into `data/raw/` and document
them using `data/manifest_template.yml`. See [`data/assignment_data_plan.md`](data/assignment_data_plan.md)
for the distinct seven-day teaching request and January–July final-assignment request.

## Status

This is a curriculum-design draft with a complete first-pass student sequence. Monday through Friday
now have guided notebooks, completed references for the guided analyses, durable notes, instructor
run-of-show documents, and exit tickets. Thursday/Friday statistical notation and theory depth are
explicitly marked for Mark's review, and the final-analysis starter still needs a confirmed
submission route and a classroom dry run.

Notebooks are paired with adjacent percent-format `.py` sources using Jupytext. Instructors review
the readable text diff and still execute the `.ipynb` from a fresh kernel before merging.

Course source is maintained publicly in
[`holdenlesliebole/climate-data-foundations`](https://github.com/holdenlesliebole/climate-data-foundations).
The student-facing Jupyter Book deploys from reviewed `main` through GitHub Pages. The site is for
reading; students execute notebooks locally until a Codespaces option is configured. Licensing,
completed-reference release timing, Codespaces policy, and the final submission route still require
decisions.
