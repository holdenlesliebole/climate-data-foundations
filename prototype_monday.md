# Monday novice-first prototype

This branch prototypes a lower-floor, high-ceiling structure for students who may never have written
code. It changes the default Monday path without discarding the existing material.

## What changed

- The first lesson now treats running cells, naming values, recognizing arrays, and making a first
  labeled plot as the complete beginner outcome.
- Indexing, Boolean selection, missing-value decisions, loops, functions, and formal checks remain
  available in a clearly separated **Go further** path.
- The Pier lesson still requires students to find, download, inspect, and load the provider file.
  Plotting is expanded into a small visualization studio: time series, histogram, and scatterplot.
- Completed references appear beside their student notebooks in the daily navigation instead of in
  a distant solutions section.
- A new [choosing a plot](notes/plotting_foundations.md) page gives students a durable question-to-
  format guide and a minimum-viable-figure checklist.

## Suggested review route

1. Read [Python from zero: values, arrays, and a first plot](notebooks/01_python_numpy.ipynb).
2. Compare its core stopping point with its **Go further** section.
3. Read [From source to figure](notebooks/02_source_to_figure.ipynb), especially the visualization
   studio.
4. Check whether each [completed Monday 1 reference](reference/01_python_numpy_complete.ipynb) and
   [completed Monday 2 reference](reference/02_source_to_figure_complete.ipynb) would be useful after
   class without replacing the thinking students do in class.
5. Use the questions below to leave comments on the draft pull request.

## Questions for Connor and Izzy

- Could a student who has never coded reach the core checkpoint without being rushed?
- Is the boundary between core and **Go further** obvious?
- Do students make enough plots, and do the formats answer genuinely different questions?
- Which plotting decision still needs a more explicit worked example?
- What should be cut before anything else if downloading the Pier archive takes longer than planned?

:::{note}
This is a pedagogical prototype, not a second permanent curriculum. If the structure works, the same
lesson pattern can be applied to Tuesday through Friday before the branch is merged.
:::
