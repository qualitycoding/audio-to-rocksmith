# Research round 1 — 2026-09-23 (single agent: reviewer/re-planner)

Scope: re-grade every v1 claim against evidence; run cheap spikes in the sandbox.

Actions and results
1. GitHub: repo `qualitycoding/audio-to-rocksmith` is public and empty; API reports push permission for the supplied token.
2. S1 (research/spikes/S1-python-resolve): pip dry-run resolution. basic-pitch 0.4.0 fails on py3.12 (tensorflow<2.15.1), resolves on 3.10 and 3.11.
3. S3: installed basic-pitch 0.4.0 on CPython 3.11.16 (uv). First run failed: `ModuleNotFoundError: pkg_resources` from resampy 0.4.2 with setuptools ≥ 81. Pinning setuptools 80.10.2 fixed it. Synthetic results: guitar F1 0.96; bass F1 0.80 with octave-up false positives.
4. S2: Rocksmith2014.NET inspected at pinned commit. MIT, net10.0; PSARC=AES-CFB, SNG=AES-CTR; Wwise 2019/21/22/23 (Wine on Linux); buildPackages, DD generator, PhraseGenerator, ArrangementChecker present.
5. Web: DLC Builder v3.5.0 cross-platform; RSTK line reached 2.9.0.0 and community reports tie it to Wwise 2013.

Not possible in this sandbox (recorded, not faked)
- .NET 10 SDK: download host not on the allowed network list → rs-pack not built.
- Wwise: proprietary installer, account required → not installed.
- Benchmark datasets on Zenodo: host not allowed → C-020/C-021 unverified.
- In-game load test: requires Rocksmith 2014 on PC.

Termination: protocol minimum of 3 rounds NOT met. Remaining rounds are plan step S-001 (research completion) to be run by the implementer before the freeze (S-003).
