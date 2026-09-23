# Test specification (NOT FROZEN)

Status: specification only. Test code is written in S-003 against interface stubs, verified red, then frozen
(`tests/FROZEN_MANIFEST.sha256` + CI hash check). Freezing now would violate the protocol, because
C-002, C-008 and C-017 are still unverified and T-020/T-060 depend on them.

Conventions: pytest; every test docstring cites `Req:`/`Claim:`/`Decision:` IDs; no network; fixtures generated
deterministically by `tests/fixtures/make_fixtures.py` (seed 0) and hashed; tolerances stated in-line.

## Unit
| ID | Asserts | Enforces |
|---|---|---|
| T-001 | `audio.load` returns mono float32 for WAV/FLAC/OGG fixtures; SR preserved | SC-1, D-002 |
| T-002 | `audio.load` rejects: MP3, 0-byte, truncated FLAC, all-zero audio, > 20 min, non-audio with audio extension → exit code 2 path | security, D-011 |
| T-003 | NoteEvent invariants: offset > onset ≥ 0, 0 ≤ midi ≤ 127 (hypothesis property test) | D-002 |
| T-010 | fretmap: for every FretNote, `tuning[string] + fret == midi` | D-008 |
| T-011 | fretmap: no two notes of a chord share a string | D-008 |
| T-012 | fretmap: fretted span ≤ max_span for every chord; all frets in [capo, max_fret] | D-008 |
| T-013 | fretmap: scale run E2..E4 on guitar — Viterbi total cost ≤ cost of every greedy lowest-fret assignment (exhaustive check on ≤ 8-note sequences) | D-008 optimality |
| T-014 | fretmap: infeasible chord (7 notes on 6 strings) → highest note dropped, count reported | D-008 |
| T-015 | fretmap: capo=2 → no fret < 2 except none; open strings become capo fret | D-008 |
| T-016 | fretmap: bass tuning E1 A1 D2 G2, 4 strings, notes map correctly | A-001 |
| T-017 | beats.grid on 120 BPM click fixture: every beat within 20 ms of truth; downbeats every 4th beat | D-006, C-017 |
| T-018 | beats.grid with < 8 beats and no `--bpm` → exit 3; with `--bpm 100` → constant grid | D-006 |
| T-019 | chords.group: onsets within 30 ms grouped; 31 ms apart not grouped | D-009 |
| T-030 | clean: bass octave suppression removes the +12 ghost when overlap ≥ 70 % and weaker; keeps genuine octave doubles (overlap < 70 %) | D-007, C-006 |
| T-031 | clean: merge rule and min-duration rule | D-007 |
| T-032 | clean: out-of-range handling incl. `--auto-tuning` selecting Drop D for a D2 note; > 1 % dropped → exit 4 | D-007 |

## Integration
| ID | Asserts | Enforces |
|---|---|---|
| T-020 | arrangement.build output validates against the schema extracted in S-001 (`tests/schema/instrumental.xsd`) | C-008, SC-2 |
| T-021 | arrangement: anchors cover every fretted note (note fret within [anchor.fret, anchor.fret+width−1]) | D-009 |
| T-022 | arrangement: every chord references an existing chordTemplate; handShapes cover chord times | D-009 |
| T-023 | Synthetic round-trip: known NoteEvents → Karplus-Strong render (S3 method) → full Python pipeline → onset+pitch F1 ≥ 0.90 guitar, ≥ 0.85 bass (tolerance justified by S3: 0.96 / 0.80 before D-007) | SC-4, C-005, C-006 |
| T-024 | `--review` stops after writing notes.mid, arrangement.xml, pianoroll.png; `--resume-from xml` produces identical job JSON from the unedited XML | D-013 |
| T-025 | rs-pack build with `--audio-wem` fixture (no Wwise) succeeds on the T-023 guitar XML | D-015 |

## Package verification (rs-pack verify; automated proxy for SC-2/SC-3)
| ID | Asserts |
|---|---|
| T-060 | PSARC opens, TOC decrypts (AES-CFB), all entries decompress | C-001 |
| T-061 | Expected entry set present for 1 arrangement (list extracted in S-021) | C-002 |
| T-062 | SNG decrypts (AES-CTR) and parses; max-difficulty note+chord count equals XML counts | C-001, C-009 |
| T-063 | Manifest JSON: DLC key, arrangement name, tuning, song length within 0.5 s of audio length | SC-2 |
| T-064 | First and last note times in SNG within 1 ms of XML | SC-3 |

## Operational / security / performance
| ID | Asserts |
|---|---|
| T-050 | Missing Wwise → exit 11 with actionable message naming supported versions |
| T-051 | Kill during transcription, rerun → resumes from `work/<song>/state.json`, identical outputs (hash) |
| T-052 | Output written atomically (temp + rename); partial files never at final path |
| T-053 | Path traversal in metadata (`--title ../../x`) sanitized; DLC key restricted to `[A-Za-z0-9]{1,32}` |
| T-054 | `pip-audit -r requirements.lock` shows no high/critical in runtime deps (or documented waiver per R7) |
| T-070 | 4-min fixture (synthetic, seeded) end-to-end (excluding Wwise) < 30 min and peak RSS < 4 GB at 4 threads |
| T-071 | Determinism: two runs → byte-identical notes.json and arrangement.xml (excluding provenance timestamp) |
| T-072 | Provenance fields of D-014 present in every result file |

## Offline benchmark (unknown outcome — procedure frozen, value not frozen)
| ID | Asserts |
|---|---|
| T-040 | Benchmark script runs D-012 procedure exactly; fails if held-out split was used during tuning (checks `params.json` tuning log) |
| T-041 | Output `results/benchmark.json` has P, R, F1 per instrument, N notes, provenance |
| T-042 | Validity: every excerpt processed (no silent skips); count equals split size |
| T-043 | Report-only string/fret agreement present for guitar |

## Computational checks N/A for this domain
Observed order of convergence, conservation laws, elevated-precision recompute, CAS cross-checks: N/A (no discretized PDE or closed-form quantity). Replaced by T-023 (code verification on synthetic known answer) and T-071 (reproducibility).
