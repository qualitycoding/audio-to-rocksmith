# Decisions, interfaces and decision rules

## Architecture (D-001)
Two components in one repo:
1. `a2rs/` — Python 3.11 package + CLI `a2rs`: decode → transcribe → clean → beat grid → chords → fret map → arrangement XML → project JSON.
2. `tools/rs-pack/` — .NET 10 F# console app referencing Rocksmith2014.NET (git submodule pinned at `b87c9a3a`): validate XML, generate phrases/DD, convert audio (Wwise), build PC PSARC, verify PSARC.

Python calls `rs-pack` as a subprocess with a JSON job file; no in-process .NET interop.

```
stem.wav/flac/ogg ─▶ a2rs ─▶ work/<song>/{notes.json, arrangement.xml, project.json, notes.mid, pianoroll.png}
                                 └──▶ rs-pack build project.json ─▶ out/<song>_p.psarc
                                 └──▶ rs-pack verify out/<song>_p.psarc arrangement.xml
```

## Public interfaces (stubs raise NotImplementedError until implemented)

### D-002 Canonical note data
```python
@dataclass(frozen=True)
class NoteEvent:
    onset: float        # seconds, >= 0
    offset: float       # seconds, > onset
    midi: int           # 0..127
    velocity: float     # 0..1 (basic-pitch amplitude)
    bend_cents: tuple[float, ...] = ()  # optional pitch-bend track, may be empty

@dataclass(frozen=True)
class FretNote:
    event: NoteEvent
    string: int         # 0 = lowest string
    fret: int           # 0..max_fret
```
Serialized as `notes.json` with a `provenance` object (D-014).

### Module functions
| Function | Signature | Notes |
|---|---|---|
| `a2rs.audio.load` | `(path: Path) -> tuple[np.ndarray, int]` | mono float32, original SR; rejects non WAV/FLAC/OGG, > 20 min, silent input |
| `a2rs.transcribe.run` | `(audio, sr, instrument, params) -> list[NoteEvent]` | wraps basic-pitch `predict` with instrument ranges (D-005) |
| `a2rs.clean.run` | `(events, instrument) -> list[NoteEvent]` | merge, min duration, bass octave suppression (D-007) |
| `a2rs.beats.grid` | `(audio, sr, bpm=None, first_beat=None, ts=(4,4)) -> BeatGrid` | D-006 |
| `a2rs.chords.group` | `(events, window=0.030) -> list[list[NoteEvent]]` | onset clustering |
| `a2rs.fretmap.solve` | `(groups, tuning, max_fret, capo=0, weights=DEFAULT) -> list[list[FretNote]]` | D-008 |
| `a2rs.arrangement.build` | `(fretted, grid, tuning, meta) -> ET.Element` | D-009 |
| `a2rs.project.write` | `(xml_path, audio_path, meta, out) -> Path` | job JSON for rs-pack |
| `a2rs.cli.main` | `argv -> int` exit code | D-011 |
| `rs-pack build <job.json>` | exit 0 + psarc path on stdout | D-010 |
| `rs-pack verify <psarc> <xml>` | exit 0 iff checks in T-060..T-064 pass; JSON report on stdout | |

## D-003 Packaging library
Rocksmith2014.NET, not RSTK. Reasons: maintained (2026 commits), MIT, headless library API, cross-platform, DD/phrase/checker included (C-003, C-004). RSTK rejected: GUI-centric, Wwise 2013 (C-016).

## D-004 Python environment
CPython 3.11; lock in `requirements.lock` generated from the S3 freeze; `setuptools<81` pinned (C-011, C-012).

## D-005 Transcription parameters (initial; tuned only on the tuning split in S-010)
| | guitar | bass |
|---|---|---|
| minimum_frequency (Hz) | 70 | 35 |
| maximum_frequency (Hz) | 1400 | 450 |
| onset_threshold | 0.5 | 0.5 |
| frame_threshold | 0.3 | 0.3 |
| minimum_note_length (ms) | 58 | 80 |
Tuned values are written to `a2rs/params.json` with the tuning-split F1; the held-out split is evaluated **once** with the tuned values.

## D-006 Beat grid
librosa `beat_track` on the stem → beat times; bar numbers from `--time-signature` and first downbeat (`--first-beat` or first detected beat). If inter-beat-interval coefficient of variation > 0.08 → warn "unsteady tempo"; still emit (Rocksmith ebeats may vary). If fewer than 8 beats detected → fall back to constant grid at `--bpm` (required then; exit code 3 if absent).

## D-007 Cleaning rules
- Merge same-pitch events whose gap < 30 ms.
- Drop events shorter than the instrument minimum.
- Bass octave suppression: drop event E if another event F with F.midi = E.midi − 12 overlaps ≥ 70 % of E's duration and E.velocity < F.velocity. (Motivated by C-006; verified by T-030.)
- Notes outside the tuning's playable range: if below lowest open string by 1–2 semitones and `--auto-tuning` → choose the drop/down tuning that fits; else drop and count. If dropped fraction > 1 % → exit code 4 with message.

## D-008 Fret mapping (Viterbi)
States for a chord group = all assignments of its notes to **distinct** strings with frets in [capo, max_fret]; span = max(fretted) − min(fretted) ≤ `max_span` (guitar 4, bass 4), open strings excluded from span. Cost of a state: `w_pos·mean_fret + w_span·span + w_open·(−open_count)`; transition cost: `w_move·|centroid_t − centroid_{t−1}| + w_str·string_jumps`. Defaults `w_pos=0.2, w_span=1.0, w_open=0.3, w_move=1.0, w_str=0.2` (to be tuned against GuitarSet string labels in S-010, report-only). If a group has no feasible state → drop the highest-pitched note of the group and retry; count drops. Guarantees: every output note on a real (string, fret) with correct pitch (T-010); no two notes of a chord share a string (T-011); span constraint holds (T-012).

## D-009 Arrangement construction
- ebeats from D-006, measure numbers on downbeats.
- Anchors: one anchor per phrase iteration at min fretted fret (≥1), width 4; new anchor whenever a note falls outside current anchor window.
- Chords: chordTemplates deduplicated by (fret-tuple); handShapes span chord duration.
- Phrases/sections: generated by Rocksmith2014.NET PhraseGenerator in rs-pack; COUNT and END phrases enforced.
- Single max-difficulty level from Python; DD levels generated by Rocksmith2014.NET DD generator in rs-pack.
- Pitch bends: if |bend| ≥ 50 cents sustained ≥ 60 ms → bend technique (bend value in semitones, rounded to 0.5); else ignored.
- Tone: single default clean tone per instrument.

## D-010 rs-pack pipeline
load job → XML load → ArrangementChecker (errors fail, warnings logged) → PhraseGenerator if no phrases → DD generator → Wwise conversion (main + 28 s preview starting at `--preview-start` or 30 % of length) → DLCProject → buildPackages(PC) → write `_p.psarc`. Exit codes: 0 ok, 10 checker error, 11 Wwise not found, 12 Wwise failed, 13 build failed.

## D-011 CLI
```
a2rs STEM --instrument {guitar,bass} [--tuning E] [--capo 0] [--max-fret 22|24]
     [--bpm N] [--first-beat SEC] [--time-signature 4/4] [--auto-tuning]
     [--artist A --title T --album B --year Y --art PNG] [--preview-start SEC]
     [--review] [--resume-from {transcribe,xml}] [--out DIR] [--work DIR] [--seed 0]
```
Exit codes: 0 ok; 2 bad input; 3 beat grid failure; 4 range failure; 5 no notes; 6 rs-pack failure (propagates its code in the message); 7 quality proxy hard-fail (D-013).

## D-012 Offline accuracy benchmark (development only)
- Guitar: GuitarSet, mono mic audio. Tuning split players 00–04; held-out player 05 (60 excerpts).
- Bass: Slakh2100 test split, bass stems (first 100 tracks by ID, sorted), rendered stems as provided.
- Metric: `mir_eval.transcription.precision_recall_f1_overlap`, onset tolerance 50 ms, pitch tolerance 50 cents, `offset_ratio=None`; micro-average over all notes of the split.
- Secondary (report-only): string/fret agreement on GuitarSet among correctly-matched notes.
- Target (A-004): F1 ≥ 0.70 per instrument. Value recorded at G-001, not frozen.

## D-013 Runtime quality proxies (no ground truth at runtime)
Computed per song and written to `report.json`:
- note density (notes/s): warn if > 12 (guitar) / > 8 (bass); hard-fail if > 25.
- fraction of events with velocity < 0.2: warn if > 0.3.
- dropped-note fraction from D-007/D-008: warn if > 0.02.
Warn → message + continue. Hard-fail → exit 7 unless `--force`. With `--review`, the tool stops after writing `notes.mid`, `arrangement.xml`, `pianoroll.png`; `--resume-from xml` continues from a user-edited XML (edited in any editor, e.g. EOF or DLC Builder).

## D-014 Provenance
Every `notes.json`, `report.json` and benchmark result embeds: git commit, `requirements.lock` SHA-256, seed, all CLI parameters, UTC timestamp, hostname-free hardware string (`platform.machine()`, CPU count), `OMP_NUM_THREADS`, basic-pitch and rs-pack versions.

## D-015 Wwise in CI
CI (Linux) cannot run Wwise. rs-pack supports `--audio-wem PATH` to accept a pre-converted WEM; CI uses a small committed WEM fixture produced once on a developer machine at S-022 and recorded with its SHA-256. If S-022 fails on all hosts → fallback: rs-pack writes a `.rs2dlc` project for manual build in DLC Builder (C-014), and success criterion 1 is downgraded — requires human decision (BLOCKED).

## Decision rules for the implementer (if → then)
| # | If | Then |
|---|---|---|
| R1 | rs-pack cannot build against pinned Rocksmith2014.NET | Try the nearest later upstream commit that builds; record in DEVIATIONS.md. If none within 10 commits → BLOCKED.md |
| R2 | ArrangementChecker reports an error on generated XML | Fix generator; never suppress checker errors via IgnoredIssues |
| R3 | T-060..T-064 pass but G-002 in-game load fails | Diff the package against a known-good reference built by DLC Builder from the same XML; fix; re-run G-002 |
| R4 | Held-out F1 < 0.50 | G-001 decision: stop, or evaluate alternative model (research spike) |
| R5 | 0.50 ≤ F1 < 0.70 | G-001 decision: ship with documented accuracy, or iterate |
| R6 | F1 ≥ 0.70 | Record at G-001; proceed |
| R7 | Dependency CVE (pip-audit) high/critical in a runtime dep | Upgrade within lock if compatible; else document and escalate |
| R8 | Any frozen test believed wrong | Do not edit; write BLOCKED.md with evidence (Test Challenge Rule) |
| Default | Anything else | Most reversible option not expanding scope; log in DEVIATIONS.md; halt instead if it touches frozen tests, security, data integrity, a public interface or integrity |

## Addendum v3.9 decisions (2026-11-02)

- **D-900** — Planning-only amendment. Product scope, public interfaces,
  expected test behaviour, performance targets and human gates do not change,
  except the mandatory split G-003 lesson/knowledge store semantics.
- **D-901** — Source-branch drift: the planning source branch tip `d54b607bd37a`
  is the rollout phase's `plan: add protocol v3.9 addendum` commit, a direct
  child of the audited source commit `065504cf5d8a`. The implementation
  branch therefore descends from `d54b607bd37a`, which itself descends from the
  audited commit; no newer planning was overwritten or rebased away.
- **D-902** — No platform expansion: no new OS/architecture/runtime support is
  claimed; CI coverage is recorded as plan-level jobs/waivers only.
- **D-903** — No release, deployment or package publication is authorised or
  planned by this amendment.
- **D-904** — Ambiguities resolved from existing plan artifacts and repository
  evidence only; defaults follow the addendum's no-added-platform / explicit
  waiver rule.
- **D-905** — Local build and test execution is not available in the ephemeral
  sandbox; the CI matrix jobs added to the plan are the authoritative execution
  venue (honest-verification substitution, see DEVIATIONS.md).
- **D-906** — Fresh-context independent review is unavailable in this
  environment; the cold read is recorded as a substitution with High risk
  (S-ADD-090), not claimed as an independent pass.
- **D-980** — Mutation testing design: see `reviews/MUTATION.md` (priced
  three-tier trigger strategy, one aggregator job, report-based score gate).
