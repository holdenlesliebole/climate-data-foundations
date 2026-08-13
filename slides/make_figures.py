"""Generate the static figures used by the Wednesday deck.

Everything here is computed from scratch, so this runs offline and needs no
course data. Figures are saved with transparent backgrounds and mid-tone colors
so they stay legible against either the light or the dark artifact ground.

    python3 make_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "figs"
OUT.mkdir(exist_ok=True)

RED, CYAN, GRAY = "#D9534A", "#2E9BA0", "#8A939F"

plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "savefig.facecolor": "none",
    "text.color": GRAY,
    "axes.labelcolor": GRAY,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "axes.edgecolor": GRAY,
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


# --------------------------------------------------------------------------
# Lorenz
# --------------------------------------------------------------------------
def lorenz_step(state, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    x, y, z = state
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])


def integrate(state, dt, steps):
    out = np.empty((steps, 3))
    s = np.asarray(state, dtype=float)
    for i in range(steps):
        k1 = lorenz_step(s)
        k2 = lorenz_step(s + 0.5 * dt * k1)
        k3 = lorenz_step(s + 0.5 * dt * k2)
        k4 = lorenz_step(s + dt * k3)
        s = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        out[i] = s
    return out


DT, STEPS = 0.004, 16000

traj = integrate([1.0, 1.0, 1.0], DT, STEPS)[2000:]
fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=170)
ax.plot(traj[:, 0], traj[:, 2], lw=0.35, color=CYAN, alpha=0.85)
ax.set_xlabel("x")
ax.set_ylabel("z")
ax.set_title("Lorenz attractor  ·  ρ = 28", color=GRAY, fontsize=12, pad=10)
fig.tight_layout()
fig.savefig(OUT / "lorenz_attractor.png", transparent=True)
plt.close(fig)

# The separation saturates once the two runs are as far apart as the attractor
# is wide. Past that point the curve is flat and the number means nothing.
a = integrate([1.0, 1.0, 1.0], DT, STEPS)
b = integrate([1.0 + 1e-9, 1.0, 1.0], DT, STEPS)
sep = np.linalg.norm(a - b, axis=1)
time = np.arange(STEPS) * DT

fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=170)
ax.semilogy(time, sep, lw=1.4, color=RED)
ax.axhline(sep[-3000:].mean(), ls="--", lw=1.1, color=GRAY)
ax.text(time[-1] * 0.985, sep[-3000:].mean() * 1.7,
        "saturated — number is now meaningless",
        ha="right", va="bottom", fontsize=10, color=GRAY)
ax.set_xlabel("time")
ax.set_ylabel("distance between the two runs")
ax.set_title("Two starts, one billionth apart", color=GRAY, fontsize=12, pad=10)
ax.grid(True, which="major", lw=0.4, alpha=0.25, color=GRAY)
fig.tight_layout()
fig.savefig(OUT / "lorenz_separation.png", transparent=True)
plt.close(fig)


# --------------------------------------------------------------------------
# Mandelbrot
# --------------------------------------------------------------------------
def render(center, span, width=780, height=580, max_iter=600, dtype=np.float64):
    ctype = np.complex128 if dtype is np.float64 else np.complex64
    aspect = height / width
    x = np.linspace(center[0] - span / 2, center[0] + span / 2, width).astype(dtype)
    y = np.linspace(center[1] - span * aspect / 2,
                    center[1] + span * aspect / 2, height).astype(dtype)
    c = (x[None, :] + 1j * y[:, None]).astype(ctype)
    z = np.zeros_like(c)
    counts = np.full(c.shape, max_iter, dtype=float)
    alive = np.ones(c.shape, dtype=bool)
    for i in range(max_iter):
        z[alive] = z[alive] ** 2 + c[alive]
        escaped = alive & (np.abs(z) > 2.0)
        counts[escaped] = i
        alive &= ~escaped
        if not alive.any():
            break
    return counts, len(np.unique(x))


counts, _ = render((-0.6, 0.0), 3.2)
fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=170)
ax.imshow(counts, cmap="magma", origin="lower", interpolation="bilinear")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("The Mandelbrot set", color=GRAY, fontsize=12, pad=10)
fig.tight_layout()
fig.savefig(OUT / "mandelbrot.png", transparent=True)
plt.close(fig)

# Same window, two number formats. In float32 the pixel spacing falls below what
# the format can represent, so 460 requested columns collapse onto 35 positions.
# Nothing raises; the picture just goes smooth.
CENTER, SPAN, WIDTH = (-0.7436447860, 0.1318252536), 2e-6, 460

fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=170)
for ax, (dtype, label) in zip(axes, [(np.float64, "float64  ·  what you have"),
                                     (np.float32, "float32  ·  arithmetic exhausted")]):
    counts, distinct = render(CENTER, SPAN, width=WIDTH, height=360,
                              max_iter=1200, dtype=dtype)
    ax.imshow(np.log1p(counts), cmap="magma", origin="lower", interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(label, color=GRAY, fontsize=12, pad=8)
    exhausted = distinct < WIDTH
    ax.text(0.5, -0.055, f"{WIDTH} pixels requested → {distinct} distinct positions",
            transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
            color=RED if exhausted else GRAY,
            fontweight="bold" if exhausted else "normal")

fig.suptitle(f"The same window, span {SPAN:.0e}  —  no error is raised either way",
             color=GRAY, fontsize=11.5, y=1.04)
fig.tight_layout()
fig.savefig(OUT / "mandelbrot_precision.png", transparent=True, bbox_inches="tight")
plt.close(fig)

for p in sorted(OUT.glob("*.png")):
    print(f"{p.name:28s} {p.stat().st_size / 1024:7.0f} KB")


# --------------------------------------------------------------------------
# History figures — one per row of the Mandelbrot chronology slide
# --------------------------------------------------------------------------

def escape_counts(c, max_iter=400):
    z = np.zeros_like(c)
    counts = np.full(c.shape, max_iter, dtype=float)
    alive = np.ones(c.shape, dtype=bool)
    for i in range(max_iter):
        z[alive] = z[alive] ** 2 + c[alive]
        gone = alive & (np.abs(z) > 2.0)
        counts[gone] = i
        alive &= ~gone
        if not alive.any():
            break
    return counts


def julia_counts(c_const, width=760, height=560, span=3.0, max_iter=400):
    aspect = height / width
    x = np.linspace(-span / 2, span / 2, width)
    y = np.linspace(-span * aspect / 2, span * aspect / 2, height)
    z = x[None, :] + 1j * y[:, None]
    counts = np.full(z.shape, max_iter, dtype=float)
    alive = np.ones(z.shape, dtype=bool)
    for i in range(max_iter):
        z[alive] = z[alive] ** 2 + c_const
        gone = alive & (np.abs(z) > 2.0)
        counts[gone] = i
        alive &= ~gone
        if not alive.any():
            break
    return counts


# 1918 — a Julia set, the kind of object described entirely by hand
fig, ax = plt.subplots(figsize=(6.2, 4.6), dpi=170)
ax.imshow(np.log1p(julia_counts(-0.4 + 0.6j)), cmap="magma", origin="lower",
          interpolation="bilinear")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("A Julia set for c = −0.4 + 0.6i", color=GRAY, fontsize=12, pad=10)
ax.text(0.5, -0.045, "Julia and Fatou derived the properties of these by hand.",
        transform=ax.transAxes, ha="center", va="top", fontsize=10, color=GRAY)
fig.tight_layout()
fig.savefig(OUT / "julia_set.png", transparent=True, bbox_inches="tight")
plt.close(fig)


# 1967 — the coastline paradox, via a Koch curve measured with three rulers
def koch(n):
    pts = np.array([[0.0, 0.0], [1.0, 0.0]])
    for _ in range(n):
        out = [pts[0]]
        for p, q in zip(pts[:-1], pts[1:]):
            d = (q - p) / 3.0
            a = p + d
            b = p + 2 * d
            angle = np.pi / 3
            rot = np.array([[np.cos(angle), -np.sin(angle)],
                            [np.sin(angle), np.cos(angle)]])
            peak = a + rot @ d
            out += [a, peak, b, q]
        pts = np.array(out)
    return pts


fig, axes = plt.subplots(1, 3, figsize=(10.2, 2.6), dpi=170)
for ax, n in zip(axes, (1, 2, 3)):
    pts = koch(n)
    ax.plot(pts[:, 0], pts[:, 1], lw=1.3, color=CYAN)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(f"ruler = 1/{3 ** n}", color=GRAY, fontsize=11, pad=6)
    ax.text(0.5, -0.12, f"measured length {(4 / 3) ** n:.2f}", transform=ax.transAxes,
            ha="center", va="top", fontsize=10.5, color=RED, fontweight="bold")
fig.suptitle("The same coastline, three rulers. Shorter ruler, longer answer.",
             color=GRAY, fontsize=11.5, y=1.12)
fig.tight_layout()
fig.savefig(OUT / "coastline_ruler.png", transparent=True, bbox_inches="tight")
plt.close(fig)


# 1978 — the first published picture, a few hundred asterisks on a line printer
# A monospace cell is roughly 0.6 as wide as it is tall, so the grid needs about
# 1.9 columns per row to come out with the set's true proportions.
ROWS = 34
COLS = 64
x = np.linspace(-2.15, 0.75, COLS)
y = np.linspace(-1.25, 1.25, ROWS)
inside = escape_counts(x[None, :] + 1j * y[:, None], max_iter=60) >= 60
art = "\n".join("".join("*" if v else " " for v in row) for row in inside[::-1])

fig = plt.figure(figsize=(5.4, 3.1), dpi=170)
fig.text(0.5, 0.46, art, ha="center", va="center",
         family="monospace", fontsize=7.4, linespacing=1.0, color=GRAY)
fig.text(0.5, 0.97, "Roughly what the first published picture looked like, 1978",
         ha="center", va="top", fontsize=11.5, color=GRAY)
fig.savefig(OUT / "brooks_matelski.png", transparent=True, bbox_inches="tight",
            pad_inches=0.12)
plt.close(fig)


# 1990s — structure that keeps going, however far in you look
fig, axes = plt.subplots(1, 3, figsize=(10.2, 2.9), dpi=170)
views = [((-0.6, 0.0), 3.2, "full extent"),
         ((-0.745, 0.113), 0.06, "50× in"),
         ((-0.745, 0.113), 0.0025, "1,300× in")]
for ax, (center, span, label) in zip(axes, views):
    w, h = 420, 330
    aspect = h / w
    gx = np.linspace(center[0] - span / 2, center[0] + span / 2, w)
    gy = np.linspace(center[1] - span * aspect / 2, center[1] + span * aspect / 2, h)
    ax.imshow(np.log1p(escape_counts(gx[None, :] + 1j * gy[:, None], max_iter=900)),
              cmap="magma", origin="lower", interpolation="bilinear")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(label, color=GRAY, fontsize=11, pad=6)
fig.suptitle("Every zoom finds more boundary. It never smooths out.",
             color=GRAY, fontsize=11.5, y=1.06)
fig.tight_layout()
fig.savefig(OUT / "mandelbrot_zoom.png", transparent=True, bbox_inches="tight")
plt.close(fig)


# What the plot actually is: three points, three orbits
# Escape iterations verified by hand: never, 35, 15. A point that "looks outside"
# is not enough — c = 0.35 + 0.35i is actually in the set.
PROBES = [(-0.5 + 0.0j, "inside — never escapes", CYAN),
          (-0.76 + 0.09j, "on the edge — escapes at step 35", "#C9A227"),
          (0.4 + 0.3j, "outside — escapes at step 15", RED)]

fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0), dpi=170)

w, h, span, center = 620, 470, 3.2, (-0.6, 0.0)
gx = np.linspace(center[0] - span / 2, center[0] + span / 2, w)
gy = np.linspace(center[1] - span * h / w / 2, center[1] + span * h / w / 2, h)
axes[0].imshow(escape_counts(gx[None, :] + 1j * gy[:, None]), cmap="magma",
               origin="lower", interpolation="bilinear",
               extent=[gx[0], gx[-1], gy[0], gy[-1]])
for offset, (c_val, label, color) in zip([(12, 10), (-8, -20), (12, 8)], PROBES):
    axes[0].plot(c_val.real, c_val.imag, "o", ms=10, mfc="none", mec=color, mew=2.4)
    axes[0].annotate(label.split(" — ")[0], (c_val.real, c_val.imag),
                     textcoords="offset points", xytext=offset,
                     fontsize=11, color=color, fontweight="bold")
axes[0].set_xticks([]); axes[0].set_yticks([])
for s in axes[0].spines.values():
    s.set_visible(False)
axes[0].set_title("Pick any point c on the plane", color=GRAY, fontsize=12, pad=8)

STEPS_SHOWN = 60
for c_val, label, color in PROBES:
    z, mags = 0j, []
    for _ in range(STEPS_SHOWN):
        z = z * z + c_val
        mags.append(abs(z))
        if abs(z) > 1e8:
            break
    axes[1].semilogy(range(1, len(mags) + 1), mags, lw=1.9, color=color, label=label)
axes[1].axhline(2.0, ls="--", lw=1.2, color=GRAY)
axes[1].text(1, 2.6, "escape radius 2", ha="left", va="bottom", fontsize=10, color=GRAY)
axes[1].set_xlim(0, STEPS_SHOWN)
axes[1].set_xlabel("iteration of  z → z² + c   (starting from z = 0)")
axes[1].set_ylabel("|z|")
axes[1].set_title("Then see whether it runs away", color=GRAY, fontsize=12, pad=8)
axes[1].legend(frameon=False, fontsize=10, labelcolor=GRAY, loc="upper left",
               bbox_to_anchor=(0.0, 0.88))
axes[1].grid(True, lw=0.4, alpha=0.25, color=GRAY)

fig.tight_layout()
fig.savefig(OUT / "mandelbrot_orbits.png", transparent=True, bbox_inches="tight")
plt.close(fig)

print("\nhistory figures written")


# --------------------------------------------------------------------------
# What Lorenz saw in 1961: the same run, restarted from a rounded number
# --------------------------------------------------------------------------
FULL, ROUNDED = 0.506127, 0.506
T_END = 45.0
n = int(T_END / DT)

full = integrate([FULL, 1.0, 1.0], DT, n)
rounded = integrate([ROUNDED, 1.0, 1.0], DT, n)
t = np.arange(n) * DT

# First time the two runs differ by more than a tenth of the attractor's width.
gap = np.abs(full[:, 0] - rounded[:, 0])
split = t[np.argmax(gap > 3.0)]

fig, ax = plt.subplots(figsize=(9.4, 3.9), dpi=170)
ax.plot(t, full[:, 0], lw=1.3, color=CYAN, label=f"started from {FULL}")
ax.plot(t, rounded[:, 0], lw=1.3, color=RED, alpha=0.9, label=f"started from {ROUNDED}")
ax.axvline(split, ls="--", lw=1.1, color=GRAY)
ax.annotate("the two forecasts stop agreeing",
            xy=(split, ax.get_ylim()[1] * 0.82), xytext=(split - 1.0, ax.get_ylim()[1] * 0.98),
            ha="right", fontsize=10.5, color=GRAY,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
ax.text(split / 2, ax.get_ylim()[0] * 0.92, "indistinguishable", ha="center",
        fontsize=10.5, color=GRAY)
ax.set_xlabel("time in the model (not days)")
ax.set_ylabel("one of the three variables")
ax.set_xlim(0, T_END)
ax.legend(frameon=False, fontsize=10.5, labelcolor=GRAY, loc="lower right")
ax.grid(True, lw=0.4, alpha=0.22, color=GRAY)
fig.tight_layout()
fig.savefig(OUT / "lorenz_1961.png", transparent=True, bbox_inches="tight")
plt.close(fig)
print(f"lorenz_1961.png — runs diverge at t≈{split:.0f}")
