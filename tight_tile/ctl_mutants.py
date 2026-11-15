"""Two more Tight-Tile controls, made from the board by exact integer arithmetic:

  mut_all099.txt   every segment weight multiplied by 99/100 (rounded down), so every wall tile has mass below 1;
  mut_x2_099.txt   only the segments on the line x = 2 multiplied by 99/100 (106 segments), so the tight tile between
                   the lines x = 1 and x = 2 loses mass at its right edge.

Usage:  python3 ctl_mutants.py ../certificate/sol_exact_box11.txt OUTDIR
Then:   python3 ctl_rise.py OUTDIR/mut_all099.txt 2000     (same chart and face point as the ctl_rise control)
Both must be refused (cells that fail the bound test, none certified at the face point (1, 1)); the unmodified board
certifies the same region.  See run_controls.sh.
"""
import os, sys
board, outdir = sys.argv[1], sys.argv[2]
L = open(board).read().split("\n")
n = int(L[6]); head, segs, tail = L[:7], L[7:7 + n], L[7 + n:]
os.makedirs(outdir, exist_ok=True)

def make(name, pick):
    out, k = [], 0
    for l in segs:
        x1, y1, x2, y2, w = map(int, l.split()[:5])
        w2 = (w * 99) // 100 if pick(x1, y1, x2, y2) else w
        k += w2 != w
        out.append("%d %d %d %d %d" % (x1, y1, x2, y2, w2))
    open(os.path.join(outdir, name), "w").write("\n".join(head + out + tail))
    print(name, "segments changed:", k)

make("mut_all099.txt", lambda x1, y1, x2, y2: True)
make("mut_x2_099.txt", lambda x1, y1, x2, y2: x1 == x2 == 20)
