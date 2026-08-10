# Three-instructor collaboration setup

## Repository

The dedicated repository is
[`holdenlesliebole/climate-data-foundations`](https://github.com/holdenlesliebole/climate-data-foundations),
separate from `holdenlesliebole/teaching-notes`. This keeps course collaborators, Pages, issues,
releases, and permissions from affecting unrelated teaching materials.

The local course root has its own Git history. Always run course Git commands from this directory,
not from the surrounding `Teaching` checkout, and never stage this directory in the parent
`teaching-notes` repository.

A personal GitHub repository can invite the two co-instructors as collaborators through repository
settings. If Scripps/UCSD offers an organization, an organization-owned repository is preferable for
continuity, team roles, and handoff. See GitHub's guides to
[inviting collaborators](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository)
and [managing repository access](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository).

## Recommended settings

1. Give all three instructors write access; retain admin access with the course owner and ideally one
   continuity backup.
2. Protect `main` with a ruleset or branch-protection rule:
   - require a pull request;
   - require one approving review;
   - dismiss stale approvals or require approval of the latest push;
   - require conversation resolution;
   - require notebook/site QA when it exists;
   - block force pushes and deletion.
   Until both co-instructors have accepted repository invitations, require pull requests and checks
   but keep the approving-review count at zero; otherwise the sole current collaborator can be
   unable to merge. Raise it to one as soon as another instructor has write access.
3. Enable Issues, Discussions if desired, Actions, and Pages only after the repository is ready.
4. Add a `.github/CODEOWNERS` file after all three GitHub usernames are known. GitHub can
   automatically request owners for changed paths and can require their approval. See
   [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
   and [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Suggested future `CODEOWNERS` shape:

```text
# Replace placeholders with actual GitHub usernames or an organization team.
*                                  @course-lead @co-instructor
/notebooks/07_*                    @mark-username @course-lead
/notebooks/08_*                    @mark-username @course-lead
/notebooks/09_*                    @mark-username @course-lead
/reference/07_*                    @mark-username @course-lead
/reference/08_*                    @mark-username @course-lead
/reference/09_*                    @mark-username @course-lead
/.github/                          @course-lead
/environment.yml                  @course-lead @co-instructor
```

Do not add this file with fake handles: CODEOWNERS must reference people/teams with repository write
access.

## Weekly authoring rhythm

### Fifteen-minute planning meeting

- Move issues into `ready`, `in progress`, `review`, or `done`.
- Assign exactly one active owner and at least one reviewer per notebook.
- Confirm the minimum viable takeaway, core checkpoint, and first cut.
- Name dependencies: data, environment, Mark's notation, or another notebook.

### Authoring

- Owner creates a branch and draft PR.
- Reviewer comments on scope/logic before the owner polishes outputs.
- Owner runs the notebook and updates instructor notes/reference in the same PR.
- A second instructor can test as a novice proxy without editing the active notebook.

### Review meeting or asynchronous review

- Reviewer starts with student outcome/timing, then checks code/statistics.
- Review GitHub's rendered `.ipynb` diff for cell content and appearance.
- Use `nbdiff-web` when outputs or cell structure matter.
- Record unresolved decisions in the issue, not in private chat alone.

### Merge/release

- Merge after approval and QA.
- Pages deploys reviewed `main`; no one edits generated Pages output by hand.
- Tag classroom releases. Urgent in-class fixes receive a small PR and a new patch tag.

## Notebook conflict prevention

[nbdime](https://nbdime.readthedocs.io/en/stable/) provides notebook-aware diff and merge views for
`.ipynb` files. It helps, but it does not make simultaneous editing of the same instructional
narrative a good idea.

Use these rules:

- one active author per notebook;
- restart, run, and save before handing off notebook ownership;
- one notebook or tightly coupled pair per PR when possible;
- never resolve a notebook conflict by choosing “ours” or “theirs” without reviewing cell content;
- preserve reference and guided notebook alignment in the same change;
- keep generated outputs out of guided-notebook diffs.

## Suggested division of responsibility

The exact names should be agreed by the three instructors:

- **Course/release owner:** repository settings, environment, schedule, final release, Pages.
- **Tools/data owner:** Monday/Tuesday acquisition, terminal, VS Code, Copilot, data services.
- **Statistics owner (Mark):** Thursday/Friday theory notation, assumptions, worked examples.

Every area still has a different reviewer. Ownership means first responsibility, not sole authority.
Wednesday reliability/Git and the final-assignment integration should receive cross-review because
they connect all three areas.

## Public versus private authoring

- A private authoring repository makes timed solution release and unfinished material easier, but
  private GitHub Pages depends on account/organization plan.
- A public repository makes Pages and student access simple. Do not rely on obscurity to hide
  solutions; publish/release student and reference materials deliberately.
- A two-repository public/private mirror is possible but creates synchronization overhead. Prefer one
  repository unless the solution-release policy truly requires separation.

The repository and student site are public. Pull requests remain the authoring boundary: Pages
deploys only reviewed `main`, while lesson branches can be checked without changing the live site.
Decide the course-material license, completed-reference release timing, Codespaces billing, and
student submission workflow before the classroom release.
