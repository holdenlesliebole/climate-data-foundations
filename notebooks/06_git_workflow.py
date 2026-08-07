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
# # Version control: five commands you will use every week
#
# Git answers a question that gets harder every week of a research project: *what did I have, and
# when did I have it?* Today you build a history you can read, in a folder you can throw away.
#
# **Minimum viable takeaway:** `status → diff → add → commit → log`. Look at exactly what you are
# about to record, then record it with a message that says why.
#
# **You do not need to finish the whole notebook.** The core path ends at the **Core checkpoint**
# after section 6. Branches, pull requests, and conflicts are **Go further**.
#
# :::{tip} Need an example?
# The [annotated completed reference](../reference/06_git_workflow_complete.ipynb) has every command
# with its expected output, plus the fixes for the problems that actually happen.
# :::
#
# :::{warning} Type Git commands in the VS Code **terminal**, not in this notebook.
# The notebook is here to explain each step and to inspect the result. Every command block below is
# meant to be typed at a terminal prompt inside the practice folder.
# :::

# %% [markdown]
# ## Learning objectives
#
# By the core checkpoint, you can:
#
# - explain working tree, staging area, and commit in plain language;
# - read a short project history and say what happened;
# - run `git status`, `git diff`, `git add`, `git commit`, and `git log` deliberately;
# - inspect exactly what a commit will contain **before** making it;
# - write a commit message that a collaborator (or you, in March) can use; and
# - keep generated files and data out of a repository.

# %% [markdown]
# ## 1. Worked example: read a history you did not write
#
# Before running any command, read this. It is the output of `git log --oneline` for a small
# analysis project, newest commit at the top.
#
# ```text
# 9f2c1ab Exclude 2019 from the trend after finding the sensor swap
# 4ad77e0 Add the annual mean figure
# c81b3e5 Restrict the analysis to quality flag 0
# 2e90f4d Load the Pier temperature record
# 71bb0c9 Describe the question and the data source
# ```
#
# With your partner, answer:
#
# 1. What was this person trying to find out? **TODO**
# 2. Which commit records a **scientific decision** rather than a mechanical step? **TODO**
# 3. Which one would you want to read the diff of first, and why? **TODO**
# 4. Six months later, the trend looks wrong. Which commit do you go back to? **TODO**
#
# That is the whole point of version control, and none of it is about software. A good history is a
# record of decisions with reasons attached. This is also why `update files` and `fixes` are bad
# commit messages: they answer "what changed" — which Git already knows — instead of "why."

# %% [markdown]
# ## 2. The model: four places a file can be
#
# ```text
# working tree  --git add-->  staging area  --git commit-->  local history  --git push-->  remote
#      ↑                            ↑                             ↑
#   git diff                 git diff --cached                 git log
# ```
#
# - **Working tree:** the files as they are on disk right now.
# - **Staging area:** your proposal for the next snapshot. Nothing is recorded yet.
# - **Local history:** the commits, on your machine only.
# - **Remote:** a copy elsewhere, usually GitHub. Nothing reaches it until you `push`.
#
# The staging area is the part beginners skip and later wish they had not. It exists so you can
# record *one coherent change* even when you have three unrelated edits open.
#
# **Predict:** you edit one file and run `git commit -m "..."` without `git add`. What happens?
# **TODO**

# %% [markdown]
# ## 3. Create a disposable project
#
# In the VS Code terminal, from the **course root**:
#
# ```bash
# python scripts/setup_git_practice.py
# cd data/processed/git_practice
# pwd
# ls
# ```
#
# The last two commands are not filler. Say the folder name out loud before continuing. Almost every
# Git accident in a first course begins with running a command in the wrong directory.
#
# The setup script refuses to overwrite an existing practice folder. To start over later, keep the
# old one and use `python scripts/setup_git_practice.py --name git_practice_2`.

# %%
from pathlib import Path
import subprocess

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
GIT_PRACTICE = PROJECT_ROOT / "data" / "processed" / "git_practice"


def git_output(*args):
    """Return stdout for a read-only Git command in the practice repository."""
    if not GIT_PRACTICE.exists():
        return "The practice folder does not exist yet. Run the setup script above."
    if not (GIT_PRACTICE / ".git").exists():
        return "The practice folder exists but is not a repository yet. Run `git init` in it."
    completed = subprocess.run(
        ["git", *args], cwd=GIT_PRACTICE, text=True, capture_output=True,
    )
    if completed.returncode != 0:
        return f"Git reported a problem: {completed.stderr.strip()}"
    return completed.stdout.strip() or "(no output)"


print("Practice repository:", GIT_PRACTICE)
print("Exists:", GIT_PRACTICE.exists())

# %% [markdown]
# ## 4. Initialize and look before you touch anything
#
# **Predict first:** after `git init`, how many files will `git status` list, and in what category?
#
# ```bash
# git init -b main
# git status
# ```
#
# Git reports three untracked files. Untracked means Git can see them but has never recorded them
# and is not watching them. Nothing is in history yet — `git init` creates an empty repository, not
# a snapshot.
#
# The `-b main` names the first branch. Without it, Git prints a several-line hint and may use
# `master`, which will not match the `main` branch every other part of this course refers to. Naming
# it explicitly avoids both.

# %%
print(git_output("status", "--short"))

# %% [markdown]
# ### If Git asks who you are
#
# The first commit may fail with a message about `user.email` and `user.name`. Set them for **this
# practice repository only** (no `--global`), using your own details:
#
# ```bash
# git config user.name "Your Name"
# git config user.email "you@ucsd.edu"
# ```
#
# Never copy an instructor's identity: commit authorship is a record of who did the work.

# %% [markdown]
# ## 5. Commit 1 — the purpose
#
# Run these one at a time and read the output of each before typing the next:
#
# ```bash
# git add README.md
# git status
# git diff --cached
# git commit -m "Describe the practice analysis and how to run it"
# git log --oneline
# ```
#
# What each one did:
#
# - `git add` moved the README into the staging area. The file on disk did not change.
# - `git status` now shows it under "Changes to be committed," and the other two files still
#   untracked.
# - `git diff --cached` shows the exact content of the proposed snapshot. This is the habit worth
#   building: **look at what you are recording before you record it.**
# - `git commit` wrote the snapshot into local history, on your machine, uploaded nowhere.
#
# :::{warning} If your terminal suddenly fills with text and will not accept commands
# You ran `git commit` without `-m`, so Git opened a text editor for the message. If the screen says
# `~` down the left side you are in Vim: press `Esc`, then type `:q!` and press Enter. If the bottom
# shows `^X Exit` you are in nano: press `Ctrl` and `X`. Then run the commit again **with** `-m`.
# This happens to everyone once.
# :::

# %%
print("Status:\n", git_output("status", "--short"))
print("\nHistory:\n", git_output("log", "--oneline"))

# %% [markdown]
# ## 6. Commit 2 — the code, and something new appears
#
# Run the analysis before you commit it. Committing code you have not run is how a broken script
# enters a project's history.
#
# ```bash
# python analysis.py
# git status
# ```
#
# **Predict before running `git status`:** the script printed a mean and wrote a figure. What will
# `git status` show that it did not show before?

# %% [markdown]
# A new untracked `figures/` folder appeared. Now the decision: **should the figure be in your
# history?**
#
# It should not, and the reasoning generalizes:
#
# - it is **generated** — `analysis.py` recreates it any time, so storing it duplicates information;
# - binary files cannot be diffed, so every rerun looks like a large opaque change;
# - the same argument applies, much more strongly, to raw data, NetCDF files, and anything with a
#   credential in it.
#
# Create a `.gitignore` file in the practice folder containing:
#
# ```text
# figures/
# __pycache__/
# ```
#
# Then commit the code and the ignore rule as two separate, coherent changes:
#
# ```bash
# git add analysis.py
# git diff --cached
# git commit -m "Add the temperature summary and figure script"
#
# git status
# git add .gitignore
# git commit -m "Ignore generated figures and caches"
# git status
# ```
#
# The final `git status` should no longer mention `figures/` — only `interpretation.md`, which you
# have not committed yet. Git is not deleting the figure; it is agreeing not to track it.

# %%
print("Status:\n", git_output("status", "--short"))
print("\nHistory:\n", git_output("log", "--oneline"))

# %% [markdown]
# ### Which message would you rather find in six months?
#
# All five describe the same change. Rank them, then say what separates the top from the bottom.
#
# ```text
# a. update
# b. changed analysis.py
# c. Fixed stuff after the meeting
# d. Add the temperature summary and figure script
# e. Add temperature summary script; uses Agg backend so it runs headless on the lab machines
# ```
#
# **My ranking:** TODO
#
# **What separates them:** TODO
#
# A useful message finishes the sentence "If applied, this commit will…" and adds *why* when the why
# is not obvious. Length is not the point; (e) is long because it carries a real reason, not because
# longer is better.

# %% [markdown]
# ## Core checkpoint — one commit with no instructions
#
# Do this loop yourself, without looking at the commands above.
#
# 1. Open `interpretation.md` and replace the TODO with one bounded sentence: what the four values
#    show, plus the fact that they are invented example values rather than observations.
# 2. Before staging, have your partner run `git diff` and read your change back to you.
# 3. Stage it, inspect the staged diff, and commit it with a message you chose.
# 4. Run `git log --oneline` and `git status`.
#
# You should end with four commits and a clean status.

# %%
print("Status (clean means the working tree matches the last commit):")
print(git_output("status", "--short"))
print("\nHistory:")
print(git_output("log", "--oneline", "--decorate", "--max-count=6"))

# %% [markdown]
# ### Checkpoint questions
#
# - What does `git diff --cached` show that `git diff` does not? **TODO**
# - Your history has four commits. Could a stranger reconstruct what you did, in order? **TODO**
# - A clean `git status` means: **TODO**
#   It does **not** mean the analysis is correct, or that anything has been uploaded anywhere.
#
# :::{tip} Compare with the completed reference
# This is the end of the core path. Open the
# [annotated reference](../reference/06_git_workflow_complete.ipynb) and read the "common problems
# and fixes" section before continuing — it covers the five situations most likely to happen to you
# this year.
# :::

# %% [markdown]
# ## Exit ticket
#
# In one sentence each:
#
# - `git add` does: **TODO**
# - `git commit` does: **TODO**
# - `git push` would do: **TODO**
# - One reason to inspect `git diff --cached` before committing: **TODO**

# %% [markdown]
# ---
#
# # Go further

# %% [markdown]
# ### A. Undo, safely
#
# The commands people actually need in their first month, none of which destroy work:
#
# ```bash
# git restore --staged notes.md   # staged the wrong file; unstage it, keep the edit
# git restore notes.md            # discard edits to a file since the last commit (this DOES lose them)
# git commit --amend -m "Better message"   # fix the message of the commit you just made
# git show HEAD                   # read the last commit in full
# git log -p interpretation.md    # every change ever made to one file
# ```
#
# Try `git restore --staged` in the practice repository: stage a change, check `git status`, unstage
# it, and check again. Nothing is lost.
#
# Not on this list: `git reset --hard`, `git push --force`, and rewriting published history. When
# you think you need one of those, stop and ask someone. Almost nothing in Git is irreversible
# *except* those.

# %% [markdown]
# ### B. Branches and pull requests
#
# ```bash
# git switch -c improve-readme
# # edit README.md
# git add README.md
# git commit -m "Explain what the figure shows"
# git switch main
# git log --oneline --all --graph
# ```
#
# A branch is a movable label pointing at a line of commits. Your edit exists on `improve-readme`
# and not on `main`, which is the point: unfinished work does not disturb the version everyone else
# is using.
#
# On GitHub, a **pull request** proposes that a branch be reviewed and merged. It is a conversation
# attached to a set of commits, not a Git command. The course repository's loop:
#
# ```text
# issue → one active lesson owner → short branch → commits → draft pull request
#       → another instructor reviews → automated checks → merge into protected main
#       → GitHub Pages publishes the reviewed main
# ```
#
# Before requesting review: sync `main`, read every changed file, run the notebook from a fresh
# kernel, run the tests, and say what you are still unsure about.

# %% [markdown]
# ### C. Why notebooks are hard to review
#
# An `.ipynb` file is JSON containing your code, the outputs, and execution counters. Two people
# editing the same notebook produce a conflict that is nearly unreadable, and every rerun changes
# the file even when the code did not.
#
# This course pairs every notebook with a Jupytext `.py` file so reviewers get a readable line diff.
# The working rules:
#
# - one active editor per notebook at a time;
# - students open the `.ipynb`; reviewers read the `.py`;
# - `jupytext --sync` after editing either one, so the pair stays consistent;
# - never resolve a notebook conflict by picking one whole version blindly;
# - a clean text diff does not prove the notebook runs. Restart and run it.
#
# Compare the two representations of any course notebook in VS Code and see which one you would
# rather review.

# %% [markdown]
# ### D. Situations to think through, not to perform
#
# For each, say what you would do **first** — stop, inspect, or ask:
#
# 1. `git status` lists 400 changed files and you only edited one.
# 2. You committed a file containing an API key.
# 3. Two people edited the same notebook cell and the merge shows `<<<<<<<` markers.
# 4. A collaborator says "just force-push over it."
# 5. You are about to commit the 40 MB Pier archive.
#
# In every one of these the correct first move is to inspect and ask, never to repair by deleting or
# rewriting history. A secret that reached a shared remote must be **rotated**, not just removed
# from the next commit — the old commit still contains it.

# %% [markdown]
# ### E. Continuation
#
# Initialize a repository for your own final-assignment folder, write its `.gitignore` **before**
# the first commit, and make one commit per real step of the analysis. On Friday you will make a
# final commit of the submitted notebook; today's habits are what make that a two-minute task.
