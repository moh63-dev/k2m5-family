#!/usr/bin/env python3
"""Exact check of the untilted face theta = 0 of mu_11:  every closed axis-parallel unit square in [0,11]^2 has mass >= 1.

Usage:  python3 axis_exact.py certificate/sol_exact_box11.txt

Method.  By the D4 symmetry of mu_11 it suffices to take square centres c in [1/2, 11/2]^2.  Every breakpoint of the mass
as a function of c is a multiple of 1/10 (segment ends, the corners of the Lebesgue square [19/5, 36/5]^2, and their shifts by 1/2),
so on each open cell of the 1/10 grid the mass of the (closed) square is bilinear in c.  For closed squares the mass is
upper semicontinuous in c, so its value at any c is at least the smallest limit value over the corners of the cells that
contain c.  We therefore evaluate, exactly (integer arithmetic), the bilinear function of every open cell at its four
corners and check that the minimum is >= 1.  The bilinear function is recovered from its values at the four points
(1/4, 1/4), (3/4, 1/4), (1/4, 3/4), (3/4, 3/4) of the cell, where no square edge meets a segment end.
Standard library + numpy.
"""
import sys
import numpy as np
from fractions import Fraction as F

path = sys.argv[1]
L = [l for l in open(path).read().split("\n") if not l.startswith("#")]   # comment lines (controls carry an extra one)
assert L[0].startswith("mixed") and L[4] == "0"
n = int(L[5])
den = int(L[3])                                   # mass denominator: weights are w/den
seg = np.array([list(map(int, l.split()[:5])) for l in L[6:6 + n]], dtype=object)
tail = L[6 + n:]
assert tail[0] == "1" and tail[1].split()[0] == "4"
poly = tail[1].split()
pw = int(poly[1]); px = [int(v) for v in poly[2::2]]; py = [int(v) for v in poly[3::2]]
assert (min(px), max(px), min(py), max(py)) == (38, 72, 38, 72) and len({*zip(px, py)}) == 4
# coordinates are in units of 1/10.  Work in units of 1/40: multiply by 4.  Square half-side = 1/2 = 20 units.
S = 4
x1, y1, x2, y2 = [np.array(seg[:, i], dtype=np.int64) * S for i in range(4)]
w = np.array(seg[:, 4], dtype=np.int64)
horiz = (y1 == y2)
assert np.all(horiz | (x1 == x2)) and np.all(np.abs((x2 - x1) + (y2 - y1)) == S)
xl, xh = np.minimum(x1, x2), np.maximum(x1, x2)
yl, yh = np.minimum(y1, y2), np.maximum(y1, y2)
H = 20
# Lebesgue square [38,72]^2 in 1/10 units -> [152,288]^2 in 1/40 units; density 1 (weight = area, asserted below)
LX0, LX1 = min(px) * S, max(px) * S
area10 = (max(px) - min(px)) * (max(py) - min(py))          # in (1/10)^2 units
assert pw * 100 == den * area10, 'Lebesgue weight is not the area (density 1)'


def mass_num(cx, cy):
    """mass * den * 4 * (units) for the closed square of centre (cx, cy) given in 1/40 units; returns an exact int.
    Segment part: w * overlap_length / segment_length, segment length = S = 4 units -> numerator w * overlap, denominator 4.
    Lebesgue part: area overlap in (1/40)^2 units; mass = area / (S*S*100) * den  (area of unit 1 = (10*S)^2 units^2)."""
    X0, X1, Y0, Y1 = cx - H, cx + H, cy - H, cy + H
    ov_h = np.maximum(0, np.minimum(xh, X1) - np.maximum(xl, X0))
    ov_v = np.maximum(0, np.minimum(yh, Y1) - np.maximum(yl, Y0))
    inside_h = (y1 > Y0) & (y1 < Y1)            # sample points avoid equality, so strict = non-strict
    inside_v = (x1 > X0) & (x1 < X1)
    seg_part = int(np.sum(np.where(horiz & inside_h, w * ov_h, 0) + np.where((~horiz) & inside_v, w * ov_v, 0)))
    ax = max(0, min(LX1, X1) - max(LX0, X0)); ay = max(0, min(LX1, Y1) - max(LX0, Y0))
    return seg_part, ax * ay


# mass as an exact rational: seg_part / S  +  (ax*ay) * den / (10*S)^2   (all over den)
def mass(cx, cy):
    sp, ar = mass_num(cx, cy)
    return F(sp, S) + F(ar * den, (10 * S) ** 2)


best = None; count_min = 0; corners = 0
for i in range(50):                  # c1 in [1/2 + i/10, 1/2 + (i+1)/10]
    for j in range(50):
        c0x, c0y = 20 + 4 * i + 0, 20 + 4 * j + 0         # cell lower corner in 1/40 units (centre 1/2 = 20 units)
        v = {}
        for a, b in ((1, 1), (3, 1), (1, 3), (3, 3)):      # quarter points of the cell: cell width = 4 units
            v[(a, b)] = mass(c0x + a, c0y + b)
        # bilinear f(s,t) on s,t in [0,1]: recover from the four values at s,t in {1/4, 3/4}
        # f = A + B s + C t + D s t ; values at (1/4,1/4),(3/4,1/4),(1/4,3/4),(3/4,3/4)
        f11, f31, f13, f33 = v[(1, 1)], v[(3, 1)], v[(1, 3)], v[(3, 3)]
        D = (f33 - f31 - f13 + f11) * 4                    # d^2 f / ds dt   (step 1/2 in both: divide by 1/4)
        B = (f31 - f11) * 2 - D * F(1, 4)                  # df/ds at t = 0  ... derived below
        C = (f13 - f11) * 2 - D * F(1, 4)
        A = f11 - B * F(1, 4) - C * F(1, 4) - D * F(1, 16)
        for s in (0, 1):
            for t in (0, 1):
                val = A + B * s + C * t + D * s * t
                corners += 1
                if best is None or val < best:
                    best, count_min = val, 1
                elif val == best:
                    count_min += 1
one = F(den)
print("cells 2500, corner limit values evaluated:", corners)
print("minimum limit value (mass units, 1 = %d):" % den, best, "=", float(best / den))
print("minimum attained at", count_min, "cell corners")
ok = best >= one
print("AXIS-FACE-OK (min exactly 1)" if best == one else ("AXIS-FACE-OK (min > 1)" if ok else "AXIS-FACE-FAILED"))
sys.exit(0 if ok else 1)
