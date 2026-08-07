# Student setup guide

Complete this before Monday if possible. The setup clinic is for help, not a test of prior
experience. There are certain open source software that are necessary tools for developing in Python, conducting data analysis, and collaborating with others. It may seem overwhelming, but this is something you only have to do once - and then you can teach others to do it. For this data analysis course, we expect that you have the following installed on your local machine:

- Python/Conda
- VSCode

Note: Installation can be notoriously finicky. LLM’s are very good at solving installation issues and are recommended if any are encountered. Be descriptive about your issues and copy/paste the error codes from your terminal to ChatGPT/Gemini/Claude etc…


## A. Installing Python/Conda

1. Download the miniforge version for your machine from [this website](https://conda-forge.org/download/)

2. Open your terminal, type `cd ~/Downloads`, and Enter

3. Type `./Miniforge3-`, hit Tab (this should autocomplete the name of the downloaded file. If it doesn't, copy and paste the file name): 

  - For example, my downloaded filename is: Miniforge3-MacOSX-arm64.sh

  - Hit `Enter` to run the script 

  - If this command fails with a "permission denied" error, type `chmod +x Miniforge3-<filename>`, hit Enter, and try to run the script again.

4. Follow the text prompts in the terminal:
- Press space to move/scroll through the text
- Type `yes` and Enter to approve the license
- Hit Enter to approve the default location for installation 
- It will ask you whether you want conda to be automatically configured in the terminal. Type `yes` and Enter to add Miniforge to your `PATH`

5. Restart your terminal and type `conda --version` to confirm that conda is installed. You should see a version number printed in the terminal. Check that Python is also available by typing `python --version` in the terminal. You should see a version number printed in the terminal.

## B. Installing VSCode

1. Download the latest version of VSCode for your machine from [this website](https://code.visualstudio.com/Download)

2. Once you have the software installed, open VSCode and install the following extensions:
- Python (by Microsoft)
- Jupyter (by Microsoft)


## C. Gather the workshop materials

1. Navigate to the course Github repository at[https://github.com/holdenlesliebole/climate-data-foundations]

2. Click the green "Code" button and click 'Download ZIP'

3. Unzip the downloaded file and move it to a location of your choice (e.g., Desktop, Documents, etc.)

4. Open the entire folder in VS Code
- File → Open Folder

5. Open a terminal in VSCode (Terminal → New Terminal) and type `conda env create -f environment.yml` to create the conda environment for this course. This may take a few minutes to complete.

6. Activate the environment by typing `conda activate climate-data-foundations` in the terminal. You should see the name of the environment in parentheses at the beginning of the terminal prompt.
