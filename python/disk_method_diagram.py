#!/usr/bin/env python3
"""
Disk method for volumes of revolution — two-panel vector diagram.

LEFT : the region under y = f(x), a <= x <= b, with one vertical strip of width dx.
RIGHT: the solid obtained by rotating that region 360° about the x-axis, drawn
       with a wedge removed (angle THETA) so the interior is visible. The orange
       strip becomes a solid disk of radius f(x) and thickness dx, perpendicular
       to the x-axis.

The right panel is an oblique projection in cylindrical coordinates about the
x-axis (X along the axis, rho the radius, psi the angle, psi = 0 pointing up):
    screen_x = X + KX * rho * sin(psi)
    screen_y = rho * cos(psi) + KY * rho * sin(psi)
Depth (sin psi > 0) goes up and to the right, so the viewer looks from the
front, the right and above. The visible part of the outer surface is bounded
by its silhouette, obtained analytically from normal · view = 0.

Output: disk_method.svg / .pdf (vector) and disk_method.png.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# --------------------------------------------------------------------------- #
a, b = 1.0, 3.0
x0, dx = 1.7, 0.22
THETA = 90.0                        # opening of the removed wedge, in degrees (0-90)
KX, KY = 0.433, 0.25                # depth offset on screen (back = up-right)
M = np.hypot(1.0, KY)
BETA = np.arctan2(1.0, KY)
TWO_PI = 2 * np.pi

LIGHT, MED, DARK = "#BFDCF5", "#5FA8E0", "#1F5F9F"
ORANGE = "#F28C28"
LW = 0.9
FONT = dict(family="sans-serif", fontsize=13, zorder=100)


def f(x):
    return 0.35 + 2.1 * np.exp(-(x - a))


def fp(x):
    return -2.1 * np.exp(-(x - a))


# --------------------------------------------------------------------------- #
def proj(X, rho, psi):
    X, rho, psi = np.broadcast_arrays(np.asarray(X, float), np.asarray(rho, float),
                                      np.asarray(psi, float))
    return np.c_[X + KX * rho * np.sin(psi), rho * np.cos(psi) + KY * rho * np.sin(psi)]


def sil1(x):                        # upper silhouette of the outer surface
    return np.arccos(fp(x) * KX / M) - BETA


def sil2(x):                        # lower silhouette
    return TWO_PI - np.arccos(fp(x) * KX / M) - BETA


def wedge(theta):                   # removed wedge [psi1, psi2]; upper face vertical at 90°
    w = 12.0 * (1 - theta / 90.0)
    return np.radians(270 + w), np.radians(270 + w + theta)


def fill(ax, pts, color, z):
    ax.add_patch(Polygon(pts, closed=True, fc=color, ec="none", lw=0, zorder=z))


def line(ax, pts, z, **kw):
    kw = {**dict(color="k", lw=LW, solid_capstyle="round", solid_joinstyle="round"), **kw}
    ax.plot(pts[:, 0], pts[:, 1], zorder=z, **kw)


def lower(xa, xb, psi1):            # visible surface between sil2(x) and psi1
    xs = np.linspace(xa, xb, 60)
    return np.vstack([proj(xs, f(xs), sil2(xs)),
                      proj(xb, f(xb), np.linspace(sil2(xb), psi1, 60)),
                      proj(xs[::-1], f(xs[::-1]), psi1),
                      proj(xa, f(xa), np.linspace(psi1, sil2(xa), 60))])


def upper(xa, xb, psi2):            # visible surface between psi2 and sil1(x) + 2π
    xs = np.linspace(xa, xb, 60)
    return np.vstack([proj(xs, f(xs), sil1(xs) + TWO_PI),
                      proj(xb, f(xb), np.linspace(sil1(xb) + TWO_PI, psi2, 90)),
                      proj(xs[::-1], f(xs[::-1]), psi2),
                      proj(xa, f(xa), np.linspace(psi2, sil1(xa) + TWO_PI, 90))])


def face(psi, r0, r1):              # flat cut face in the half-plane at angle psi
    xs = np.linspace(r0, r1, 60)
    return np.vstack([proj(xs, 0.0, psi), proj(xs[::-1], f(xs[::-1]), psi)])


def cap(X, p0, p1):                 # flat end of the solid at x = X
    return np.vstack([proj(X, 0.0, 0.0), proj(X, f(X), np.linspace(p0, p1, 160))])


# --------------------------------------------------------------------------- #
fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.6), facecolor="white")
XLIM, YLIM = (-3.6, 3.8), (-2.9, 3.4)
for ax in (axL, axR):
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM); ax.set_aspect("equal"); ax.axis("off")

# =========================== LEFT PANEL ==================================== #
xs = np.linspace(a, b, 200)
fill(axL, np.vstack([np.c_[xs, np.zeros_like(xs)], np.c_[xs[::-1], f(xs[::-1])]]), LIGHT, 1)
strip = np.array([[x0, 0], [x0 + dx, 0], [x0 + dx, f(x0)], [x0, f(x0)]])
fill(axL, strip, ORANGE, 2); line(axL, np.vstack([strip, strip[:1]]), 3)
line(axL, np.c_[xs, f(xs)], 3, lw=1.4)
line(axL, np.array([[a, 0], [a, f(a)]]), 3); line(axL, np.array([[b, 0], [b, f(b)]]), 3)
line(axL, np.array([[XLIM[0] + 0.3, 0], [XLIM[1] - 0.3, 0]]), 4)
line(axL, np.array([[0, YLIM[0] + 0.4], [0, YLIM[1] - 0.3]]), 4)
for t in (a, b):
    line(axL, np.array([[t, -0.07], [t, 0.07]]), 4)
axL.text(XLIM[1] - 0.25, -0.35, "x", ha="center", va="top", **FONT)
axL.text(0.18, YLIM[1] - 0.3, "y", ha="left", va="top", **FONT)
axL.text(-0.15, -0.15, "0", ha="right", va="top", **FONT)
axL.text(a, -0.2, "a", ha="center", va="top", **FONT)
axL.text(b, -0.2, "b", ha="center", va="top", **FONT)
axL.text(x0, -0.2, "x", ha="center", va="top", **FONT)
axL.text(x0 + dx / 2, f(x0) + 0.12, "dx", ha="center", va="bottom", **FONT)
axL.text(1.05, f(1.05) + 0.18, "y = f(x)", ha="left", va="bottom", **FONT)

# =========================== RIGHT PANEL =================================== #
cut = THETA >= 4
psi1, psi2 = wedge(THETA) if cut else (np.radians(282),) * 2
x1 = x0 + dx
z = 0
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]

# axes behind the solid
z += 1
line(axR, np.array([[0, YLIM[0] + 0.4], [0, YLIM[1] - 0.3]]), z)
hid = KX * f(a) / M                                     # axis hidden behind the flared end
line(axR, np.array([[XLIM[0] + 0.3, 0], [a - hid, 0]]), z)

# 1-2. visible outer surface, lower and upper parts, with the orange band
z += 1; fill(axR, lower(a, b, psi1), MED, z); fill(axR, lower(x0, x1, psi1), ORANGE, z + 1)
z += 2; fill(axR, upper(a, b, psi2), MED, z); fill(axR, upper(x0, x1, psi2), ORANGE, z + 1)
z += 2
xsr = np.linspace(a, b, 80)
line(axR, proj(xsr, f(xsr), sil2(xsr)), z)
line(axR, proj(xsr, f(xsr), sil1(xsr) + TWO_PI), z)
line(axR, proj(a, f(a), np.linspace(sil2(a), psi1, 60)), z)
line(axR, proj(a, f(a), np.linspace(psi2, sil1(a) + TWO_PI, 90)), z)
for r in (x0, x1):
    line(axR, proj(r, f(r), np.linspace(sil2(r), psi1, 40)), z, lw=0.6)
    line(axR, proj(r, f(r), np.linspace(psi2, sil1(r) + TWO_PI, 60)), z, lw=0.6)

# 3. flat end at x = b
z += 1; fill(axR, cap(b, psi2, psi1 + TWO_PI), LIGHT, z)
z += 1; line(axR, proj(b, f(b), np.linspace(psi2, psi1 + TWO_PI, 160)), z)

# 4. cut faces with the disk's cross-section
if cut:
    for psi in (psi1, psi2):
        z += 1; fill(axR, face(psi, a, b), DARK, z); fill(axR, face(psi, x0, x1), ORANGE, z + 1)
        z += 2
        fc = face(psi, a, b); line(axR, np.vstack([fc, fc[:1]]), z)
        line(axR, proj(np.array([x0, x0]), np.array([0, f(x0)]), psi), z, lw=0.6)
        line(axR, proj(np.array([x1, x1]), np.array([0, f(x1)]), psi), z, lw=0.6)

# 5. axis in front (crease of the wedge and beyond the solid), labels
z += 1
line(axR, np.array([[a if cut else b, 0], [XLIM[1] - 0.3, 0]]), z)
axR.text(XLIM[1] - 0.25, -0.35, "x", ha="center", va="top", **FONT)
axR.text(0.18, YLIM[1] - 0.3, "y", ha="left", va="top", **FONT)
axR.text(-0.15, -0.15, "0", ha="right", va="top", **FONT)
for xx, s in ((a, "a"), (x0, "x"), (b, "b")):
    axR.text(xx, -0.2, s, ha="center", va="top", path_effects=HALO, **FONT)
if THETA >= 25:
    pf = proj(x1, f(x0) / 2, psi2)[0]
    axR.text(pf[0] + 0.14, pf[1], "f(x)", ha="left", va="center", path_effects=HALO, **FONT)
xm = x0 + dx / 2
pd = proj(xm, f(xm), sil1(xm) + TWO_PI)[0]
axR.text(pd[0], pd[1] + 0.12, "dx", ha="center", va="bottom", path_effects=HALO, **FONT)

# --------------------------------------------------------------------------- #
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.05)
for ext in ("svg", "pdf", "png"):
    fig.savefig(f"disk_method.{ext}", dpi=200, facecolor="white")
plt.show()
