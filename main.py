"""Generates every figure into figures/ and prints the linear-algebra analysis.
Usage:  python main.py          (saves figures)
        python main.py --show   (also opens each figure window, handy for the live demo)
"""
import sys
import numpy as np
import matplotlib
if "--show" not in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from chaos_game import *

SHOW = "--show" in sys.argv


def save(pts, v, title, name, color="#1F6F5C", ms=1, size=(6, 6)):
    plt.figure(figsize=size)
    plt.plot(pts[0], pts[1], ".", color=color, markersize=ms)
    if v is not None:
        plt.plot(v[0], v[1], "k*")
    plt.axis("equal")
    plt.title(title)
    plt.savefig(f"figures/{name}.png", dpi=150, bbox_inches="tight")
    if SHOW:
        plt.show()
    plt.close()


def box_count_dim(pts, ks=range(2, 8)):
    """Box-counting dimension: slope of log N(eps) against log(1/eps)."""
    p = pts - pts.min(axis=1, keepdims=True)
    p /= p.max()
    logs_inv_eps, logs_n = [], []
    for k in ks:
        eps = 2.0 ** -k
        boxes = {tuple(b) for b in np.floor(p.T / eps).astype(int)}
        logs_inv_eps.append(np.log(1 / eps))
        logs_n.append(np.log(len(boxes)))
    return np.polyfit(logs_inv_eps, logs_n, 1)[0]


# ---- Figures ----
tri, sq, hexa, pent = polygon(3), polygon(4), polygon(6), polygon(5)
save(chaos_game(tri, scale(1/2)), tri, "Sierpinski triangle (r = 1/2)", "01_triangle_half")
save(chaos_game(tri, scale(1/3)), tri, "Triangle, r = 1/3", "02_triangle_third")
save(chaos_game(tri, 0.5 * rot(np.pi/18)), tri, "Triangle with rotation (theta = pi/18)", "03_triangle_rotation")
save(chaos_game(sq, scale(1/2)), sq, "Square, r = 1/2 (no fractal)", "04_square_half")
save(chaos_game(sq, scale(1/3)), sq, "Square, r = 1/3", "05_square_third")
save(chaos_game(sq, scale(1/2), rule=not_same), sq, "Square, r = 1/2, no repeated vertex", "06_square_no_repeat")
save(chaos_game(sq, scale(1/2), rule=not_opposite), sq, "Square, r = 1/2, no opposite vertex", "07_square_no_opposite")
save(barnsley_fern(), None, "Barnsley fern", "08_fern", color="#2F7D32", size=(5, 8))
save(chaos_game(hexa, scale(1/3)), hexa, "Hexagon, r = 1/3", "09_hexagon_third")
save(chaos_game(pent, scale(2/5), rule=not_same), pent, "Pentagon, r = 2/5, no repeated vertex", "10_pentagon_restricted")

# ---- Analysis 1: fractal dimension, measured vs theory ----
print("\nFractal dimension (box counting vs similarity dimension log(n)/log(1/r))")
print(f"{'case':<28}{'measured':>10}{'theory':>10}")
cases = [("triangle r=1/2", tri, 1/2, 3), ("triangle r=1/3", tri, 1/3, 3),
         ("square r=1/3", sq, 1/3, 4), ("hexagon r=1/3", hexa, 1/3, 6)]
for name, v, r, n in cases:
    d = box_count_dim(chaos_game(v, scale(r), 300000))
    print(f"{name:<28}{d:>10.3f}{np.log(n)/np.log(1/r):>10.3f}")
print("(theory is exact only when the pieces don't overlap; r=1/2 square fills the plane, dim 2)")

# ---- Analysis 2: linear-algebra properties of the fern maps ----
print("\nBarnsley fern: properties of each matrix T")
print(f"{'map':<5}{'det(T)':>9}{'|eigenvalues|':>26}  note")
for i, T in enumerate(FERN_T, 1):
    ev = np.linalg.eigvals(T)
    d = np.linalg.det(T)
    print(f"T{i:<4}{d:>9.4f}{str(np.round(np.abs(ev), 3)):>26}  "
          f"{'area shrinks to %.0f%%' % (abs(d)*100) if abs(d) > 1e-12 else 'collapses plane to a line (stem)'}")
print("Every map has spectral radius < 1 (shrinks distances in the long run) -> the iteration settles onto a unique attractor.")
print("\nFigures saved to figures/")
