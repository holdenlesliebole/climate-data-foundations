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

This disposable project practices meaningful Git snapshots.

Question: How do four example surface temperatures change through time?
""",
    "analysis.py": """import numpy as np

temperature_c = np.array([15.8, 16.0, 16.4, 16.3])
print("mean temperature (C):", np.mean(temperature_c))
""",
    "interpretation.md": """# Interpretation

TODO: Run the analysis, then write one bounded sentence about the four values.
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
    print("  git init")
    print("  git status")


if __name__ == "__main__":
    main()
