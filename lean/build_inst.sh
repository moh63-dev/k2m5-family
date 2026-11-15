#!/bin/bash
# Build the k^2-5 Lean instance, one module per process (each kernel check needs about 6 GB of memory), and write
# build_full.log with each module's wall time, CPU time and peak memory.
#   K2M5_DIR=<dir holding K2m5/*.lean>  LEAN_BIN=<lean>  LEAN_PATH_EXTRA=<Mathlib/project lib dirs, ':'-separated> \
#     bash build_inst.sh
# (Daniel's Lean project at evand/square-packing@659ee62 and its Mathlib must already be built; see README.md.)
set -e
: "${K2M5_DIR:?set K2M5_DIR}" "${LEAN_BIN:?set LEAN_BIN}"
HERE=$(cd "$(dirname "$0")" && pwd); LOG=$HERE/build_full.log
{ echo "# $(date -u +%Y-%m-%dT%H:%MZ)  $($LEAN_BIN --version)  $(uname -sm)"; } > "$LOG"
for m in Grid10 Fam10 InstData InstFam InstC1 InstC2 InstC3 InstC4 InstC5 InstC6 InstC7 Inst; do
  python3 "$HERE/timed_build.py" K2m5.$m | tee -a "$LOG"
  test -f "$K2M5_DIR/build/K2m5/$m.olean" || { echo "FAILED: $m" | tee -a "$LOG"; exit 1; }
done
printf 'import K2m5.Inst\n#print axioms SquarePacking.K2m5Inst.k2m5_of_valid11\n' > "$K2M5_DIR/K2m5/Ax.lean"
(cd "$K2M5_DIR" && LEAN_PATH="$K2M5_DIR/build:$LEAN_PATH_EXTRA" "$LEAN_BIN" K2m5/Ax.lean 2>&1 | tee -a "$LOG"); rm -f "$K2M5_DIR/K2m5/Ax.lean"
