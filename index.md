# Climate Data Foundations

Welcome! This is a five-day, low-stakes introduction to the computational tools used throughout a
climate-science master's program. The goal is not to memorize Python. It is to leave with a workable
research routine, a set of examples you understand, and notes you can return to later.

The afternoon course consists of two 80-minute sessions per day. Students arrive with many kinds of
experience, so each lesson begins with a worked example, continues through a **core path**, and ends
with a clearly labeled **Go further** path. Complete the core checkpoint before moving to extensions.

:::{important}
This preview prototypes a novice-first structure with additional data-visualization practice. If you
are reviewing the revision for the teaching team, start with the
[Monday prototype guide](prototype_monday.md) and the
[Wednesday prototype guide](prototype_wednesday.md).
:::

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

## Begin here

1. Read the [setup guide](notes/setup.md) before the first class.
2. Open and run the [setup check](notebooks/00_setup_check.ipynb).
3. Keep the [paths and data-inspection cheatsheet](cheatsheets/paths_and_data_inspection.md) nearby.
4. Keep the [choosing and improving a plot guide](notes/plotting_foundations.md) nearby.
5. When something breaks, open [errors, functions, and checks](notes/functions_and_errors.md).
6. Use the [student schedule](student_schedule.md) to find each session.

:::{important}
This website is for reading. A GitHub Pages page cannot run Python on its own. Download or clone the
course and use the course environment to execute notebooks. A browser-based Codespaces option will
be added after its institutional access and quota are confirmed.
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

Each completed notebook appears beside its student notebook in the daily navigation. Use it to
recover, compare approaches, or review later—not as a substitute for predicting, trying, and
interpreting during class. Your instructors may suggest a useful moment to compare your work with
the annotated example.

## Need help?

Start with the reusable notes in this site. If the problem remains, bring an instructor the smallest
failing example plus the exact error, current path, selected environment/kernel, and what you already
checked.
