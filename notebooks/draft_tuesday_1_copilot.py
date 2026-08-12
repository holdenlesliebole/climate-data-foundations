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
# # Copilot as a study partner
#
# **DRAFT — not yet promoted to the course sequence.**
#
# Today we use Copilot to understand code, not to avoid understanding it. A line stays in your notebook only if you can say what it does in your own words.
#
# | Minutes | Activity |
# |---|---|
# | 0–10 | How Copilot talks to you |
# | 10–28 | Explain a line you did not write |
# | 28–43 | A traceback is a question |
# | 43–48 | Break |
# | 48–62 | Syntax on demand |
# | 62–76 | Comment-first completion |
# | 76–85 | What Copilot cannot know; exit ticket |

# %% [markdown]
# ## Preflight
#
# This notebook reads no files and uses no network. Run this cell; it names the fix if anything is missing.

# %%
import sys

print("Python:", sys.version.split()[0])
print("Interpreter:", sys.executable)

missing = []
for package in ["numpy", "pandas"]:
    try:
        __import__(package)
    except ImportError:
        missing.append(package)

if missing:
    print("\nMISSING:", ", ".join(missing))
    print("Fix: activate the course environment, then re-select the kernel.")
    print("  conda activate climate-data-foundations")
    print("If the environment does not exist yet, from the project folder:")
    print("  conda env create -f environment.yml")
else:
    print("\nPASS — numpy and pandas are available.")

if "climate-data-foundations" not in sys.executable:
    print(
        "\nNOTE: this kernel does not look like the course environment. That is usually fine,"
        "\nbut if a later cell fails on an import, use the kernel picker (top right) and choose"
        "\nthe interpreter whose path contains 'climate-data-foundations'."
    )

# %% [markdown]
# ### Is Copilot ready?
#
# 1. Copilot icon in the VS Code status bar is present and not crossed out.
# 2. Type `# add two numbers` in a code cell and press `Enter` — grey ghost text should appear.
# 3. The Copilot chat panel opens from the sidebar.
#
# If not: install the **GitHub Copilot** and **GitHub Copilot Chat** extensions → sign in to GitHub in VS Code → check your student entitlement. Entitlement problems need an instructor, not a code fix.
#
# **If Copilot will not work today**, you are not skipping the session:
#
# - pair with someone who has it and you drive the keyboard;
# - Activity 2 works from the traceback and the docs alone;
# - Activity 3 works from `pandas.pydata.org/docs` and `help(pd.DataFrame.groupby)`.
#
# Only Activities 4 and 5 need it live.

# %%
import numpy as np
import pandas as pd

# Shaped like Monday's Pier table: six days from each of three months, two surface values missing.
practice = pd.DataFrame(
    {
        "date": pd.to_datetime(
            [
                "2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08", "2026-01-09", "2026-01-10",
                "2026-02-05", "2026-02-06", "2026-02-07", "2026-02-08", "2026-02-09", "2026-02-10",
                "2026-03-05", "2026-03-06", "2026-03-07", "2026-03-08", "2026-03-09", "2026-03-10",
            ]
        ),
        "surface_temperature_c": [
            16.1, 16.3, np.nan, 16.5, 16.9, 17.2,
            15.8, 15.6, 15.9, np.nan, 16.2, 16.4,
            16.7, 17.1, 17.0, 16.8, 17.3, 17.5,
        ],
        "bottom_temperature_c": [
            15.8, 15.9, 16.0, 16.1, 16.2, 16.4,
            15.2, 15.1, 15.3, 15.4, 15.6, 15.7,
            16.0, 16.2, 16.1, 16.0, 16.3, 16.5,
        ],
    }
)
practice

# %% [markdown]
# ## 1. Three ways Copilot talks to you
#
# | Surface | How to open it | Best for |
# |---|---|---|
# | **Inline suggestion** (grey ghost text) | start typing in a cell | finishing a line you began |
# | **Inline chat** | `Cmd+I` / `Ctrl+I` | changing the selected lines in place |
# | **Chat panel** | Copilot icon in the sidebar | explaining, decoding errors |
#
# Ghost text: `Tab` accepts, `Esc` dismisses, `Alt+]` shows the next alternative.
#
# > **The one rule:** a line stays in your notebook only if you can say out loud what it does, without reading the code.

# %% [markdown]
# ## 2. Explain a line you did not write
#
# For each line: **write your guess first**, then select the line and ask Chat `/explain`, then record one thing the explanation added or corrected. Guessing first turns the answer into feedback instead of text you skim.

# %%
# Line A
practice["surface_temperature_c"].isna().sum()

# %% [markdown]
# - **My guess:** TODO
# - **Added or corrected:** TODO

# %%
# Line B
practice.loc[practice["surface_temperature_c"] > 16.5, "date"]

# %% [markdown]
# - **My guess:** TODO
# - **Added or corrected:** TODO

# %%
# Line C
practice["surface_temperature_c"].sub(practice["bottom_temperature_c"]).round(2)

# %% [markdown]
# - **My guess:** TODO
# - **Added or corrected:** TODO

# %%
# Line D — dense. Ask Copilot to break it into steps.
practice.assign(month=practice["date"].dt.month).groupby("month")["surface_temperature_c"].mean()

# %% [markdown]
# - **My guess:** TODO
# - **Added or corrected:** TODO
#
# Now ask: *"What happens to the missing values here, and where is that decision made?"* `groupby(...).mean()` skips them by default — a scientific decision made silently, by a default. Finding the default is what Copilot is good for; judging it is your job.
#
# **Where was that decision made, and who made it?** TODO

# %% [markdown]
# ## 3. A traceback is a question
#
# The **last line** of a traceback is the complaint. That line is what you paste into Chat.
#
# For each cell: predict the error type, run it, read the last line, ask Chat what it *means* before asking for a fix, then fix it yourself.

# %%
# Broken cell 1 — predict the error type first: TODO
practice["surface_temp_c"].mean()

# %% [markdown]
# - **Error type:** TODO
# - **In my words:** TODO
# - **Actual cause:** TODO

# %%
# Broken cell 2 — predict the error type first: TODO
mask = np.array([True, False, True])
practice.loc[mask, "surface_temperature_c"]

# %% [markdown]
# - **Error type:** TODO
# - **In my words:** TODO
# - **Actual cause:** TODO
#
# The error talks about lengths; you were thinking about rows. Translating between those two sentences is the skill.

# %%
# Broken cell 3 — predict the error type first: TODO
temperatures = ["16.1", "16.3", "16.5"]
sum(temperatures) / len(temperatures)

# %% [markdown]
# - **Error type:** TODO
# - **In my words:** TODO
# - **Actual cause:** TODO
#
# Worth asking Copilot: *"Why does Python not convert these strings to numbers for me?"* Silent conversion is how a column of `"NaN"` strings becomes a plausible number.

# %% [markdown]
# ## Break
#
# Five minutes. Switch driver and navigator.

# %% [markdown]
# ## 4. Syntax on demand
#
# You can describe the step in words but cannot spell it in pandas. That is a vocabulary gap, and closing it fast is a good use of the tool.
#
# Ask for one small named step. Read the answer, then **type it yourself rather than paste it**. Run it and look at the result.

# %%
# 4a. Select only the rows where the surface temperature is missing.


# %%
# 4b. Count how many days the surface was warmer than the bottom.


# %%
# 4c. Add a column called "surface_minus_bottom_c" holding the difference.


# %%
# 4d. Find the date of the warmest surface temperature in the table.


# %%
# 4e. Report the mean surface temperature two ways: once propagating missing values,
#     once skipping them. Print both, labeled.


# %% [markdown]
# Compare with your partner — you probably wrote different code, and both may be correct.
#
# - **Which version is easier to read in six months, and why?** TODO
# - **Did either make a missing-value decision silently?** TODO

# %% [markdown]
# ## 5. Comment-first completion
#
# Type the comment below, press `Enter`, wait for the grey suggestion. Before pressing `Tab`: read every line, predict what it returns, then accept, edit, or reject. Run it and check your prediction.

# %%
# Return the mean surface temperature for each month, skipping missing values,
# as a DataFrame with columns "month" and "mean_surface_c".


# %% [markdown]
# - **Did it match your prediction?** TODO
# - **Accepted, edited, or rejected — why?** TODO
# - **A line I could not explain, and what I did:** TODO
#
# Now delete your work and retry with a vague comment: `# summarize the temperatures`.
#
# - **What changed?** TODO
# - **What did the specific comment give the tool?** TODO
#
# That is all "prompting" means here: state the input, the output, and the decision you already made.

# %% [markdown]
# ## 6. What Copilot cannot know
#
# It has read a great deal of code. It has never seen your data. It does not know where your file came from, whether your temperatures are °C or K, what a missing value means in *your* record, or whether your question is answerable with the data you have.
#
# So after accepting anything, run **one check you chose in advance** — a known value, a shape, a range, a count.

# %%
# Choose one check for something you accepted today, and write it here.
# Example shape: assert practice["surface_minus_bottom_c"].notna().sum() == 16


# %% [markdown]
# **Privacy.** Never paste credentials, tokens, personal information, unpublished or restricted data, reviewer material, or private code into an external service. Follow the institution's AI and data policy.
#
# **Authority.** Pause before running generated commands that delete, change permissions, install, upload, request credentials, or target broad paths. A suggestion cannot authorize an action.
#
# **Attribution.** One sentence is enough: *"Used Copilot to explain `groupby` and look up `idxmax`."* The interpretation stays yours.

# %% [markdown]
# ## Exit ticket
#
# 1. **What do you understand better than at the start, and which activity did it?** TODO
# 2. **Name one question today that Copilot could not have answered, and why.** TODO

# %% [markdown]
# ## Continuation lane
#
# 1. Ask Copilot to rewrite your densest line as three simpler ones. Which would you put in a paper, and why?
# 2. Ask for the same explanation twice in two chats, worded differently. Settle any disagreement with the documentation, not a third prompt.
# 3. Write an under-specified comment where the missing-value decision matters. Record what the tool assumed, then write the comment that removes the ambiguity.
