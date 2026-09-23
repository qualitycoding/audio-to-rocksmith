#!/usr/bin/env bash
# Spike S1: can basic-pitch 0.4.0 be resolved, and on which Python versions?
# Run from repo root. Requires pip >= 23. Network: pypi.org only.
set -u
OUT=research/spikes/S1-python-resolve
for pv in 3.12 3.11 3.10; do
  pip install --dry-run --quiet --report "$OUT/resolve-py$pv-linux.json" \
    --python-version "$pv" --only-binary=:all: \
    --platform manylinux2014_x86_64 --platform manylinux_2_17_x86_64 --platform manylinux_2_28_x86_64 \
    --target "/tmp/s1-$pv" "basic-pitch==0.4.0" mir_eval pretty_midi soundfile \
    > "$OUT/log-py$pv.txt" 2>&1
  echo "py$pv exit=$?" >> "$OUT/log-py$pv.txt"
done
