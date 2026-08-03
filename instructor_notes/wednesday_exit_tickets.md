# Wednesday exit tickets and interpretation guide

Use these as completion checks, not high-stakes grading. Accept plain language when the distinction
is correct. Follow up on patterns across the class rather than polishing every response.

## Session 1: reliable analysis

### Prompt

Name one assumption protected by today's loader, assertion, or unit test. What important scientific
claim does that check **not** establish?

### Strong-response ingredients

- names a concrete assumption, such as required columns, parseable timestamps, one sensor/depth,
  expected units, valid known-value arithmetic, or explicit quality-flag filtering;
- connects the check to a failure it could catch;
- states a limit, such as calibration accuracy, representativeness, independence, causation, or
  correctness of every record.

### Follow-up cue

If a student writes only “the tests pass,” ask: “What specific wrong input would make one fail, and
what scientific problem could still remain?”

## Session 2: Git

### Prompt

Explain the difference between `git add`, `git commit`, and a GitHub pull request. Name one check you
would perform before asking a collaborator to merge your work.

### Strong-response ingredients

- `git add` selects changes for the next snapshot;
- `git commit` records that snapshot in local history;
- a pull request proposes that a branch be reviewed and merged in the shared GitHub repository;
- check examples: inspect the staged diff, run from a fresh kernel, run tests, review paths/data
  policy, read the rendered notebook, or ask a novice proxy to follow the instructions.

### Common misconceptions to address Thursday

- “Commit uploads the file.” A commit is local until pushed.
- “Push merges it.” Pushing shares a branch; review/merge is separate.
- “Clean status means correct.” It means recorded files match the latest commit.
- “Git saves the data source.” Provider data and provenance still follow the course data contract.
- “A readable `.py` diff means the notebook runs.” Execution QA is still required.

## Optional confidence pulse

Students mark one item privately: green / yellow / red for (1) reading a traceback, (2) running a
test, (3) making a focused commit, and (4) explaining a pull request. Use this to form Thursday pairs
and target office-hour support.
