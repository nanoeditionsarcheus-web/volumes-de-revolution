#!/usr/bin/env python3
"""
Shell method for volumes of revolution — two-panel vector diagram.

LEFT : 2D region under y = f(x), a <= x <= b, with one vertical strip of width dx.
RIGHT: the solid obtained by rotating that region 360° about the y-axis, drawn
       with a 90° wedge removed (270° shown) so the interior is visible.
       The orange strip becomes a thin cylindrical shell of inner radius x,
       outer radius x + dx and height f(x), coaxial with the y-axis.

The right panel is a flat oblique (cabinet-style) projection of the solid:
    screen_x = r * cos(phi)
    screen_y = y + E * r * sin(phi)
so the y-axis is the same vertical line (screen_x = 0) in both panels and all
heights are drawn at the same scale. Surfaces are painted back-to-front.

Output: shell_method.svg / .pdf (vector) and shell_method.png.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# --------------------------------------------------------------------------- #
# Parameters
# --------------------------------------------------------------------------- #
a, b = 1.0, 3.0            # limits of integration (a = b/3)
x0, dx = 1.7, 0.22         # position and radial thickness of the strip / shell
E = 0.38                   # foreshortening of the depth direction (elevated view)
OV = np.radians(2)         # angular overlap between adjacent pieces (hides AA seams)
PHI1, PHI2 = np.radians(205), np.radians(295)   # removed wedge: 205° -> 295°
                                                # (phi = 270° points at the viewer)

LIGHT, MED, DARK = "#BFDCF5", "#5FA8E0", "#1F5F9F"
ORANGE = "#F28C28"
LW = 0.9                   # outline width
FONT = dict(family="sans-serif", fontsize=13, zorder=100)


def f(x):
    """Smooth decreasing profile, positive on [a, b]."""
    return 0.35 + 2.1 * np.exp(-(x - a))


# --------------------------------------------------------------------------- #
# Drawing helpers
# --------------------------------------------------------------------------- #
def proj(r, phi, y):
    """Project cylindrical coordinates (r, phi, y) onto the page."""
    r, phi, y = np.broadcast_arrays(np.asarray(r, float),
                                    np.asarray(phi, float),
                                    np.asarray(y, float))
    return np.c_[r * np.cos(phi), y + E * r * np.sin(phi)]


def fill(ax, pts, color, z=0):
    ax.add_patch(Polygon(pts, closed=True, fc=color, ec="none", lw=0, zorder=z))


def line(ax, pts, z=0, **kw):
    kw = {**dict(color="k", lw=LW, solid_capstyle="round",
                 solid_joinstyle="round"), **kw}
    ax.plot(pts[:, 0], pts[:, 1], zorder=z, **kw)


def roof_piece(p0, p1, r0, r1):
    """Polygon of the top surface y = f(r), r in [r0, r1], phi in [p0, p1]."""
    ph = np.linspace(p0, p1, 160)
    rs = np.linspace(r0, r1, 60)
    return np.vstack([proj(r1, ph, f(r1)),               # outer arc
                      proj(rs[::-1], p1, f(rs[::-1])),   # radial edge at p1
                      proj(r0, ph[::-1], f(r0)),         # inner arc (back)
                      proj(rs, p0, f(rs))])              # radial edge at p0


def cut_face(phi, r0, r1):
    """Flat face in the half-plane at angle phi: 0 <= y <= f(r), r0 <= r <= r1."""
    rs = np.linspace(r0, r1, 80)
    return np.vstack([proj(rs, phi, 0.0), proj(rs[::-1], phi, f(rs[::-1]))])


def wall_band(r, p0, p1, y0, y1):
    """Vertical cylindrical band of radius r between heights y0 and y1."""
    ph = np.linspace(p0, p1, 160)
    return np.vstack([proj(r, ph, y0), proj(r, ph[::-1], y1)])


# --------------------------------------------------------------------------- #
# Figure
# --------------------------------------------------------------------------- #
fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 6.2), facecolor="white")
XLIM, YLIM = (-3.6, 3.8), (-1.6, 3.4)
for ax in (axL, axR):
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")

# =========================== LEFT PANEL: 2D region ========================== #
xs = np.linspace(a, b, 200)

# shaded region under the curve
fill(axL, np.vstack([np.c_[xs, np.zeros_like(xs)],
                     np.c_[xs[::-1], f(xs[::-1])]]), LIGHT, 1)

# orange strip: x -> x+dx, 0 -> f(x)
strip = np.array([[x0, 0], [x0 + dx, 0], [x0 + dx, f(x0)], [x0, f(x0)]])
fill(axL, strip, ORANGE, 2)
line(axL, np.vstack([strip, strip[:1]]), 3)

# curve and vertical sides of the region
line(axL, np.c_[xs, f(xs)], 3, lw=1.4)
line(axL, np.array([[a, 0], [a, f(a)]]), 3)
line(axL, np.array([[b, 0], [b, f(b)]]), 3)

# axes
line(axL, np.array([[XLIM[0] + 0.3, 0], [XLIM[1] - 0.3, 0]]), 4)
line(axL, np.array([[0, YLIM[0] + 0.4], [0, YLIM[1] - 0.3]]), 4)
for t in (a, b):
    line(axL, np.array([[t, -0.07], [t, 0.07]]), 4)

# labels
axL.text(XLIM[1] - 0.25, -0.35, "x", ha="center", va="top", **FONT)
axL.text(0.18, YLIM[1] - 0.3, "y", ha="left", va="top", **FONT)
axL.text(-0.15, -0.15, "0", ha="right", va="top", **FONT)
axL.text(a, -0.2, "a", ha="center", va="top", **FONT)
axL.text(b, -0.2, "b", ha="center", va="top", **FONT)
axL.text(x0, -0.2, "x", ha="center", va="top", **FONT)
axL.text(x0 + dx / 2, f(x0) + 0.12, "dx", ha="center", va="bottom", **FONT)
axL.text(1.05, f(1.05) + 0.18, "y = f(x)", ha="left", va="bottom", **FONT)

# ==================== RIGHT PANEL: 270° cutaway of the solid ================ #
TWO_PI = 2 * np.pi
z = 0  # running z-order (painter's algorithm, back to front)

# 1. back part of the top surface (phi 0° -> 180°) + orange band on it
z += 1; fill(axR, roof_piece(0, np.pi, a, b), MED, z)
z += 1; fill(axR, roof_piece(0, np.pi, x0, x0 + dx), ORANGE, z)
z += 1
ph = np.linspace(0, np.pi, 160)
line(axR, proj(b, ph, f(b)), z)                         # outer rim
for r in (x0, x0 + dx):
    line(axR, proj(r, ph, f(r)), z, lw=0.6)             # band edges

# 2. inner cylindrical wall (hollow core of radius a), back half, seen from inside
z += 1; fill(axR, wall_band(a, 0, np.pi, 0.0, f(a)), LIGHT, z)
z += 1
line(axR, proj(a, ph, 0.0), z)                          # base arc
line(axR, proj(a, ph, f(a)), z)                         # inner rim
line(axR, proj(a, np.pi, np.array([0.0, f(a)])), z)     # left silhouette
line(axR, proj(a, 0.0, np.array([0.0, f(a)])), z)       # right silhouette

# 3. front-left part of the top surface (180° -> 205°) and outer wall there
z += 1; fill(axR, roof_piece(np.pi - OV, PHI1, a, b), MED, z)
z += 1; fill(axR, roof_piece(np.pi - OV, PHI1, x0, x0 + dx), ORANGE, z)
z += 1; fill(axR, wall_band(b, np.pi, PHI1, 0.0, f(b)), MED, z)
z += 1
ph = np.linspace(np.pi, PHI1, 60)
line(axR, proj(b, ph, f(b)), z)                         # outer rim
line(axR, proj(b, ph, 0.0), z)                          # outer base
line(axR, proj(b, np.pi, np.array([0.0, f(b)])), z)     # outer silhouette
line(axR, proj(a, ph, f(a)), z)                         # inner rim
for r in (x0, x0 + dx):
    line(axR, proj(r, ph, f(r)), z, lw=0.6)

# 4. front-right part of the top surface (295° -> 360°) and outer wall there
z += 1; fill(axR, roof_piece(PHI2, TWO_PI + OV, a, b), MED, z)
z += 1; fill(axR, roof_piece(PHI2, TWO_PI + OV, x0, x0 + dx), ORANGE, z)
z += 1; fill(axR, wall_band(b, PHI2, TWO_PI, 0.0, f(b)), MED, z)
z += 1
ph = np.linspace(PHI2, TWO_PI, 120)
line(axR, proj(b, ph, f(b)), z)
line(axR, proj(b, ph, 0.0), z)
line(axR, proj(b, TWO_PI, np.array([0.0, f(b)])), z)
line(axR, proj(a, ph, f(a)), z)
for r in (x0, x0 + dx):
    line(axR, proj(r, ph, f(r)), z, lw=0.6)

# 5. the two flat cut faces (dark blue) carrying the shell's cross-section (orange)
for phi in (PHI1, PHI2):
    z += 1; fill(axR, cut_face(phi, a, b), DARK, z)
    z += 1; fill(axR, cut_face(phi, x0, x0 + dx), ORANGE, z)
    z += 1
    face = cut_face(phi, a, b)
    line(axR, np.vstack([face, face[:1]]), z)
    line(axR, proj(x0, phi, np.array([0.0, f(x0)])), z, lw=0.6)
    line(axR, proj(x0 + dx, phi, np.array([0.0, f(x0 + dx)])), z, lw=0.6)

# 6. axis of revolution (seen through the opening) and labels
z += 1
line(axR, np.array([[0, YLIM[0] + 0.4], [0, YLIM[1] - 0.3]]), z)
axR.text(0.18, YLIM[1] - 0.3, "y", ha="left", va="top", **FONT)
axR.text(-0.15, -0.15, "0", ha="right", va="top", **FONT)

pa, pb, px = (proj(r, PHI1, 0.0)[0] for r in (a, b, x0))
axR.text(pa[0], pa[1] - 0.12, "a", ha="center", va="top", **FONT)
axR.text(pb[0], pb[1] - 0.12, "b", ha="center", va="top", **FONT)
axR.text(px[0], px[1] - 0.12, "x", ha="center", va="top", **FONT)

pfx = proj(x0 + dx, PHI1, f(x0) / 2)[0]
axR.text(pfx[0] + 0.14, pfx[1], "f(x)", ha="left", va="center", **FONT)

pdx = proj(x0 + dx / 2, PHI2, 0.0)[0]
axR.text(pdx[0], pdx[1] - 0.12, "dx", ha="center", va="top", **FONT)

# --------------------------------------------------------------------------- #
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.05)
for ext in ("svg", "pdf", "png"):
    fig.savefig(f"shell_method.{ext}", dpi=200, facecolor="white")
plt.show()
