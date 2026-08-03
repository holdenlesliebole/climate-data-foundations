# Git and GitHub for a small research project

Git records a local history of deliberate snapshots. GitHub hosts a shared copy and adds issues,
pull requests, review, and access control. They are related but distinct: a commit can exist only on
your computer, and pushing a branch does not merge it.

## The four places to keep straight

```text
working tree --git add--> staging area --git commit--> local history --git push--> GitHub
```

- **Working tree:** files you are currently editing.
- **Staging area:** the exact changes selected for the next commit.
- **Local history:** commits saved in your local repository.
- **Remote:** a shared copy such as GitHub.

`git status` is the best first command when you are unsure where you are in this sequence.

## A safe daily loop

```bash
git status
git switch main
git pull --ff-only
git switch -c initials/short-description
```

Edit one bounded piece of work, then inspect before recording it:

```bash
git status
git diff
git add path/to/file
git diff --cached
git commit -m "Describe the completed change"
```

Run the relevant notebook or tests, push the short branch, and open a draft pull request. In the
pull request, state what changed, why, how it was checked, and what deserves special reviewer
attention.

## Good commit boundaries

Prefer a small sequence that tells a story:

- `Document Pier data source`
- `Add Pier loading validation`
- `Explain temperature-difference figure`

Avoid vague messages such as `updates`, giant week-long commits, or commits mixing unrelated lesson
changes. Do not commit passwords, tokens, restricted data, provider archives, generated recovery
files, or environment-specific clutter.

## Three-instructor course workflow

1. Make or claim a lesson issue.
2. Record one active notebook editor and one reviewer.
3. Create a short branch and open a draft pull request early.
4. Keep the notebook and its paired `.py` source synchronized.
5. Reviewer checks pedagogy, scientific meaning, paths, and the readable text diff.
6. A different person runs the notebook from a fresh kernel in the course environment.
7. Resolve review comments, obtain approval, and merge to protected `main`.

Only one instructor should actively edit a particular notebook at a time. Multiple instructors can
still work concurrently on different lessons, notes, tests, or figures.

## Notebook diffs

Raw `.ipynb` files are JSON and can create noisy conflicts. This repository uses Jupytext to pair
each notebook with an adjacent percent-format `.py` file. After editing either member of a pair,
run from the course root:

```bash
jupytext --sync notebooks/03_tools_llms.ipynb
```

Use the `.py` change for line-by-line review, but execute the `.ipynb` from a fresh kernel before
merging. `nbdiff` can provide a notebook-aware local comparison:

```bash
nbdiff main...HEAD -- notebooks/03_tools_llms.ipynb
```

Do not resolve a notebook conflict by accepting one entire side unless you have verified that no
lesson content was lost. Ask the active owner to reconcile the paired source and rerun the notebook.

## Recovery questions

- **Wrong branch?** Stop editing, run `git status`, and ask before moving changes if the correct
  destination is unclear.
- **Commit failed for identity?** Configure your own name and email; authentication is separate.
- **Push rejected?** Fetch/pull and inspect the remote changes. Do not force-push shared history.
- **Data file is huge?** Do not add it. Check `data/README.md` and the manifest/recovery policy.
- **Secret or restricted data staged?** Do not commit or push. Tell the course lead immediately.

Avoid history rewriting, force pushes, recursive deletion, and broad commands until you understand
the target and consequence. A collaborator—or Copilot—can suggest a command but cannot authorize it.
