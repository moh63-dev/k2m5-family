#!/usr/bin/env python3
"""Build one Lean module of K2m5 and print its wall time, CPU time and peak resident memory.

Usage:  K2M5_DIR=<dir holding K2m5/*.lean> LEAN_BIN=<path to lean> LEAN_PATH_EXTRA=<Mathlib and project lib dirs, ':'-separated> \
        python3 timed_build.py K2m5.Fam10

Output goes to <K2M5_DIR>/build/.  Peak memory is the largest resident size of the lean process (it includes the
memory-mapped Mathlib .olean files).  Linux and macOS.
"""
import os, resource, subprocess, sys, time

m = sys.argv[1]
d = os.environ["K2M5_DIR"]; lean = os.environ["LEAN_BIN"]; extra = os.environ.get("LEAN_PATH_EXTRA", "")
B = os.path.join(d, "build"); p = m.replace(".", "/")
os.makedirs(os.path.dirname(os.path.join(B, p)), exist_ok=True)
env = dict(os.environ); env["LEAN_PATH"] = B + ":" + extra
cmd = ["bash", "-c", f'ulimit -s unlimited 2>/dev/null; cd "{d}" && "{lean}" -DmaxHeartbeats=0 {p}.lean -o "{B}/{p}.olean" -i "{B}/{p}.ilean"']
t0 = time.time(); r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
pr = subprocess.run(cmd, env=env, capture_output=True, text=True)
t1 = time.time(); r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
div = 1e9 if sys.platform == "darwin" else 1e6            # ru_maxrss: bytes on macOS, kilobytes on Linux
errs = [l for l in (pr.stdout + pr.stderr).splitlines() if "error" in l.lower()]
print(f"== {m}: exit {pr.returncode}; wall {t1 - t0:.1f} s; cpu {(r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime):.1f} s;"
      f" peak RSS {r1.ru_maxrss / div:.2f} GB; errors {len(errs)}")
for l in errs[:3]:
    print("   ", l[:200])
sys.exit(pr.returncode)
