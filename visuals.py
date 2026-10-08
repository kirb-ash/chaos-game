"""Extra visuals for the slides and the live demo.
Creates in figures/:  step_diagram.png, buildup.png, chaos_game.gif
Usage: python visuals.py
"""
import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from chaos_game import polygon, scale, chaos_game

TEAL, ORANGE = "#1F6F5C", "#E07A2F"
v = polygon(3)
pts = chaos_game(v, scale(0.5), 30000)

# 1) One step of the game: x -> midpoint between x and the chosen vertex
x = np.array([-0.15, -0.25])
vk = v[:, 0]
x_new = 0.5 * (x - vk) + vk
fig, ax = plt.subplots(figsize=(6, 6))
tri = np.c_[v, v[:, 0]]
ax.plot(tri[0], tri[1], "-", color="#B8C7BF", lw=1.5)
ax.plot(v[0], v[1], "*", color="k", ms=12)
ax.annotate("", xy=x_new, xytext=x, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5))
ax.plot(*x, "o", color=TEAL, ms=11)
ax.plot(*x_new, "o", color=ORANGE, ms=11)
ax.plot(*vk, "o", mfc="none", mec=TEAL, ms=18, mew=2)
ax.text(x[0] - 0.08, x[1] - 0.12, "x", fontsize=18, color=TEAL, ha="right")
ax.text(x_new[0] + 0.06, x_new[1] + 0.04, "x_new", fontsize=18, color=ORANGE)
ax.text(vk[0] - 0.02, vk[1] + 0.1, "v (chosen at random)", fontsize=15, ha="right")
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-0.95, 1.25); ax.set_ylim(-1.0, 1.0)
fig.savefig("figures/step_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# 2) Build-up strip: same rule, more and more points
counts = [10, 100, 1000, 20000]
fig, axes = plt.subplots(1, 4, figsize=(16, 4.3))
for ax, n in zip(axes, counts):
    ax.plot(pts[0, :n], pts[1, :n], ".", color=TEAL, markersize=2.5 if n < 1000 else 1)
    ax.plot(v[0], v[1], "k*", ms=8)
    ax.set_title(f"{n:,} points", fontsize=18)
    ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig("figures/buildup.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# 3) GIF: watch the triangle form (open in a browser or a slide show)
frames = []
steps = np.unique(np.logspace(0, np.log10(20000), 70).astype(int))
for n in steps:
    fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=80)
    ax.plot(pts[0, :n], pts[1, :n], ".", color=TEAL, markersize=2 if n < 1500 else 1)
    ax.plot(*pts[:, n], "o", color=ORANGE, ms=7)
    ax.plot(v[0], v[1], "k*", ms=10)
    ax.set_title(f"{n:,} points", fontsize=14)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1)
    buf = io.BytesIO(); fig.savefig(buf, format="png"); plt.close(fig)
    frames.append(Image.open(buf).convert("P", palette=Image.ADAPTIVE))
durations = [90] * (len(frames) - 1) + [2500]
frames[0].save("figures/chaos_game.gif", save_all=True, append_images=frames[1:],
               duration=durations, loop=0)
print("saved step_diagram.png, buildup.png, chaos_game.gif")
