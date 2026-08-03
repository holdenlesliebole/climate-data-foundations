# Student setup guide

Complete this before Monday if possible. The setup clinic is for help, not a test of prior
experience.

## 1. Get the course project

Until the GitHub repository is published, download or copy the entire
`Climate_science_bootcamp` folder. Keep the folder somewhere you can edit, such as Documents—not in
a protected system or application directory.

Once the repository is published, use either:

- **local route:** clone the repository and use the environment below;
- **Codespaces route:** open the repository's Codespace in a browser; its environment will be
  prepared from the same course specification.

## 2. Create the Python environment

Install a Conda-compatible environment manager if you do not already have one. From a terminal in
the course project:

```bash
conda env create --file environment.yml
conda activate climate-data-foundations
python -m ipykernel install --user --name climate-data-foundations --display-name "Climate Data Foundations"
```

If the environment already exists and the course file changed:

```bash
conda env update --name climate-data-foundations --file environment.yml --prune
```

Do not install the same packages repeatedly into unrelated environments. If a command fails, save
the first error and bring it to the setup clinic.

## 3. Prepare VS Code

Install current versions of:

- Visual Studio Code;
- the Microsoft Python extension;
- the Microsoft Jupyter extension;
- Git;
- GitHub Copilot and GitHub Copilot Chat, using the student entitlement provided for the course.

Open the whole course folder in VS Code. In `notebooks/00_setup_check.ipynb`, select the kernel named
**Climate Data Foundations**.

## 4. Run the setup check

Open `notebooks/00_setup_check.ipynb`, choose **Restart Kernel and Run All**, and confirm that every
automated check says `PASS`. The notebook should create only:

```text
data/processed/setup_check/setup_example.csv
data/processed/setup_check/setup_example.nc
```

These are generated test files and may be replaced. The setup notebook does not use the network.

## 5. If something fails

Send or bring:

- your operating system;
- the first traceback, not only the final cascade of errors;
- the Python executable printed by the notebook;
- the working directory printed by the notebook;
- the checks that passed before the failure.

Never send a password, access token, or other credential. Do not paste credentials or unpublished or
restricted data into GitHub Copilot or another external AI service.

## Setup is complete when

- [ ] the course folder opens as a project;
- [ ] the selected kernel is **Climate Data Foundations**;
- [ ] the plot appears;
- [ ] CSV and NetCDF round trips pass;
- [ ] GitHub Copilot is signed in, or an instructor knows that access is still pending;
- [ ] you know where to find the setup clinic or course help channel.
