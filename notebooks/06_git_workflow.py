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
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Version control with Git
#
# Git records meaningful snapshots of a project. A remote GitHub repository adds sharing, review, and resilience, but the local history comes first.
#
# **Minimum viable takeaway:** use `status` and `diff` to understand changes, stage only the intended files, and make a commit whose message explains one coherent step.

# %% [markdown]
# ## Learning objectives
#
# By the end, you can:
#
# - explain working tree, staging area, commit, branch, and remote in plain language;
# - use `git status`, `git diff`, `git add`, `git commit`, and `git log`;
# - create two small commits with meaningful messages;
# - inspect exactly what will enter a commit;
# - describe how a branch/pull-request review protects a shared course or research repository.

# %%
from pathlib import Path
import subprocess

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
GIT_PRACTICE = PROJECT_ROOT / "data" / "processed" / "git_practice"
print("Practice repository will be:", GIT_PRACTICE.relative_to(PROJECT_ROOT))


# %% [markdown]
# ## 1. Create a disposable project
#
# In the VS Code terminal at the course root:
#
# ```bash
# python scripts/setup_git_practice.py
# cd data/processed/git_practice
# ls
# ```
#
# The setup script refuses to overwrite an existing practice folder. To repeat later, preserve the old folder and use `python scripts/setup_git_practice.py --name git_practice_2`.

# %% [markdown]
# ## 2. The local Git model
#
# ```text
# working tree --git add--> staging area --git commit--> local history
#      inspect: git diff       inspect: git diff --cached      inspect: git log
# ```
#
# - **Working tree:** files you currently see/edit.
# - **Staging area:** the exact next snapshot proposal.
# - **Commit:** a named snapshot plus parent/history.
# - **Branch:** a movable name pointing through a line of commits.
# - **Remote:** another repository copy used for sharing; GitHub is one remote host.

# %% [markdown]
# ## 3. Initialize and inspect—do not stage yet
#
# Predict what `status` will list, then run:
#
# ```bash
# git init
# git status
# ```
#
# Git reports the three generated files as untracked. Nothing is in history yet. If Git asks for your identity during the first commit, configure it for this practice repository only:
#
# ```bash
# git config user.name "Your Name"
# git config user.email "your GitHub noreply or course email"
# ```

# %% [markdown]
# ## 4. First commit: project purpose
#
# Stage only the README, inspect the staged diff, then commit:
#
# ```bash
# git add README.md
# git status
# git diff --cached
# git commit -m "Describe the tiny climate analysis"
# git log --oneline
# ```
#
# A strong message uses an imperative verb and describes why this coherent snapshot exists. `update files` does not help your future self.

# %%
def git_output(*args):
    """Return stdout for a read-only Git command in the practice repository."""
    completed = subprocess.run(
        ["git", *args], cwd=GIT_PRACTICE, text=True, capture_output=True,
    )
    if completed.returncode != 0:
        return f"Git not ready: {completed.stderr.strip()}"
    return completed.stdout

print(git_output("status", "--short"))
print(git_output("log", "--oneline", "--max-count=3"))

# %% [markdown]
# After the first commit, `analysis.py` and `interpretation.md` remain untracked. That is expected: the first snapshot intentionally contained only the project purpose.

# %% [markdown]
# ## 5. Second commit: runnable analysis
#
# Inspect and run the script before committing it:
#
# ```bash
# python analysis.py
# git diff
# git add analysis.py
# git diff --cached
# git commit -m "Calculate the example mean temperature"
# ```
#
# `git diff` was empty because untracked files are not automatically shown as line diffs. `status` identifies them; staging creates a diff proposal.

# %% [markdown]
# ## 6. Edit, review, and commit an interpretation
#
# Open `interpretation.md` in VS Code and replace the TODO with one bounded sentence that reports the approximate mean and says it describes only four generated values. Save it.
#
# Before staging, ask your partner to review:
#
# ```bash
# git status
# git diff
# ```
#
# Then stage, inspect, and commit:
#
# ```bash
# git add interpretation.md
# git diff --cached
# git commit -m "Interpret the four-value temperature mean"
# git log --oneline --decorate
# git status
# ```

# %%
print("Status after exercise:")
print(git_output("status", "--short"))
print("Recent history:")
print(git_output("log", "--oneline", "--decorate", "--max-count=5"))

# %% [markdown]
# A clean final `status` means the working tree matches the latest commit. It does not mean the analysis is scientifically correct or uploaded anywhere.

# %% [markdown]
# ## 7. From local history to collaboration
#
# For the co-instructor course repository, the intended flow is:
#
# ```text
# issue → one active lesson owner → short branch → commits → draft pull request
#       → another instructor reviews → automated notebook checks → merge to protected main
#       → GitHub Pages publishes reviewed main
# ```
#
# A pull request is a proposal and discussion around commits. A branch keeps unfinished work from changing the reviewed course. The remote is useful only because the local commits already express understandable steps.

# %% [markdown]
# ### Notebook-specific collaboration
#
# Notebook JSON is conflict-prone. Course authors use one active editor per notebook, paired Jupytext `.py` sources for readable diffs, and `nbdime` for notebook-aware inspection. Students still open `.ipynb`. Do not resolve a notebook conflict by blindly choosing one whole version.

# %% [markdown]
# ## Exit ticket
#
# In one sentence each:
#
# - `git add` does: **TODO**
# - `git commit` does: **TODO**
# - `git push` would do: **TODO**
# - One reason to inspect `git diff --cached` is: **TODO**

# %% [markdown]
# ## Continuation lane
#
# Create a branch named `improve-readme`, change one sentence, make a commit, switch back to the default branch, and compare histories. If the instructor provides a shared remote practice repository, push the branch and open a pull request; another pair reviews without merging until the change and checks are understood.
