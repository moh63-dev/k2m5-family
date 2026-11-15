#!/usr/bin/env python3
"""Crop the board mu_11 to the segments that can matter for the root-9632 window.

Usage:  python3 crop_cover.py certificate/sol_exact_box11.txt > verification/r9632/c9632.txt

Keeps every segment of the board that meets (closed) one of the eight D4 images of the rectangle
[5403/1250, 2704/625] x [43199/10000, 43239/10000] of square centres, enlarged by 3/4 on every side.  The header,
the segment order, the weights and the trailing Lebesgue square are the board's, so the output is the board with
segments removed.  Exact rational arithmetic, standard library only.  The output (632 of 13,244 segments) is
byte-identical to the shipped c9632.txt; verification/verify.sh checks this.
"""
import sys
from fractions import Fraction as F

CX = (F(5403, 1250), F(2704, 625))
CY = (F(43199, 10000), F(43239, 10000))
M = F(3, 4)
K = 11


def boxes():
    out = []
    for sw in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                x, y = CX, CY
                if sw:
                    x, y = y, x
                if fx:
                    x = (K - x[1], K - x[0])
                if fy:
                    y = (K - y[1], K - y[0])
                out.append((x[0] - M, x[1] + M, y[0] - M, y[1] + M))
    return out


def main(path):
    lines = open(path).read().split("\n")
    head = lines[:5]                      # 'mixed 1', comment, '11 1', '10', mass denominator
    assert lines[5] == "0" and lines[6] == "13244", "unexpected board header"
    segs = lines[7:7 + 13244]
    tail = lines[7 + 13244:]
    bx = boxes()
    kept = []
    for l in segs:
        x1, y1, x2, y2 = [F(int(v), 10) for v in l.split()[:4]]
        xl, xh, yl, yh = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        if any(xl <= b and xh >= a and yl <= d and yh >= c for a, b, c, d in bx):
            kept.append(l)
    out = head[:2]
    out.append("# cropped by crop_cover.py to centres [5403/1250,2704/625] x [43199/10000,43239/10000] "
               "(+3/4, all D4 images): %d of 13244 segments" % len(kept))
    out += head[2:5] + ["0", str(len(kept))] + kept + tail
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
