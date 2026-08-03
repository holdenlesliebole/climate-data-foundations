# Publishing plan: course website plus executable notebooks

## Recommendation

Use one GitHub repository with two student entry points:

1. **Jupyter Book on GitHub Pages** for fast, durable reading of schedules, notes, cheatsheets,
   guided notebooks, and completed references.
2. **GitHub Codespaces with JupyterLab/VS Code** for actually running and editing the notebooks in a
   controlled Python environment.

GitHub Pages is static hosting; it should not be presented as if it runs Python. Jupyter Book can
render notebooks and provide launch buttons, while Codespaces supplies the live kernel. This keeps
the public course site readable even when a compute service is unavailable.

Primary documentation:

- [Jupyter Book: publish to GitHub Pages](https://jupyterbook.org/stable/get-started/publish/)
- [Jupyter Book: execution and launch buttons](https://jupyterbook.org/stable/execution/)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Developing in a GitHub Codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace)
- [Using JupyterLab in Codespaces](https://docs.github.com/codespaces/developing-in-a-codespace/getting-started-with-github-codespaces-for-machine-learning)

## Student experience

The repository landing page and course website should offer three equally visible routes:

- **Read online:** open the rendered lesson or completed reference on GitHub Pages.
- **Run in browser:** open the repository in Codespaces, where the course environment and extensions
  are already configured.
- **Work locally:** clone/download the repository, create `environment.yml`, and select the course
  kernel in VS Code or JupyterLab.

Every lesson page should include:

- session purpose and minimum viable takeaway;
- guided notebook link;
- completed reference link released after class;
- concise concept notes/cheatsheet;
- “Open in Codespaces” button once configured;
- data acquisition/provenance instructions;
- extension lane clearly separated from the core.

## Repository additions at publishing time

```text
Climate_science_bootcamp/
├── .devcontainer/
│   └── devcontainer.json       # Codespaces environment and VS Code extensions
├── .github/workflows/
│   ├── qa.yml                  # notebook/build checks
│   └── deploy.yml              # Jupyter Book → GitHub Pages
├── myst.yml                    # Jupyter Book site configuration/navigation
├── environment.yml             # student scientific environment
├── requirements-docs.txt       # Jupyter Book build dependencies only
├── CITATION.cff
├── LICENSE
└── ... current course files
```

Keep documentation-build dependencies separate from the student scientific environment. Students
do not need Jupyter Book to run an analysis notebook.

## What the site build should and should not execute

- Execute and cache small, deterministic, data-free reference notebooks such as Python/NumPy.
- Render guided notebooks without replacing student prompts.
- Do not make a Pages deployment depend on a live Pier/MOP/ERA5 service.
- For data-dependent completed references, either commit already-executed notebook outputs after
  attribution/licensing review, or build from an authorized fixed teaching input. Do not silently
  download a rolling source during every deployment.
- Never publish credentials, student submissions, restricted/unpublished data, machine-specific
  paths, or instructor-only solutions before their release time.

## Codespaces design

The dev container should:

- use the same supported Python version and scientific packages as `environment.yml`;
- install the Python, Jupyter, GitHub Copilot, and GitHub Copilot Chat VS Code extensions;
- open `README.md` and `notebooks/00_setup_check.ipynb` on first launch;
- preserve `data/raw/` as a student workspace but not populate it with provider data;
- let students perform the same Pier and MOP acquisition steps as local users;
- avoid storing tokens in repository files;
- use the smallest adequate machine type and document how to stop/delete a Codespace.

Confirm institutional ownership/billing, quotas, and prebuild availability before making Codespaces
the only executable route. Students already receiving GitHub Copilot makes it a natural primary
browser route, but the local environment remains a full alternative.

Jupyter Book can also expose Binder or JupyterHub launch buttons. Binder is a useful optional public
fallback, not the sole classroom plan: cold starts and capacity are outside the course's control.

## Automated QA before deployment

On pull requests and pushes to the default branch:

1. Validate every `.ipynb` as JSON and compile its Python cells.
2. Build a clean supported environment or container.
3. Execute the setup notebook, guided Python notebook, and data-free completed references.
4. Execute fixed-data references when an authorized test fixture is available.
5. Build Jupyter Book with warnings treated as failures where practical.
6. Check internal links and ensure raw/recovery/student files are absent from the artifact.
7. Deploy Pages only from the protected default branch after QA passes.

Run live provider acquisition as a scheduled/manual preflight near the course date rather than on
every pull request. Record coverage, schema, flags, size, and checksum changes.

## GitHub Pages deployment sequence

After the full notebook set is stable:

1. Use the public `holdenlesliebole/climate-data-foundations` repository as the dedicated course
   source and GitHub Pages origin.
2. Add source attribution, `CITATION.cff`, and release policy.
3. Create the Jupyter Book navigation/configuration and render locally.
4. Add the generated/custom GitHub Actions deployment workflow.
5. In repository **Settings → Pages**, select **GitHub Actions** as the publishing source.
6. Push to a test branch, inspect the artifact/site on desktop and mobile, then merge.
7. Add the Pages URL and Codespaces launch button to `README.md`.
8. Tag the tested course release used in class, for example `2026-bootcamp-v1`.

## Student work and submissions

Keep the published course repository clean. Before class, choose one submission pattern:

- individual GitHub Classroom repositories created from the course starter;
- individual forks, if repository visibility and permissions make that appropriate;
- a learning-management-system upload of the final notebook plus commit identifier.

Do not ask novices to submit work directly to the shared upstream course repository. The Git lesson
can still use a disposable practice repository or small shared documentation exercise.

## Decisions required before classroom release

- License for original course materials and attribution for adapted materials.
- Pier recovery redistribution decision and treatment of executed data-derived outputs.
- Institutional Codespaces billing/quota/prebuild policy.
- Whether GitHub Classroom, forks, or LMS upload handles assignments.
- Domain name/branding, accessibility review, and who maintains the next year's release.
