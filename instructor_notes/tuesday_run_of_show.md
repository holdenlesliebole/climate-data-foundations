# Tuesday instructor run-of-show

Assumption: approximately 20 students, ten pairs, three instructors. Tuesday 1 uses a generated
practice folder; Tuesday 2 requires the public CDIP service and a preflighted local recovery file.

## Preflight

- Run `scripts/setup_terminal_practice.py` from a clean checkout on each supported OS.
- Confirm VS Code Python/Jupyter/Copilot extensions and student entitlement/sign-in.
- Prepare three setup-failure cards: wrong directory, wrong kernel, missing file.
- Confirm institutional policy for Copilot, privacy, unpublished data, and attribution.
- Recheck D0513 coverage; execute seven-day and January–July requests; record schema, size, flags,
  checksums, and exact recovery files.
- Verify every downstream MOP step from local files with network disabled.

## Session 1: terminal, VS Code, and verified Copilot use

**Minimum viable takeaway:** know the project/directory/interpreter/kernel, and require a visible
verification trail for generated code.

**Core checkpoint by minute 38:** each pair has navigated/copy-renamed inside the generated practice
folder and diagnosed one path/kernel symptom using evidence.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–5 | Retrieval: path versus Python error | Individual first-check prediction | Triage unresolved setup |
| 5–17 | Generate practice folder; model `pwd`, `ls`, `cd`, Tab completion | Run commands one line at a time, predicting first | Rover enforces bounded `processed/` folder |
| 17–30 | Introduce `head`, `mkdir`, `cp`, `mv`; map terminal to Explorer | Complete scavenger; switch driver/navigator | Verify result file, no destructive commands |
| 30–38 | Map project/directory/interpreter/kernel | Diagnose three failure cards before fixing | Observer reports dominant confusion |
| 38–42 | Break | Reset/switch roles | Resolve only blockers |
| 42–54 | Demonstrate verification loop with wrong Kelvin sign | Write known-value check; reject proposal | Ask who owns unit decision |
| 54–67 | Bounded Copilot plotting task | Prompt, inspect diff, normal/adversarial checks | Require every accepted line explained |
| 67–77 | Peer verification trail audit | Partner names caught/not-caught failure | Extension only after core trail |
| 77–80 | Exit ticket | Individual response | Collect tool-access/privacy issues privately |

### Recovery and cut order

- If terminal setup consumes more than three focused minutes, provide the generated practice folder
  and continue with navigation; do not skip the directory explanation.
- If Copilot access fails, pair with a signed-in student or use the printed candidate patch; the
  learning target is verification, not account troubleshooting.
- Cut cross-model comparison first, then shorten VS Code panel tour. Preserve path/kernel diagnosis,
  wrong-but-plausible code, and normal/adversarial checks.

### Safety language to say aloud

“Do not run a generated command until you can state its target and consequence. Stop for deletion,
permissions, installation, upload, credentials, broad paths, or Git history rewriting.”

## Session 2: reproducible remote MOP data

**Minimum viable takeaway:** choose a bounded remote subset, save the exact request and untouched
response, then analyze the local NetCDF with its metadata and flags.

**Core checkpoint by minute 53:** each pair has an exact URL/manifest entry and a seven-day local
NetCDF or documented recovery copy.

| Time | Lead | Students | Supports |
|---|---|---|---|
| 0–10 | Compare Pier manual archive with parameterized MOP request | Mark which choices belong in URL, filename, manifest | Check Monday paths/manifests |
| 10–23 | Read MOP/NCSS coverage and attributes | Choose/confirm site, dates, five variables, format | Check modeled-versus-observed language |
| 23–39 | Build repeated `var` parameters and encoded URL | Audit printed URL; predict 168 observations/KB scale | Catch dictionary/repeated-key errors |
| 39–43 | Break | Switch driver/navigator | Confirm destination names |
| 43–53 | Acquire once; model non-overwrite/recovery record | Download or copy recovery; record evidence | Three-minute network diagnostic |
| 53–66 | xarray structure/metadata/flag inspection | Answer six inspection questions | Ask for attrs, not memorized units |
| 66–76 | Plot `waveHs`; field note | Label UTC/units/source and limitation | Direction extension only after core |
| 76–80 | Exit ticket and assignment-file launch | State repeatability needs; start/queue longer request | Confirm every student knows follow-up |

### After-class required follow-up

Students acquire `D0513_2026-01-01_2026-07-31.nc` (or replacement months inside current coverage),
validate 5,088 expected hourly observations for the proposed dates, and add its own manifest entry.
Allow time Wednesday/Friday for anyone who needed recovery.

### Recovery and cut order

- Check network, current coverage, spelling, encoded URL, and response type one at a time. Then use
  the identical local recovery file and record `instructor_recovery`.
- Cut checksum calculation and direction extension first. Preserve exact URL, local file, xarray
  attrs/flags, labeled plot, and modeled-output limitation.

## Tuesday debrief

- Who lacked Copilot access and needs follow-up?
- Which safety boundary produced uncertainty?
- How many pairs downloaded versus used recovery, and why?
- Did every student acquire or schedule the assignment-sized MOP file?
- Which request/schema fact must be updated in the reference before release?
