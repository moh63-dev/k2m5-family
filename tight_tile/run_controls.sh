#!/bin/bash
# The Tight-Tile controls: the unmodified board certifies, each mutant is refused.  Logs go to out_controls/.
#   cd tight_tile && bash run_controls.sh            (cap 2000 cells; CAP=6000 reproduces the 1,190 refused cells of the
#                                                    ctl_rise mutant recorded in docs/TIGHT_TILE_PROOF.md)
cd "$(dirname "$0")"
CAP=${CAP:-2000}; B=../certificate/sol_exact_box11.txt; O=out_controls
mkdir -p $O; python3 --version > $O/versions.txt 2>&1
python3 -c "import numpy, scipy; print('numpy', numpy.__version__, 'scipy', scipy.__version__)" >> $O/versions.txt 2>&1
[ -f ctl_rise.txt ] || gunzip -k ctl_rise.txt.gz
python3 ctl_mutants.py $B $O
for c in $B ctl_rise.txt $O/mut_all099.txt $O/mut_x2_099.txt; do
  echo "== $c"; python3 ctl_rise.py $c $CAP 2>&1 | grep -v progress | tee -a $O/controls_cap$CAP.out
done
