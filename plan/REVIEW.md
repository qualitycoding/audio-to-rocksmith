# Review of plan v1 and summary of changes (v2)

Plan v1 (the pasted "Hardened TDD" output) was reviewed on 2026-09-23. This file records
what was wrong and where each fix lives, so a reader can audit the revision.

| # | Finding in v1 | Severity | Fix in v2 | Where |
|---|---|---|---|---|
| F1 | Integrity violations: "GitHub access verified" with a literal `<repo-url>`; claims marked "verified" with no spikes; setup "recorded as succeeded" without running | Critical | All claims re-graded from committed evidence only; three real spikes committed with outputs | research/claims.json, research/spikes/ |
| F2 | Toolchain wrong/stale: RSTK "v2.5.0.0", Wwise 2021.1 pairing, Windows-only GUI tool used as CLI | Critical | Packaging via Rocksmith2014.NET (MIT, pinned commit) through a thin in-repo .NET console tool `rs-pack` | D-003, S-020..S-023 |
| F3 | Wwise is proprietary; contradicts "open-source only" constraint; Linux needs Wine | High | Explicit exception A-010 requiring human sign-off (G-000); Linux support documented as "Wwise via Wine" | A-010, G-000 |
| F4 | Arrangement content missing: beat map, anchors, phrases/sections, chord templates, hand shapes, DD, tuning, preview, art, manifest | Critical | Full arrangement pipeline S-013..S-019; DD/phrases/checker reused from Rocksmith2014.NET | PLAN.md, D-006..D-009 |
| F5 | Runtime F1 decision rule impossible (no ground truth per song) | Critical | F1 is an offline benchmark (G-001); runtime uses proxies + optional `--review` pause | D-012, D-013, G-001 |
| F6 | Benchmark and metric unspecified | High | GuitarSet player-05 held-out; Slakh2100 bass test split; mir_eval note-onset F1, 50 ms / 50 cents | D-012, T-040..T-043 |
| F7 | Fret mapping heuristic ("> 5 fret span → reassign") not an algorithm | High | Viterbi over (string, fret) states with explicit cost function | D-008, T-010..T-016 |
| F8 | Demucs pinned and load-bearing though separation was out of scope | Medium | Removed; C-010 dropped | A-006 |
| F9 | Pins stale/unsatisfiable (basic-pitch 0.2.6, numpy 1.24.3, py 3.10.12) | High | Python 3.11 + resolved lock from spike S1/S3; setuptools<81 needed | ENVIRONMENT.md |
| F10 | Irrelevant V&V (convergence order, conservation laws, CAS, "64-bit everywhere") | Low | Replaced with domain checks: synthetic round-trip, determinism, onset tolerance | tests/SPEC.md |
| F11 | Success criteria 2–3 only human-checkable | High | Automated structural verification (unpack, decrypt SNG, compare to XML) before G-002 | S-023, T-060..T-064 |
| F12 | MIDI as intermediate loses string/fret | Medium | Internal NoteEvent JSON is canonical; MIDI emitted as side output | D-002 |
| F13 | Platform ambiguity (host OS vs game platform) | Low | A-008: host = Win/macOS/Linux; target = RS2014 Remastered PC (`_p.psarc`) | A-008 |
| F14 | Development gates conflated with end-user runtime review | Medium | Dev gates G-000..G-002; runtime review is a CLI feature (`--review`) | GATES.md, D-013 |
| F15 | Pre-mortem/cold-read claimed but not run | High | Author pre-mortem round 1 committed and labelled non-independent; independent rounds are S-002 | premortem/ |

New findings surfaced by the v2 spikes (not in v1 at all):
- basic-pitch 0.4.0 **cannot be installed on Python 3.12** on Linux (needs tensorflow<2.15.1; no cp312 wheel). → Python 3.11 (C-011).
- resampy 0.4.2 imports `pkg_resources`, absent from setuptools ≥ 81 → pin `setuptools<81` (C-012).
- Synthetic bass test: basic-pitch emits octave-up false positives (precision 0.667, recall 1.0). → Bass octave-harmonic suppression step (D-007, T-030).
- PSARC TOC uses AES-CFB, SNG uses AES-CTR (v1 said "AES-CTR" for PSARC). (C-001)
