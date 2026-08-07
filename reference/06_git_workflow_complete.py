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
# # Annotated reference: version control
#
# The completed version of [Wednesday 2](../notebooks/06_git_workflow.ipynb), with the expected
# output of each command, an explanation of why it behaves that way, and the problems that actually
# happen in a first Git session.
#
# Core check: **Can I say what will be in my next commit before I make it?**

# %% [markdown]
# ## Reading the worked-example history
#
# ```text
# 9f2c1ab Exclude 2019 from the trend after finding the sensor swap
# 4ad77e0 Add the annual mean figure
# c81b3e5 Restrict the analysis to quality flag 0
# 2e90f4d Load the Pier temperature record
# 71bb0c9 Describe the question and the data source
# ```
#
# 1. **The question:** a temperature trend from a quality-screened record, read bottom-up as
#    question → data → screening decision → figure → correction.
# 2. **The scientific decisions** are `c81b3e5` and `9f2c1ab`. Loading a file and adding a figure are
#    mechanical; deciding which observations count is a judgment that changes the answer.
# 3. **Read `9f2c1ab` first.** It excludes a year, which by itself can move a trend. A reviewer wants
#    to see the reason and the size of the effect.
# 4. **Go back to `c81b3e5`**, the point where the screening rule entered. `git show c81b3e5` prints
#    exactly what changed and why.
#
# Notice how much of that was answered from the *messages* alone, without reading a line of code.
# That is the return on writing them well.

# %% [markdown]
# ## The command sequence, with expected output
#
# ```bash
# python scripts/setup_git_practice.py
# cd data/processed/git_practice
# pwd     # confirm you are inside the practice folder before anything else
# git init -b main
# git status
# ```
#
# ```text
# On branch main
#
# No commits yet
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#         README.md
#         analysis.py
#         interpretation.md
# ```
#
# "No commits yet" is the important line. `git init` created an empty repository; it did not record
# anything. Untracked means Git can see these files but has never been told to watch them.
#
# `-b main` names the initial branch explicitly. Plain `git init` on a machine that has never had
# `init.defaultBranch` configured prints a five-line hint and creates `master`, which then disagrees
# with the `main` branch used everywhere else in this course. Both problems disappear with `-b main`;
# alternatively, run `git config --global init.defaultBranch main` once and forget about it.

# %% [markdown]
# ### Commit 1 — purpose
#
# ```bash
# git add README.md
# git status          # README.md now under "Changes to be committed"
# git diff --cached   # the exact content of the proposed snapshot
# git commit -m "Describe the practice analysis and how to run it"
# git log --oneline
# ```
#
# `git add` changed nothing on disk. It recorded an *intention*: this is what the next commit will
# contain. `git diff --cached` is the review step, and it is the habit that separates people who
# trust their history from people who are surprised by it.
#
# After the commit, `analysis.py` and `interpretation.md` are still untracked, which is correct. The
# first snapshot deliberately contains only the project's purpose.

# %% [markdown]
# ### Commit 2 and 3 — the code, then the ignore rule
#
# ```bash
# python analysis.py
# ```
#
# ```text
# mean temperature (C): 16.125
# figure written to: .../git_practice/figures/temperature.png
# ```
#
# `git status` now also lists an untracked `figures/` directory. The prediction question has a
# definite answer: running the analysis created a file, and Git noticed.
#
# ```bash
# git add analysis.py
# git diff --cached
# git commit -m "Add the temperature summary and figure script"
#
# # create .gitignore containing:  figures/  and  __pycache__/
# git add .gitignore
# git commit -m "Ignore generated figures and caches"
# git status
# ```
#
# ```text
# On branch main
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#         interpretation.md
#
# nothing added to commit but untracked files present (use "git add" to track)
# ```
#
# `figures/` has disappeared from the listing even though the folder is still on disk — that is what
# `.gitignore` does. `interpretation.md` is still listed because it is the checkpoint task, and the
# working tree only reports clean after that fourth commit.
#
# **Why `figures/` does not belong in history.** The figure is *derived*: `analysis.py` plus the data
# regenerates it exactly. Recording it stores the same information twice, and the two copies can
# disagree. It is also binary, so Git cannot show what changed — every rerun appears as a large
# opaque modification, and the repository grows forever.
#
# The same reasoning, with much higher stakes, covers raw provider data, NetCDF files, environments,
# and anything containing a credential. The course rule follows from it: commit the code and the
# provenance record that let someone *reacquire* the data, never the data itself.
#
# **Two commits rather than one** because they are two different changes with two different reasons.
# If the ignore rule turns out to be wrong, it can be inspected and reversed without touching the
# analysis.

# %% [markdown]
# ### Ranking the commit messages
#
# ```text
# e. Add temperature summary script; uses Agg backend so it runs headless on the lab machines
# d. Add the temperature summary and figure script
# b. changed analysis.py
# c. Fixed stuff after the meeting
# a. update
# ```
#
# (e) and (d) both finish the sentence "If applied, this commit will…". (e) additionally records a
# *reason* that the code cannot express on its own — a future reader who sees `matplotlib.use("Agg")`
# and wonders whether it is still needed has their answer.
#
# (b) restates what Git already knows: the filename is in the diff. (c) sounds informative and is
# not — which meeting, which fix? (a) is the most common message in the world and the least useful.
#
# The test: could you use this message to find this change six months from now, without reading the
# diff?

# %% [markdown]
# ## Inspect the result

# %%
from pathlib import Path
import subprocess

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name in {"notebooks", "reference"}:
    PROJECT_ROOT = PROJECT_ROOT.parent
GIT_PRACTICE = PROJECT_ROOT / "data" / "processed" / "git_practice"


def git_output(*args):
    """Return stdout for a read-only Git command in the practice repository."""
    if not (GIT_PRACTICE / ".git").exists():
        return "Practice repository is not initialized yet. Follow the commands above."
    completed = subprocess.run(
        ["git", *args], cwd=GIT_PRACTICE, text=True, capture_output=True,
    )
    if completed.returncode != 0:
        return f"Git reported a problem: {completed.stderr.strip()}"
    return completed.stdout.strip() or "(no output)"


print("Status:\n", git_output("status", "--short"))
print("\nHistory:\n", git_output("log", "--oneline", "--decorate", "--max-count=6"))

# %% [markdown]
# ## What each command establishes — and what it does not
#
# | Command | Establishes | Does not establish |
# |---|---|---|
# | `git status` | which files are untracked, modified, or staged | that anything is correct |
# | `git diff` | changes in the working tree not yet staged | changes already staged |
# | `git diff --cached` | exactly what the next commit will contain | that the code runs |
# | `git commit` | a snapshot in **local** history | that anything was uploaded |
# | `git log` | the sequence of recorded decisions | that they were good decisions |
# | clean `git status` | working tree matches the last commit | correctness, backup, or review |
#
# The right-hand column is the one to memorize. Almost every Git misunderstanding is a claim from
# the left column being read as a claim from the right.

# %% [markdown]
# ## Common problems and fixes
#
# **"Git says `not a git repository`."** You are outside the practice folder. Run `pwd`. Do not run
# `git init` to make the message go away — that creates a second repository somewhere you did not
# intend, which is a much worse problem than the one you started with.
#
# **"My terminal filled with text and won't take commands."** You ran `git commit` without `-m` and
# Git opened an editor. Vim (`~` down the left margin): press `Esc`, type `:q!`, press Enter. Nano
# (`^X Exit` at the bottom): press `Ctrl-X`. Then redo the commit with `-m "your message"`.
#
# **"Please tell me who you are."** Set an identity for this repository only:
# `git config user.name "..."` and `git config user.email "..."`. Omit `--global` unless you mean to
# set it for every project on the machine.
#
# **"I staged the wrong file."** `git restore --staged wrongfile.md` unstages it and keeps your
# edits. Nothing is lost. Note that `git restore wrongfile.md` — without `--staged` — is different
# and *does* discard your edits.
#
# **"My last commit message is wrong."** `git commit --amend -m "Better message"`, but only if you
# have not shared the commit yet. Amending replaces a commit; doing that to something a collaborator
# already has creates two versions of the same history.
#
# **"`git status` lists hundreds of files."** You are probably in the wrong directory or missing a
# `.gitignore`. Stop and look before staging anything. `git add .` at this moment is how a 40 MB
# archive or a `.env` file enters a repository permanently.
#
# **"I committed something secret."** Removing it in the next commit is not enough — the old commit
# still contains it, and if it reached a shared remote, assume it is compromised. Rotate the
# credential first, then ask for help cleaning the history.

# %% [markdown]
# ## Go further reference
#
# **Branches.** `git switch -c improve-readme` creates a label and moves you onto it. Commits made
# there do not appear on `main` until merged. `git log --oneline --all --graph` draws both lines.
#
# **Pull requests** are a GitHub feature, not a Git command: a proposal that one branch be reviewed
# and merged. The course loop is issue → one active lesson owner → short branch → commits → draft
# pull request → co-instructor review → automated checks → merge into protected `main` → Pages
# publishes.
#
# **Notebooks.** `.ipynb` is JSON holding code, outputs, and execution counters, so it produces
# conflicts that are hard to read and diffs that change even when the code did not. This course
# pairs each notebook with a Jupytext `.py` file: students open the notebook, reviewers read the
# `.py`, one person edits a given notebook at a time, and `jupytext --sync` keeps the pair
# consistent. A clean text diff still does not prove the notebook runs — restart and run it.
#
# **The scenario answers.** All five are *stop and inspect*. Four hundred changed files means you
# are in the wrong place. A committed key needs rotation, not deletion. Conflict markers need
# reading, not a coin flip. "Just force-push" is the one instruction to decline until you understand
# what it would overwrite. And a 40 MB archive belongs in `.gitignore` with its provenance recorded
# in the manifest.

# %% [markdown]
# ## Exit ticket answers
#
# - **`git add`** selects changes to include in the next snapshot; it changes nothing on disk and
#   records nothing in history.
# - **`git commit`** writes the staged snapshot into local history with a message and an author.
# - **`git push`** would copy local commits to a remote such as GitHub. Until then, the work exists
#   on one machine.
# - **Inspecting `git diff --cached`** is how you confirm the commit contains what you intend and
#   nothing else — no debugging print, no data file, no unrelated edit.
