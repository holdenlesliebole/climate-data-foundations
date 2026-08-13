# Climate Data Foundations

Welcome! This is a five-day, low-stakes introduction to the computational tools used throughout a
climate-science master's program. The goal is not to memorize Python. It is to leave with a workable
research routine, a set of examples you understand, and notes you can return to later.

The afternoon course consists of two 80-minute sessions per day. Students arrive with many kinds of
experience, so each lesson begins with a worked example, continues through a **core path**, and ends
with a clearly labeled **Go further** path. Complete the core checkpoint before moving to extensions.

## What you will be able to do

By the end of the week, you should be able to:

- find, acquire, preserve, and document a small climate dataset;
- load tabular and NetCDF data with pandas and xarray;
- inspect dimensions, columns, metadata, units, missing values, and quality flags;
- make a labeled figure and write a bounded interpretation;
- use Copilot or another coding assistant while keeping a visible verification trail;
- turn repeated work into a small function with an assertion or test;
- record meaningful project history with Git; and
- apply introductory statistical ideas without hiding their assumptions or limitations.

## Lecture slides

The decks used in class. Each one opens in your browser, works offline once loaded, and covers the
ideas, the notebooks, and what to do step by step. Arrow keys move through them; press `↓` to reveal
a whole slide at once.

::::{grid} 1 1 3 3

:::{card} Wednesday
:link: https://holdenlesliebole.github.io/climate-data-foundations/slides/wednesday_deck.html
**Getting unstuck** — the terminal, reading error messages, acquiring data, Git and GitHub, and
keeping notes an AI can use.
:::

:::{card} Thursday
:link: https://holdenlesliebole.github.io/climate-data-foundations/slides/thursday_deck.html
**How sure are you?** — distributions, spread against uncertainty, data health, and the bootstrap.
:::

:::{card} Friday
:link: https://holdenlesliebole.github.io/climate-data-foundations/slides/friday_deck.html
**Two things that move together** — correlation, fitted lines, residuals, trends, and the final
analysis brief.
:::

::::

These addresses are stable, so they are safe to bookmark or paste into a message.

## Begin here

1. Read the [setup guide](notes/setup.md) before the first class.
2. Open and run the [setup check](notebooks/00_setup_check.ipynb).
3. Keep the [paths and data-inspection cheatsheet](cheatsheets/paths_and_data_inspection.md) nearby.
4. When something breaks, open [errors, functions, and checks](notes/functions_and_errors.md).
5. Use the [student schedule](student_schedule.md) to find each session.

:::{important}
This website is for reading. A web page cannot run Python on its own, so to execute a notebook you
need a copy of the course on your own machine and the course environment set up. The
[setup guide](notes/setup.md) walks through it.
:::

## How lessons work

Most sessions follow the same rhythm:

```text
predict → try → inspect → explain → change one thing → check again
```

Work in pairs when asked, switch driver and navigator roles, and write an answer before asking an AI
tool to propose one. If setup blocks you, use the recovery path and rejoin the scientific task; a
software problem is evidence to diagnose, not evidence that you do not belong in the course.

## Data responsibility

The course intentionally teaches data acquisition rather than handing over only tidy files. Keep
provider files untouched in `data/raw/`, save exact requests and provenance, and write generated
work elsewhere. Never commit credentials, restricted data, or student records.

## Completed references

Completed notebooks for selected lessons are grouped at the end of the navigation. They are for
recovery and later review—not a substitute for predicting, trying, and interpreting during class.
Wednesday keeps its worked examples, hints, core path, and extensions together in its two notebooks.

## Where to go after this week

Two outside resources worth knowing about. Both are free, both are maintained by people who do this
for a living, and between them they cover the two directions this course runs out of time for.

::::{grid} 1 1 2 2

:::{card} Scientific Python Lectures
:link: https://lectures.scientific-python.org/index.html
Tutorials on the scientific Python ecosystem, from the Scientific Python developers. Starts where we
started, with Python, NumPy and matplotlib, and continues into debugging, optimization, image
processing, scikit-learn and SymPy.

**Use it when** you want the language and the array tools properly, rather than as much as one week
allowed.
:::

:::{card} Project Pythia Cookbooks
:link: https://cookbooks.projectpythia.org
Worked example workflows for geoscience, from NCAR, Unidata and the University at Albany. Each
cookbook is a runnable notebook on a real problem: CMIP6 model output, MetPy, EOF analysis, ocean
biogeochemistry, machine learning on Landsat imagery.

**Use it when** you want to see a full analysis end to end in your own field, written by someone who
does it for a living.
:::

::::

The first teaches the tools. The second shows what people build with them.

## Need help?

Start with the reusable notes in this site. If the problem remains, bring an instructor the smallest
failing example plus the exact error, current path, selected environment/kernel, and what you already
checked.
