# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Version control with Git — completed reference
#
# Git records a sequence of deliberate project snapshots. GitHub adds shared hosting, review, issues, and pull requests; it is not a replacement for understanding the local history.

# %% [markdown]
# ## The local model
#
# ```text
# working tree --git add--> staging area --git commit--> local history
# ```
#
# A file can therefore be untracked, modified, staged, or committed. `git status` tells you which state applies.

# %% [markdown]
# ## Safe disposable-repository exercise
#
# From the **course root**, create the practice files once:
#
# ```bash
# python scripts/setup_git_practice.py
# cd data/processed/git_practice
# git init
# git status
# ```
#
# Keep every command in this generated folder. It contains no course source files.

# %% [markdown]
# ## Three focused commits
#
# Commit the purpose first:
#
# ```bash
# git add README.md
# git diff --cached
# git commit -m "Document practice analysis"
# ```
#
# Then commit the analysis separately:
#
# ```bash
# git add analysis.py
# git diff --cached
# git commit -m "Add temperature summary"
# ```
#
# Finally, write a short interpretation in `interpretation.md`, inspect it, and commit it:
#
# ```bash
# git diff
# git add interpretation.md
# git diff --cached
# git commit -m "Interpret temperature summary"
# git status
# git log --oneline --max-count=3
# ```

# %% [markdown]
# ### If Git asks for your identity
#
# Set it for only this disposable repository, replacing the values with your own:
#
# ```bash
# git config user.name "Your Name"
# git config user.email "you@example.edu"
# ```
#
# Do not copy an instructor's identity. Authentication to GitHub is a separate step.

# %%
from pathlib import Path
import subprocess

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name in {"notebooks", "reference"}:
    PROJECT_ROOT = PROJECT_ROOT.parent
PRACTICE_REPO = PROJECT_ROOT / "data" / "processed" / "git_practice"
print(PRACTICE_REPO.relative_to(PROJECT_ROOT))


# %%
def git_output(*args):
    """Run a read-only Git inspection command in the practice repository."""
    if not (PRACTICE_REPO / ".git").exists():
        return "Practice repository is not initialized yet. Follow the commands above."
    completed = subprocess.run(
        ["git", *args], cwd=PRACTICE_REPO, text=True, capture_output=True,
    )
    if completed.returncode != 0:
        return completed.stderr.strip()
    return completed.stdout.strip()

print("Working-tree status:")
print(git_output("status", "--short") or "clean")
print("\nRecent commits:")
print(git_output("log", "--oneline", "--max-count=3"))

# %% [markdown]
# ## A repeatable collaboration loop
#
# ```text
# issue → short branch → small commits → draft pull request → review → QA → merge
# ```
#
# Before asking for review, sync current `main`, inspect every changed file, run the notebook or tests, and describe what remains uncertain. The pull request should answer: what changed, why, how it was checked, and what the reviewer should examine closely.

# %% [markdown]
# ## Notebook-specific rule
#
# Only one person actively edits a given notebook at a time. This course pairs each `.ipynb` with a Jupytext `.py` file so pull-request review has readable line changes. Run the notebook from a fresh kernel before merging; the text diff cannot prove that execution succeeds.

# %% [markdown]
# ## What the commands establish
#
# - `git diff` shows unstaged changes.
# - `git diff --cached` shows exactly what the next commit would contain.
# - `git log --oneline` shows local history.
# - a clean `git status` means the working tree matches the latest commit.
#
# None of these establish scientific correctness, successful upload, or peer review. Those require tests, interpretation, a remote push, and a pull request.

# %% [markdown]
# ## Exit ticket
#
# Explain the difference between `git add`, `git commit`, and a GitHub pull request. Name one check you would complete before asking a collaborator to merge your work.
