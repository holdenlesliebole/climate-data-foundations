# Climate Data Foundations

A five-day introduction to the computational tools used through a climate-science master's program:
Python, acquiring and documenting real data, reliable code, Git, and introductory statistics.

**Everything is on the course website:**
[holdenlesliebole.github.io/climate-data-foundations](https://holdenlesliebole.github.io/climate-data-foundations/)

The site is for reading. To run the notebooks, get a copy of this repository and set up the course
environment below.

## Set up your machine

```bash
conda env create --file environment.yml
conda activate climate-data-foundations
```

Then open the project in VS Code or JupyterLab, choose the `climate-data-foundations` kernel, and run
[`notebooks/00_setup_check.ipynb`](notebooks/00_setup_check.ipynb) from top to bottom. The full
walkthrough, including what to do when something fails, is in [`notes/setup.md`](notes/setup.md).

## The week

| Day | Session | Notebook | Worked version |
|---|---|---|---|
| Monday | Python and NumPy | [`01_python_numpy.ipynb`](notebooks/01_python_numpy.ipynb) | [complete](reference/01_python_numpy_complete.ipynb) |
| Monday | Source to figure | [`02_source_to_figure.ipynb`](notebooks/02_source_to_figure.ipynb) | [complete](reference/02_source_to_figure_complete.ipynb) |
| Tuesday | Terminal, VS Code, AI tools | [`03_tools_llms.ipynb`](notebooks/03_tools_llms.ipynb) | [complete](reference/03_tools_llms_complete.ipynb) |
| Tuesday | AI-assisted analysis | [`015_ai_assisted_coding.ipynb`](notebooks/015_ai_assisted_coding.ipynb) | — |
| Tuesday | Remote data | [`04_remote_data.ipynb`](notebooks/04_remote_data.ipynb) | [complete](reference/04_remote_data_complete.ipynb) |
| Wednesday | Errors, functions, checks | [`05_reliable_code.ipynb`](notebooks/05_reliable_code.ipynb) | [complete](reference/05_reliable_code_complete.ipynb) |
| Wednesday | Git | [`06_git_workflow.ipynb`](notebooks/06_git_workflow.ipynb) | worked examples in the notebook |
| Thursday | Data health | [`07_data_health.ipynb`](notebooks/07_data_health.ipynb) | [complete](reference/07_data_health_complete.ipynb) |
| Thursday | Uncertainty | [`08_uncertainty.ipynb`](notebooks/08_uncertainty.ipynb) | [complete](reference/08_uncertainty_complete.ipynb) |
| Friday | Relationships | [`09_relationships.ipynb`](notebooks/09_relationships.ipynb) | [complete](reference/09_relationships_complete.ipynb) |
| Friday | Your own analysis | [`10_final_analysis.ipynb`](notebooks/10_final_analysis.ipynb) | your work, no single answer |

The completed versions are for catching up and for later review. Predict, try and interpret first.

## Lecture slides

The decks shown in class. They open in a browser and keep working offline once loaded.

- [Wednesday: getting unstuck](https://holdenlesliebole.github.io/climate-data-foundations/slides/wednesday_deck.html)
- [Thursday: how sure are you?](https://holdenlesliebole.github.io/climate-data-foundations/slides/thursday_deck.html)
- [Friday: two things that move together](https://holdenlesliebole.github.io/climate-data-foundations/slides/friday_deck.html)

## Notes to keep

Written to be useful long after the week ends.

- [`notes/data_loading.md`](notes/data_loading.md): finding, acquiring, preserving, loading and
  checking research data
- [`notes/functions_and_errors.md`](notes/functions_and_errors.md): reading errors, writing
  functions, adding checks
- [`notes/verified_ai_coding.md`](notes/verified_ai_coding.md): using a coding assistant while
  keeping a verification trail
- [`notes/git_and_github.md`](notes/git_and_github.md): the commands you will actually use
- [`notes/statistics_foundations_1.md`](notes/statistics_foundations_1.md) and
  [`_2.md`](notes/statistics_foundations_2.md): distributions, uncertainty, relationships
- [`cheatsheets/paths_and_data_inspection.md`](cheatsheets/paths_and_data_inspection.md): the
  one-page reference for paths and inspecting a new dataset

## Data

Provider files are not committed. You acquire the Pier, MOP, NASA GISTEMP and optional Scripps CO₂
data yourself and record where each one came from, which is part of what the course teaches.

Keep what a provider sent untouched in `data/raw/`, write anything you generate to
`data/processed/`, and fill in [`data/manifest_template.yml`](data/manifest_template.yml) as you go.
The folder contract and every acquisition route are in [`data/README.md`](data/README.md).

## Optional projects

Three self-contained visualisation notebooks sitting beside the weekday sequence, for whenever you
want to try something.

| Project | Notebook | Needs a download? |
|---|---|---|
| Ocean biogeochemistry in 3D | [`045_3d_ccs.ipynb`](notebooks/045_3d_ccs.ipynb) | Yes, plus a free NASA Earthdata Login |
| Chaos and the Lorenz attractor | [`046_lorenz.ipynb`](notebooks/046_lorenz.ipynb) | No, it generates everything |
| The Mandelbrot set | [`047_mandelbrot.ipynb`](notebooks/047_mandelbrot.ipynb) | No, it generates everything |

Each one hides a failure that produces a plausible-looking wrong answer with no error message: a
misspelled `_Fillvalue` that xarray ignores, a separation that saturates and stops meaning anything,
and a zoom that runs out of arithmetic. That is the transferable part; the pictures are the hook.

`plotly` is not in `environment.yml`, so nobody has to rebuild a working environment for an optional
project. The notebooks install it into their own kernel the first time you run them.

The Mandelbrot project was inspired by
[tonigineer/mandelbrot-set](https://github.com/tonigineer/mandelbrot-set), an interactive C++/SFML
implementation worth a look if you want a compiled version. None of its code is used here.

## Final analysis

One small, completion-oriented analysis: a question you can answer with data you already have, one
figure, one number, and an honest paragraph. The brief is in
[`final_assignment_draft.md`](final_assignment_draft.md).

---

## For instructors

Course design, authoring and delivery material. None of it is needed to take the course.

- [`course_plan.md`](course_plan.md): goals, the five-day sequence, session plans, data strategy,
  differentiation, staffing and build priorities
- [`CONTRIBUTING.md`](CONTRIBUTING.md): branch, review, notebook sync and release workflow
- [`lesson_template.md`](lesson_template.md): shared authoring template
- [`instructor_notes/`](instructor_notes/): run-of-show, timing, roles, recovery plans, cut points
  and exit-ticket guidance for each day
- [`planning/collaboration_workflow.md`](planning/collaboration_workflow.md): one-time GitHub setup,
  branch protection and lesson ownership
- [`publishing_plan.md`](publishing_plan.md): Pages and Codespaces publication architecture
- [`slides/README.md`](slides/README.md): editing the lecture decks, the reveal system, and
  regenerating their figures
- [`data/assignment_data_plan.md`](data/assignment_data_plan.md): teaching and final-analysis data
  plan

The `.ipynb` files are canonical. Coordinate one active editor per notebook, use GitHub's rendered
notebook diff or `nbdiff`, and execute from a fresh kernel before publishing.

`python scripts/fetch_cms_ccs.py` acquires the four bounded CMS subsets (~76 MB) for notebook 045;
`python scripts/make_ccs_3d_figures.py` rebuilds its standalone figures. Both routes and their known
server traps are documented in [`data/README.md`](data/README.md) route 4.

### Open decisions

Thursday and Friday statistical notation and theory depth need a review pass. The final analysis
needs a confirmed submission route. Licensing, completed-reference release timing and Codespaces
policy are still undecided.
