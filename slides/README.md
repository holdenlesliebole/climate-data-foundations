# Slides

Projector decks for the afternoon sessions. Plain HTML, no build tooling beyond
Python, nothing fetched at view time.

## Wednesday — Getting unstuck

50 slides in six sections, meant to be broken up rather than shown end to end:

| Section | Slides | Runs before | Roughly |
|---|---|---|---|
| 1 · The terminal | 6 | notebook 05 | 5 min |
| 2 · Reading errors | 13 | notebook 05 | 12 min |
| 3 · Getting data yourself | 6 | notebook 04 | 8 min |
| 4 · Git & GitHub | 10 | the live `git clone` | 15 min |
| 5 · What gets built | 9 | after the clone | 12 min |
| 6 · Durable AI context | 5 | end of day | 8 min |

Jump buttons along the bottom move between sections, so the running order is
yours to change on the spot. Section 5 covers one project at a time (046 Lorenz,
then 047 Mandelbrot, then 045 CCS), so you can stop after any of them.

## Have these open before you start

Tabs and windows, left to right, so you are never hunting mid-session:

| Open | Needed by | Note |
|---|---|---|
| The deck | throughout | Full screen, second display if you have one |
| **Mac Terminal** | slides 3–7 | Open it *live* on slide 4 so they watch ⌘Space → "Terminal" |
| **VS Code, terminal panel showing** | slide 4 | Show it right after, so "same terminal" lands as a demo |
| `notebooks/05_reliable_code.ipynb` | slide 20 → | Kernel set, setup cell run |
| `reference/05_reliable_code_complete.ipynb` | slide 20 → | **Fully executed, all outputs stored.** Never needs running |
| `notebooks/04_remote_data.ipynb` | slide 26 → | Kernel set, first cell run |
| `reference/04_remote_data_complete.ipynb` | slide 26 → | **Has stored outputs** — the fallback if CDIP is slow |
| [MOP transect viewer](https://cdip.ucsd.edu/m/product_descriptions/models.html) | slide 23 | Show the form that builds the URL |
| [California swell viz](https://holdenlesliebole.github.io/california-swell/index.html) | slide 23 or 26 | "This is what the data becomes" |
| `course-reference/notebooks/046_lorenz.ipynb` | slide 40 → | First cell already run so plotly is installed |
| `course-reference/notebooks/047_mandelbrot.ipynb` | slide 43 → | Same |
| A terminal at `~/Desktop` | slides 31–33 | For the live clone |

Before the clone demo, remove any `~/Desktop/course-reference` from a rehearsal, or
`git clone` will refuse and you will be debugging in front of everyone.

### Which folder, and which version

Students work in **their own folder from Monday** for notebooks 04 and 05. Not a fresh
copy: `data/raw/**` is gitignored, so a clone contains none of the Pier or MOP files
they downloaded, and notebook 05 globs `data/raw/pier/` for its input.

`course-reference` is only ever used for 045, 046 and 047, which do not exist in their
Monday folder at all. That is what keeps the two folders unambiguous.

Teach from the **student versions** in `notebooks/`, not the completed ones. Their screens
match yours, and the 3 TODO cells in 05 and 1 in 04 are the only moments they type
anything. Give each TODO 2–3 minutes, then show the answer and move on.

### You never have to write code live

Both completed notebooks are fully executed with every output stored:

- `reference/05_reliable_code_complete.ipynb` — 18/18 cells run, 10 figures, every TODO answered
- `reference/04_remote_data_complete.ipynb` — 8/10 cells with outputs

Open them and scroll. Nothing needs a kernel, a network, or a working `data/raw/`. If a TODO
stalls the room, switch to the completed one, show the answer, and carry on.

Both resolve `PROJECT_ROOT` correctly from `reference/`, so if you *do* run a cell it will work.
The kernel is pinned in the file, so opening it selects `climate-data-foundations` for you.

Five cells in the completed 05 print red tracebacks. **That is the lesson, not a failure** —
`NameError`, `FileNotFoundError`, `KeyError`, and two `AssertionError`s, each caught deliberately
inside `try`/`except`. Say so before someone raises a hand.

## Driving it

| Key | Does |
|---|---|
| `→` `space` | Reveal the next box; at the end of a slide, go to the next slide |
| `←` | Step back a box, then back a slide |
| `↓` | Reveal everything on this slide at once |
| `↑` | Collapse back to the first box |
| `Home` `End` | First / last slide |
| `⌘P` | Export to PDF, one slide per page, everything revealed |

The counter reads `12 / 50 · 2/4` — slide 12 of 50, showing 2 of its 4 boxes.

## Class instructions

Amber blocks headed **"Everyone — do this now"** are spoken instructions to the room,
not notes to yourself. They appear on slides 4, 5, 20, 26, 31, 38, 41 and 44, and they
say which file to open, which kernel to pick, and which cell to run. Read them out.

Each one is the last thing revealed on its slide, so the explanation lands before the
instruction to act.

## Progressive reveal

Boxes appear one at a time so a text-heavy slide does not land all at once.
Nothing moves when a box appears; hidden boxes still occupy their space.

Most slides need no markup for this — the script finds the major boxes
(`.card`, `.fix`, `.decode > div`, `figure`, `.diff`, tables) and reveals them in
document order. Add `data-step="N"` when you want a different order or want
several elements to appear together:

```html
<div class="decode">
  <div data-step="1">…</div>   <!-- appears first  -->
  <div data-step="2">…</div>   <!-- then this      -->
</div>
<div class="diff" data-step="3">…</div>   <!-- last, though it sits earlier in the DOM -->
```

If a slide has any `data-step`, only those elements are revealed and everything
else stays visible from the start. The error slides use this to keep the
traceback on screen throughout while the explanation builds under it.

A container marked `data-reveal="swap"` shows only its most recently revealed
child rather than stacking them. The Mandelbrot chronology uses it to change the
figure on the right as each year appears.

## Editing

`deck_template.html` is the source: one file, CSS at the top, one
`<section class="slide">` per slide.

Figures cannot be linked. The published page is served under a CSP that blocks
every external host, and relative paths do not resolve, so figures are inlined as
base64 `data:` URIs at build time. The template refers to them by name:

```html
<img class="fig" src="{{FIG:lorenz_attractor}}" alt="…">
```

After editing:

```bash
python3 build_deck.py       # writes wednesday_deck.html
```

## US spellings

The build refuses a template containing British spellings and names the offenders:

```
  friday: US spelling required
      coloured -> colored  (2x)
```

`colour`, `centre`, `analyse`, `labelled`, `programme`, `judgement`, `grey` and about thirty others
are checked. They keep reappearing because so much scientific prose uses them, so the check runs on
every build rather than depending on anyone spotting them. The list is `BRITISH` at the top of
`build_deck.py`; add a pair if a new one turns up.

`wednesday_deck.html` is generated. Do not edit it by hand.

## Figures

`make_figures.py` writes nine PNGs into `figs/`. Everything is computed from
scratch, so it needs no course data and no network. Takes about 15 seconds.

| File | Shows |
|---|---|
| `lorenz_attractor.png` | The butterfly, x–z plane |
| `lorenz_separation.png` | Two runs 10⁻⁹ apart, growing then saturating |
| `mandelbrot.png` | The set at full extent |
| `mandelbrot_orbits.png` | Three points and their orbits — what the plot *is* |
| `mandelbrot_precision.png` | The same window in float64 and float32 |
| `mandelbrot_zoom.png` | Structure surviving three zoom levels |
| `julia_set.png` | A Julia set, for the 1918 row |
| `coastline_ruler.png` | A Koch curve measured with three rulers |
| `brooks_matelski.png` | The set drawn in asterisks, as in 1978 |

Re-run only when a figure changes:

```bash
python3 make_figures.py
python3 build_deck.py
```

Figures are saved with transparent backgrounds and mid-tone colors so they read
against both the light and the dark version of the page.

The three points in `mandelbrot_orbits.png` were checked before use: `c = -0.5`
never escapes, `-0.76 + 0.09i` escapes at step 35, `0.4 + 0.3i` at step 15. Pick
new ones by eye and you will label an interior point "outside" — several that
look outside are not.

## Adding a figure

1. Save the PNG into `figs/`.
2. Reference it in the template as `{{FIG:<filename without extension>}}`.
3. Re-run `build_deck.py`.

The build fails if a placeholder has no matching file, and warns if the page
passes the 16 MB publishing limit. Currently 2.4 MB.
