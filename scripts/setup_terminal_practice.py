"""Create a safe, disposable folder for Tuesday's terminal scavenger hunt.

The script never overwrites an existing file. Run it again to report which files already exist.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRACTICE_ROOT = PROJECT_ROOT / "data" / "processed" / "terminal_practice"

FILES = {
    "README.txt": """Terminal practice folder

Everything here is generated course material. Practice navigation and copying here—not in data/raw.
""",
    "observations/pier_preview.csv": """date,surface_temperature_c,bottom_temperature_c
2026-01-01,16.1,15.8
2026-01-02,16.3,15.9
2026-01-03,,16.0
2026-01-04,16.5,16.1
""",
    "notes/questions.txt": """Which folder am I in?
Which file contains observations?
What is the first line of the CSV?
Where should generated results go?
""",
    "config/variables.txt": """surface_temperature_c
bottom_temperature_c
date
""",
}


def main() -> None:
    PRACTICE_ROOT.mkdir(parents=True, exist_ok=True)
    created = []
    preserved = []

    for relative_name, content in FILES.items():
        destination = PRACTICE_ROOT / relative_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            preserved.append(relative_name)
            continue
        destination.write_text(content, encoding="utf-8")
        created.append(relative_name)

    print(f"Practice root: {PRACTICE_ROOT}")
    print(f"Created {len(created)} file(s):", *created, sep="\n - ")
    print(f"Preserved {len(preserved)} existing file(s):", *preserved, sep="\n - ")
    print("Open the VS Code integrated terminal and follow notebook 03.")


if __name__ == "__main__":
    main()
