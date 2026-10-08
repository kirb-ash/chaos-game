"""Chaos Game library: regular polygons, linear maps, the game itself, and the Barnsley fern."""
import numpy as np

rng = np.random.default_rng(42)  # fixed seed -> reproducible figures


def polygon(n):
    """Vertices of a regular n-gon on the unit circle, first vertex on the x-axis. Shape (2, n)."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.array([np.cos(t), np.sin(t)])


def scale(r):
    """Uniform contraction T = r*I."""
    return r * np.eye(2)


def rot(theta):
    """Counterclockwise rotation matrix."""
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


# Restriction rules: rule(k_new, k_prev, n) -> True if the choice is allowed
not_same = lambda k, kp, n: k != kp
not_opposite = lambda k, kp, n: k != (kp + 2) % n  # meaningful for the square (n = 4)


def chaos_game(v, T, num=100000, rule=None):
    """Iterate x -> T(x - v_k) + v_k with v_k chosen at random. Returns a (2, num+1) array."""
    n = v.shape[1]
    pts = np.zeros((2, num + 1))
    pts[:, 0] = rng.random(2) - 0.5
    k_prev = None
    for j in range(num):
        k = rng.integers(n)
        if rule is not None and k_prev is not None:
            while not rule(k, k_prev, n):
                k = rng.integers(n)
        pts[:, j + 1] = T @ (pts[:, j] - v[:, k]) + v[:, k]
        k_prev = k
    return pts


# Barnsley fern: four affine maps x -> T x + Q chosen with probabilities P
FERN_T = [np.array([[0.85, 0.04], [-0.04, 0.85]]),
          np.array([[-0.15, 0.28], [0.26, 0.24]]),
          np.array([[0.2, -0.26], [0.23, 0.22]]),
          np.array([[0.0, 0.0], [0.0, 0.16]])]
FERN_Q = [np.array([0, 1.64]), np.array([-0.028, 1.05]), np.array([0, 1.6]), np.array([0, 0.0])]
FERN_P = [0.85, 0.07, 0.07, 0.01]


def barnsley_fern(num=50000):
    x = np.zeros((2, num + 1))
    x[:, 0] = rng.random(2)
    for j, i in enumerate(rng.choice(4, size=num, p=FERN_P)):
        x[:, j + 1] = FERN_T[i] @ x[:, j] + FERN_Q[i]
    return x
