# PLAN — audio-to-rocksmith (v2)

**Status: BLOCKED — HUMAN DECISION REQUIRED (G-000)**

Decisions needed: (1) accept Wwise as the sole proprietary dependency (A-010); (2) accept .NET 10 + Rocksmith2014.NET for packaging (A-003); (3) accept Python 3.11 only (A-013).
Also incomplete by design (cannot be done in the planning sandbox; now explicit steps): research rounds 2–3 (S-001), independent pre-mortem and cold read (S-002), test freeze (S-003).

- Active profiles: software, computational
- Claims: 7 verified, 6 corroborated, 1 single-source, 5 unverified (research/claims.json)
- Tests specified: 39 (unit 16, integration 6, package-verify 5, operational/security/perf 8, benchmark 4) — not yet frozen
- Steps: 21 · Gates: 3 (G-000, G-001, G-002)
- Risks (author round only, non-independent): Critical 0 open, High 0 open after mitigations, Medium 4, Low 2 (premortem/RISK_REGISTER.md)

See plan/REVIEW.md for what changed from v1.

## Step list at a glance
- S-000 Human scope acceptance (Fable (Mythos)) ← none → **G-000**
- S-001 Complete research (rounds 2–3+) (Opus) ← S-000
- S-002 Independent pre-mortem and cold read (Opus) ← S-001
- S-003 Stubs, tests, red run, freeze (Opus) ← S-002
- S-004 Environment locks for all host OSes (Sonnet) ← S-003
- S-010 Offline benchmark and parameter tuning (Opus) ← S-003, S-011 → **G-001**
- S-011 Audio input, provenance, CLI shell (Sonnet) ← S-003
- S-012 Transcription + cleaning (Sonnet) ← S-011
- S-013 Beat grid (Sonnet) ← S-011
- S-014 Chord grouping (Haiku) ← S-012
- S-016 Fret mapping (Viterbi) (Opus) ← S-014
- S-017 Arrangement XML (Opus) ← S-013, S-016, S-001
- S-018 Pipeline integration (Sonnet) ← S-017
- S-019 Resume and review mode (Sonnet) ← S-018
- S-020 rs-pack build tool (Opus) ← S-003
- S-021 Package verification tool (Opus) ← S-020
- S-022 Wwise conversion on a real host (Sonnet) ← S-020
- S-023 End-to-end packages (Sonnet) ← S-019, S-021, S-022
- S-024 In-game acceptance (Fable (Mythos)) ← S-023 → **G-002**
- S-025 Performance, security, docs (Sonnet) ← S-023
- S-026 Release candidate (Haiku) ← S-024, S-025

## Steps

### S-000 Human scope acceptance
- Tier: Fable (Mythos)
- Profile: All
- Depends on: none
- Inputs: plan/REVIEW.md, plan/ASSUMPTIONS.md
- Actions:
  1. Present REVIEW.md and A-003, A-010, A-013 to the human.
  2. Record answer verbatim in plan/GATE_LOG.md.
- Outputs: plan/GATE_LOG.md
- Evidence produced: none
- Done when: GATE_LOG.md contains a G-000 entry
- Checkpoint: gates.G-000 = answer
- On failure: If `stop`: halt. If `proceed-with-changes`: amend ASSUMPTIONS/DECISIONS, re-run S-002.
- Gate: G-000
- Relevant decisions/claims: A-003, A-010, A-013

### S-001 Complete research (rounds 2–3+)
- Tier: Opus
- Profile: All
- Depends on: S-000
- Inputs: research/*
- Actions:
  1. Open GuitarSet and Slakh2100 Zenodo records; verify C-020, C-021 (licence, splits, file layout); record in SOURCES.md.
  2. Read Rocksmith2014.XML InstrumentalArrangement types at the pinned commit; write `tests/schema/instrumental.xsd` and a prose schema note; upgrade C-008.
  3. Run R5 adversarial pass (fresh-context Opus) on every load-bearing claim; log research/rounds/round-2.md.
  4. Run a third round if round 2 produced any new load-bearing claim or downgrade (termination rule: ≥3 rounds, stop on a clean round, max 6).
- Outputs: research/rounds/round-2.md (+3..), research/claims.json, tests/schema/instrumental.xsd
- Evidence produced: claims C-008, C-020, C-021 upgraded
- Done when: No load-bearing claim below corroborated except C-002 and C-017 (verified in S-021/T-017)
- Checkpoint: research.rounds = N
- On failure: If a dataset licence forbids evaluation use: substitute and log in DEVIATIONS.md; if none available → BLOCKED.md
- Gate: none
- Relevant decisions/claims: C-008, C-020, C-021

### S-002 Independent pre-mortem and cold read
- Tier: Opus
- Profile: All
- Depends on: S-001
- Inputs: whole branch
- Actions:
  1. Fresh Opus agent (not the author) runs Phase 4 rounds from premortem/round-1.md onward until 0 Critical/High (max 5).
  2. Fresh Sonnet agent dry-runs HANDOFF.md + PLAN.md, lists every question; Haiku agent checks every referenced path/ID exists or is created earlier. Amend; repeat until zero items (max 5).
- Outputs: premortem/round-N.md, premortem/RISK_REGISTER.md, plan/COLD_READ.md
- Evidence produced: none
- Done when: RISK_REGISTER has 0 open Critical/High; COLD_READ last pass = 0 items
- Checkpoint: premortem.rounds, coldread.passes
- On failure: Non-convergence → status BLOCKED, escalate with options
- Gate: none
- Relevant decisions/claims: —

### S-003 Stubs, tests, red run, freeze
- Tier: Opus
- Profile: software, computational
- Depends on: S-002
- Inputs: plan/DECISIONS.md, tests/SPEC.md
- Actions:
  1. Create package skeleton `a2rs/` with every interface in DECISIONS.md raising NotImplementedError.
  2. Write `tests/fixtures/make_fixtures.py` (seed 0) and all tests in tests/SPEC.md.
  3. `pytest -q` → every test must fail (NotImplementedError / missing binary), none error at collection.
  4. `sha256sum tests/**/*.py tests/fixtures/* tests/schema/* > tests/FROZEN_MANIFEST.sha256`; add FROZEN header; add CI job `.github/workflows/freeze.yml` running `sha256sum -c`.
  5. Exception: `tests/expected/psarc_entries.json` (T-061) and `tests/fixtures/ci.wem.sha256` (T-025) are empty placeholders excluded from the manifest; they are populated once in S-021/S-022 and then appended to the manifest in a single commit referencing this step.
- Outputs: a2rs/**, tests/**, .github/workflows/freeze.yml
- Evidence produced: T-001..T-072 (red)
- Done when: `pytest -q` exit≠0 with 0 collection errors; `sha256sum -c tests/FROZEN_MANIFEST.sha256` OK
- Checkpoint: freeze.hash = manifest sha
- On failure: If a test cannot be made to fail cleanly: fix the test before freezing. After freeze: Test Challenge Rule (R8).
- Gate: none
- Relevant decisions/claims: —

### S-004 Environment locks for all host OSes
- Tier: Sonnet
- Profile: software
- Depends on: S-003
- Inputs: requirements.lock
- Actions:
  1. Regenerate lock on Windows and macOS runners with `uv pip compile` for py3.11 → requirements-{win,mac}.lock.
  2. Add requirements-dev.lock.
  3. CI matrix (ubuntu, windows, macos) installs and imports basic_pitch.
- Outputs: requirements*.lock, .github/workflows/ci.yml
- Evidence produced: none
- Done when: CI import job green on 3 OSes
- Checkpoint: env.locks
- On failure: macOS may resolve tensorflow-macos/coremltools: accept if import + T-023 pass; else document macOS unsupported (DEVIATIONS.md)
- Gate: none
- Relevant decisions/claims: C-011, C-012

### S-010 Offline benchmark and parameter tuning
- Tier: Opus
- Profile: computational
- Depends on: S-003, S-011
- Inputs: datasets (outside repo), a2rs.transcribe
- Actions:
  1. Implement `scripts/benchmark.py` per D-012.
  2. Tune D-005 params on the tuning split only (grid ≤ 48 configs); write a2rs/params.json with tuning log.
  3. Evaluate held-out once. Write results/benchmark.json.
- Outputs: scripts/benchmark.py, a2rs/params.json, results/benchmark.json
- Evidence produced: T-040..T-043; SC-4 value
- Done when: T-040..T-043 pass
- Checkpoint: benchmark.done, F1 values
- On failure: Compute over 10 h budget → reduce grid to 12 configs, log
- Gate: G-001
- Relevant decisions/claims: D-005, D-012, R4–R6

### S-011 Audio input, provenance, CLI shell
- Tier: Sonnet
- Profile: software
- Depends on: S-003
- Inputs: a2rs/audio.py, a2rs/cli.py
- Actions:
  1. Implement audio.load with soundfile; validation per T-002.
  2. Implement provenance (D-014) and CLI argument parsing (D-011) with exit codes.
- Outputs: a2rs/audio.py, a2rs/provenance.py, a2rs/cli.py
- Evidence produced: T-001, T-002, T-003, T-072
- Done when: those tests green
- Checkpoint: step.S-011
- On failure: Retry once; then BLOCKED.md
- Gate: none
- Relevant decisions/claims: D-002, D-011, D-014

### S-012 Transcription + cleaning
- Tier: Sonnet
- Profile: computational
- Depends on: S-011
- Inputs: a2rs/transcribe.py, a2rs/clean.py
- Actions:
  1. Wrap basic_pitch.inference.predict with D-005 ranges; cache model_output to work dir.
  2. Implement D-007 rules.
- Outputs: a2rs/transcribe.py, a2rs/clean.py
- Evidence produced: T-030..T-032
- Done when: green
- Checkpoint: step.S-012
- On failure: If T-030 cannot pass with D-007 rule → propose alternative rule in BLOCKED.md (frozen test)
- Gate: none
- Relevant decisions/claims: C-005, C-006, D-005, D-007

### S-013 Beat grid
- Tier: Sonnet
- Profile: computational
- Depends on: S-011
- Inputs: a2rs/beats.py
- Actions:
  Implement D-006.
- Outputs: a2rs/beats.py
- Evidence produced: T-017, T-018
- Done when: green
- Checkpoint: step.S-013
- On failure: If librosa misses T-017 tolerance on the click fixture → try `librosa.beat.plp` then constant-tempo fit; log
- Gate: none
- Relevant decisions/claims: C-017, D-006

### S-014 Chord grouping
- Tier: Haiku
- Profile: software
- Depends on: S-012
- Inputs: a2rs/chords.py
- Actions:
  Implement onset clustering (30 ms).
- Outputs: a2rs/chords.py
- Evidence produced: T-019
- Done when: green
- Checkpoint: step.S-014
- On failure: —
- Gate: none
- Relevant decisions/claims: D-009

### S-016 Fret mapping (Viterbi)
- Tier: Opus
- Profile: computational
- Depends on: S-014
- Inputs: a2rs/fretmap.py
- Actions:
  Implement D-008 exactly; vectorize state enumeration; cap states per group at 2000 (lowest-cost by emission).
- Outputs: a2rs/fretmap.py
- Evidence produced: T-010..T-016
- Done when: green
- Checkpoint: step.S-016
- On failure: If T-013 fails due to state cap → raise cap to 10000; if still failing → BLOCKED.md
- Gate: none
- Relevant decisions/claims: C-007, D-008

### S-017 Arrangement XML
- Tier: Opus
- Profile: software
- Depends on: S-013, S-016, S-001
- Inputs: a2rs/arrangement.py, tests/schema/instrumental.xsd
- Actions:
  Implement D-009 (Python side: ebeats, notes, chords, templates, handShapes, anchors, single level, tuning, properties).
- Outputs: a2rs/arrangement.py
- Evidence produced: T-020..T-022
- Done when: green
- Checkpoint: step.S-017
- On failure: Schema mismatch → consult Rocksmith2014.XML source; never edit the frozen XSD (R8)
- Gate: none
- Relevant decisions/claims: C-008, D-009

### S-018 Pipeline integration
- Tier: Sonnet
- Profile: software
- Depends on: S-017
- Inputs: a2rs/*
- Actions:
  Wire the CLI end-to-end up to job JSON; write notes.mid, pianoroll.png, report.json (D-013).
- Outputs: a2rs/pipeline.py, a2rs/project.py
- Evidence produced: T-023, T-071
- Done when: green
- Checkpoint: step.S-018
- On failure: T-023 below threshold → inspect per-stage outputs; tune within D-005 on synthetic only; do not touch held-out data
- Gate: none
- Relevant decisions/claims: D-013

### S-019 Resume and review mode
- Tier: Sonnet
- Profile: software
- Depends on: S-018
- Inputs: a2rs/pipeline.py
- Actions:
  Stage-level state.json in work dir; atomic writes; `--review`, `--resume-from`.
- Outputs: a2rs/pipeline.py
- Evidence produced: T-024, T-051, T-052
- Done when: green
- Checkpoint: step.S-019
- On failure: —
- Gate: none
- Relevant decisions/claims: D-013

### S-020 rs-pack build tool
- Tier: Opus
- Profile: software
- Depends on: S-003
- Inputs: vendor/Rocksmith2014.NET (submodule), tools/rs-pack
- Actions:
  1. Add submodule at pinned commit.
  2. Create F# console project referencing Rocksmith2014.XML, .XML.Processing, .DD, .DLCProject, .Audio, .PSARC, .SNG.
  3. Implement D-010 pipeline; `--audio-wem` bypass (D-015).
- Outputs: tools/rs-pack/**
- Evidence produced: T-025, T-050
- Done when: `dotnet build -c Release` ok; tests green
- Checkpoint: step.S-020
- On failure: R1
- Gate: none
- Relevant decisions/claims: C-003, C-004, C-009, D-010

### S-021 Package verification tool
- Tier: Opus
- Profile: software
- Depends on: S-020
- Inputs: tools/rs-pack
- Actions:
  1. Build a package from T-023 guitar XML; unpack; list entries → write the entry list to `tests/expected/psarc_entries.json` and append its hash to the freeze manifest (S-003 action 5).
  2. Implement `rs-pack verify` (T-060..T-064). Upgrade C-001, C-002.
- Outputs: tools/rs-pack/Verify.fs
- Evidence produced: T-060..T-064
- Done when: green
- Checkpoint: step.S-021
- On failure: —
- Gate: none
- Relevant decisions/claims: C-001, C-002

### S-022 Wwise conversion on a real host
- Tier: Sonnet
- Profile: software
- Depends on: S-020
- Inputs: developer machine with Wwise
- Actions:
  1. On Windows (primary) run rs-pack build without `--audio-wem`.
  2. Repeat on macOS and Linux+Wine; record outcome per host in research/spikes/S4-wwise/.
  3. Produce the CI WEM fixture; record SHA-256.
- Outputs: research/spikes/S4-wwise/*, tests/fixtures/ci.wem + ci.wem.sha256 (appended to manifest per S-003 action 5)
- Evidence produced: C-015 upgraded
- Done when: Windows conversion succeeds
- Checkpoint: wwise.hosts
- On failure: All hosts fail → D-015 fallback → BLOCKED (human)
- Gate: none
- Relevant decisions/claims: A-010, C-015, D-015

### S-023 End-to-end packages
- Tier: Sonnet
- Profile: software
- Depends on: S-019, S-021, S-022
- Inputs: fixtures
- Actions:
  Run `a2rs` on guitar and bass synthetic fixtures and one real stem; run verify on each.
- Outputs: out/*.psarc (not committed), results/e2e.json
- Evidence produced: T-060..T-064 on real outputs
- Done when: all verify reports pass
- Checkpoint: step.S-023
- On failure: —
- Gate: none
- Relevant decisions/claims: —

### S-024 In-game acceptance
- Tier: Fable (Mythos)
- Profile: All
- Depends on: S-023
- Inputs: out/*.psarc
- Actions:
  Hand PSARCs + instructions to human per G-002.
- Outputs: plan/GATE_LOG.md
- Evidence produced: SC-2, SC-3
- Done when: G-002 = proceed
- Checkpoint: gates.G-002
- On failure: `fix` → R3
- Gate: G-002
- Relevant decisions/claims: R3

### S-025 Performance, security, docs
- Tier: Sonnet
- Profile: software
- Depends on: S-023
- Inputs: —
- Actions:
  1. T-070 on 4-min fixture. 2. pip-audit (T-054). 3. README usage, Wwise setup, licence notes (Wwise not redistributed; datasets not shipped).
- Outputs: README.md, results/perf.json
- Evidence produced: T-053, T-054, T-070
- Done when: green
- Checkpoint: step.S-025
- On failure: Perf miss → profile; basic-pitch batch/hop settings only
- Gate: none
- Relevant decisions/claims: —

### S-026 Release candidate
- Tier: Haiku
- Profile: software
- Depends on: S-024, S-025
- Inputs: —
- Actions:
  Final consistency check (manifest, traceability, gates); tag `v0.1.0-rc1` on the generation branch. Do NOT publish a GitHub release without human instruction.
- Outputs: tag
- Evidence produced: none
- Done when: `sha256sum -c` ok; all rows traced
- Checkpoint: done
- On failure: —
- Gate: none
- Relevant decisions/claims: —
