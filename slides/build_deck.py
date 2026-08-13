"""Build the published decks from their templates.

Each template is content only. Two markers pull in the shared look and the
shared keyboard/reveal behavior:

    <!--SHELL:STYLE-->     replaced by _shell_style.html
    <!--SHELL:SCRIPT-->    replaced by _shell_script.html

Figures cannot be linked — the published page is served under a CSP that blocks
every external host, and relative paths do not resolve — so {{FIG:name}} is
replaced by a base64 data: URI of figs/name.png.

    python3 build_deck.py              # build every deck
    python3 build_deck.py thursday     # build one
"""
import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
FIGS = HERE / "figs"

DECKS = {
    "wednesday": ("deck_template.html", "wednesday_deck.html"),
    "thursday": ("thursday_template.html", "thursday_deck.html"),
    "friday": ("friday_template.html", "friday_deck.html"),
}


# The course is taught at Scripps and its written material uses US spellings.
# British forms keep reappearing because much of the source material and a lot of
# scientific prose uses them, so the build refuses rather than relying on anyone
# noticing. Add a pair here if a new one turns up.
BRITISH = {
    "colour": "color", "colours": "colors", "coloured": "colored",
    "behaviour": "behavior", "neighbour": "neighbor", "neighbouring": "neighboring",
    "centre": "center", "centred": "centered", "metre": "meter", "metres": "meters",
    "labelled": "labeled", "labelling": "labeling", "modelling": "modeling",
    "modelled": "modeled", "travelling": "traveling", "cancelled": "canceled",
    "analyse": "analyze", "analysing": "analyzing", "recognise": "recognize",
    "summarise": "summarize", "organise": "organize", "emphasise": "emphasize",
    "normalise": "normalize", "visualise": "visualize", "visualisation": "visualization",
    "generalise": "generalize", "minimise": "minimize", "maximise": "maximize",
    "programme": "program", "judgement": "judgment", "licence": "license",
    "defence": "defense", "practise": "practice", "grey": "gray",
    "whilst": "while", "amongst": "among", "learnt": "learned", "spelt": "spelled",
    "sceptical": "skeptical", "artefact": "artifact", "ageing": "aging",
}


def check_spelling(text, label):
    """Fail the build on British spellings in deck prose."""
    prose = re.sub(r"<style>.*?</style>|<script>.*?</script>", "", text, flags=re.S)
    found = {}
    for british, american in BRITISH.items():
        hits = len(re.findall(rf"\b{british}\b", prose, re.I))
        if hits:
            found[british] = (american, hits)
    if found:
        print(f"  {label}: US spelling required")
        for british, (american, hits) in sorted(found.items()):
            print(f"      {british} -> {american}  ({hits}x)")
        return False
    return True


def inline_figures(html, missing):
    def replace(match):
        name = match.group(1)
        path = FIGS / f"{name}.png"
        if not path.exists():
            missing.append(name)
            return match.group(0)
        return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")

    return re.sub(r"\{\{FIG:([A-Za-z0-9_\-]+)\}\}", replace, html)


def build(key):
    template_name, output_name = DECKS[key]
    template = HERE / template_name
    if not template.exists():
        print(f"  {key}: no template yet ({template_name}), skipped")
        return True

    html = template.read_text()
    if not check_spelling(html, key):
        return False
    for marker, partial in (("<!--SHELL:STYLE-->", "_shell_style.html"),
                            ("<!--SHELL:SCRIPT-->", "_shell_script.html")):
        if marker in html:
            html = html.replace(marker, (HERE / partial).read_text())

    figure_count = len(re.findall(r"\{\{FIG:[A-Za-z0-9_\-]+\}\}", html))
    missing = []
    html = inline_figures(html, missing)
    if missing:
        print(f"  {key}: MISSING figures -> {', '.join(sorted(set(missing)))}")
        return False
    leftover = re.findall(r"\{\{[^}]+\}\}|<!--SHELL:[A-Z]+-->", html)
    if leftover:
        print(f"  {key}: unresolved placeholders -> {leftover}")
        return False

    slides = html.count('<section class="slide')
    opened, closed = html.count("<section"), html.count("</section>")
    if opened != closed:
        print(f"  {key}: unbalanced <section> {opened}/{closed}")
        return False

    (HERE / output_name).write_text(html)
    size = (HERE / output_name).stat().st_size / 1_048_576
    flag = "  *** OVER 16 MB ***" if size > 16 else ""
    print(f"  {key}: {output_name}  {slides} slides, {figure_count} figures, {size:.2f} MB{flag}")
    return size <= 16


targets = sys.argv[1:] or list(DECKS)
unknown = [t for t in targets if t not in DECKS]
if unknown:
    sys.exit(f"unknown deck(s): {', '.join(unknown)}. Choose from {', '.join(DECKS)}")

print("building:")
ok = all(build(name) for name in targets)
sys.exit(0 if ok else 1)
