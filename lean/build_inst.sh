#!/bin/bash
# Build the k^2-5 Lean instance, one module per process (each kernel check needs ~5.8 GB).
# Every module's output goes to build_full.log with its wall time and peak memory (GNU time -v on Linux, BSD time -l on macOS).
set -e
LOG=build_full.log; : > $LOG
tm() { if /usr/bin/time -v true >/dev/null 2>&1; then /usr/bin/time -v "$@"; else /usr/bin/time -l "$@"; fi; }
for m in Grid10 Fam10 InstData InstFam InstC1 InstC2 InstC3 InstC4 InstC5 InstC6 InstC7 Inst; do
  echo "== K2m5.$m" | tee -a $LOG; tm /home/claude/lean/mk.sh K2m5.$m >>$LOG 2>&1 || true
  test -f build/K2m5/$m.olean || { echo "FAILED: $m"; exit 1; }
done
printf 'import K2m5.Inst\n#print axioms SquarePacking.K2m5Inst.k2m5_of_valid11\n' > K2m5/Ax.lean
/home/claude/lean/mk.sh K2m5.Ax || true; rm K2m5/Ax.lean
