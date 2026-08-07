"""Create a new disposable folder for Wednesday's local Git exercise.

This script deliberately does not run ``git init``; initializing and inspecting the repository are
student tasks. It refuses to overwrite an existing practice folder.
"""

import argparse
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"

FILES = {
    "README.md": """# Tiny climate analysis

This disposable project practices meaningful Git snapshots. It is deliberately small so that every
change is easy to read in a diff.

Question: how does a short run of example surface temperatures change through time?

Run it with:

    python analysis.py

The script writes a figure into `figures/`.
""",
    "analysis.py": '''"""Summarize and plot a few example surface temperatures."""

import matplotlib

matplotlib.use("Agg")  # write a file instead of opening a window

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def plot_temperature(day, temperature_c, title):
    """Plot one labeled temperature series and save it under figures/."""
    figures = Path(__file__).parent / "figures"
    figures.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(day, temperature_c, marker="o", label="Surface")
    ax.set(title=title, xlabel="Day in example", ylabel="Temperature (°C)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()

    destination = figures / "temperature.png"
    fig.savefig(destination, dpi=150)
    return destination


day = np.arange(1, 5)
temperature_c = np.array([15.8, 16.0, 16.4, 16.3])

print("mean temperature (C):", np.mean(temperature_c))
print("figure written to:", plot_temperature(day, temperature_c, "Example surface temperature"))
''',
    "interpretation.md": """# Interpretation

TODO: run the analysis, look at the figure, then write one bounded sentence about the four values.
Say what they show and say that they are invented example values, not observations.
""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name",
        default="git_practice",
        help="New folder name under data/processed (letters, numbers, underscore, hyphen).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.name):
        raise ValueError("--name may contain only letters, numbers, underscore, and hyphen.")

    practice_root = PROCESSED / args.name
    if practice_root.exists():
        raise FileExistsError(
            f"{practice_root} already exists. Preserve it and choose a new --name, "
            "for example --name git_practice_2."
        )

    practice_root.mkdir(parents=True)
    for relative_name, content in FILES.items():
        (practice_root / relative_name).write_text(content, encoding="utf-8")

    print(f"Created: {practice_root}")
    print("Next commands:")
    print(f"  cd {practice_root.relative_to(PROJECT_ROOT)}")
    print("  pwd")
    print("  git init -b main")
    print("  git status")


if __name__ == "__main__":
    main()
