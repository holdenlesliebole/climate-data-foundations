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

A message should finish the sentence "If applied, this commit will…", and should add *why* whenever
the why is not visible in the diff. The test: could you use this message to find this change six
months from now without reading the code?

## Starting a repository

```bash
cd path/to/the/project     # then run pwd and read it aloud
git init -b main
git status
```

Two details that save time later:

- `-b main` names the first branch. Without it, Git prints a multi-line hint and may create
  `master`, which then disagrees with the `main` branch used everywhere else in this course. Setting
  `git config --global init.defaultBranch main` once has the same effect permanently.
- Write `.gitignore` **before** the first commit. Generated figures, `__pycache__/`, `.ipynb`
  checkpoints, environments, and every raw data file belong in it. Anything that reaches history is
  much harder to remove than to exclude.

Commit the code and the provenance record that let someone *reacquire* the data. Never the data.

## Undoing things, safely

| Situation | Command | Loses work? |
|---|---|---|
| Staged the wrong file | `git restore --staged FILE` | no |
| Want to discard edits since the last commit | `git restore FILE` | **yes** |
| Last commit message is wrong (not yet shared) | `git commit --amend -m "Better message"` | no |
| Want to read the last commit in full | `git show HEAD` | no |
| Want the full history of one file | `git log -p FILE` | no |

Not on this list, deliberately: `git reset --hard`, `git push --force`, and anything that rewrites
published history. Almost nothing in Git is irreversible *except* those. When you think you need
one, stop and ask.

## Common problems and fixes

**"fatal: not a git repository."** You are outside the project folder. Run `pwd`. Do not run
`git init` to make the message go away — that creates a second repository where you did not intend
one, which is a worse problem than the one you started with.

**The terminal fills with text and stops accepting commands.** You ran `git commit` without `-m`, so
Git opened an editor. Vim (`~` down the left margin): press `Esc`, type `:q!`, press Enter. Nano
(`^X Exit` along the bottom): press `Ctrl-X`. Then repeat the commit with `-m "your message"`.

**"Please tell me who you are."** Set an identity for this repository only — `git config user.name`
and `git config user.email`, without `--global` unless you mean every project on the machine. Never
use someone else's identity; commit authorship records who did the work.

**`git status` lists hundreds of files.** You are in the wrong directory or missing a `.gitignore`.
Stop and look before staging. Running `git add .` at this moment is exactly how a 40 MB archive or a
credentials file enters a repository permanently.

**You committed a secret.** Removing it in the next commit is not enough; the old commit still
contains it. If it reached a shared remote, assume it is compromised: rotate the credential first,
then ask for help cleaning history.

**A notebook conflict with `<<<<<<<` markers.** Do not pick a side at random. Stop, find out who the
active editor is, inspect both notebook versions with `nbdiff`, reconcile the cells deliberately,
and rerun the notebook.

## Notebook diffs

Raw `.ipynb` files are JSON and can create noisy conflicts. The notebook itself is the canonical
course file. GitHub renders notebook changes, and `nbdiff` provides a notebook-aware local
comparison:

```bash
nbdiff main...HEAD -- notebooks/03_tools_llms.ipynb
```

Do not resolve a notebook conflict by accepting one entire side unless you have verified that no
lesson content was lost. Ask the active owner to reconcile the cells and rerun the notebook.

## Recovery questions

- **Wrong branch?** Stop editing, run `git status`, and ask before moving changes if the correct
  destination is unclear.
- **Commit failed for identity?** Configure your own name and email; authentication is separate.
- **Push rejected?** Fetch/pull and inspect the remote changes. Do not force-push shared history.
- **Data file is huge?** Do not add it. Check `data/README.md` and the manifest/recovery policy.
- **Secret or restricted data staged?** Do not commit or push. Tell the course lead immediately.

Avoid history rewriting, force pushes, recursive deletion, and broad commands until you understand
the target and consequence. A collaborator—or Copilot—can suggest a command but cannot authorize it.
