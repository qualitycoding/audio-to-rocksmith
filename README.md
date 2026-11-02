# audio-to-rocksmith

A planned command-line tool that turns an isolated guitar or bass stem (WAV, FLAC or OGG) into a
Rocksmith 2014 Remastered PC custom song (`*_p.psarc`).

> **Status: planning only. There is no code in this repository yet.** Nothing here can be run.
> The plan is blocked at human gate **G-000** (scope acceptance), and the step plan says not to start
> implementation until that decision is recorded. The frozen test suite has not been written either.

## What is here

This branch holds the revised plan (v2) and its supporting evidence, not an implementation:

| Path | Contents |
|---|---|
| `HANDOFF.md` | Start here: purpose, reading order, gates and the halt rules |
| `plan/` | The plan (`PLAN.md`, steps S-000 to S-026), design decisions, assumptions, gates, environment, traceability, and `REVIEW.md` (what was wrong with plan v1) |
| `tests/SPEC.md` | The 39 planned tests (specified, not yet written or frozen) |
| `research/` | Claims register, sources, research rounds and three small spikes (Python dependency resolution, Rocksmith2014.NET inspection, basic-pitch on synthetic audio) |
| `premortem/` | Risk register and the author's first pre-mortem round |
| `reviews/` | Adversarial review, code review and mutation notes |
| `requirements.lock` | The Python dependency set that resolved in the spikes |

## Planned design

The tool is a Python 3.11 package with a CLI called `a2rs`, plus a thin .NET console tool called
`rs-pack`. The pipeline is: decode the stem, transcribe notes (Spotify's basic-pitch), clean them,
find the beat grid (librosa), group chords, map notes to string and fret with a Viterbi search, write
the Rocksmith arrangement XML, then convert audio to Wwise and pack the PSARC.

```
a2rs STEM --instrument {guitar,bass} [--tuning E] [--capo 0] [--max-fret 22|24]
     [--bpm N] [--first-beat SEC] [--time-signature 4/4] [--auto-tuning]
     [--artist A --title T --album B --year Y --art PNG] [--preview-start SEC]
     [--review] [--resume-from {transcribe,xml}] [--out DIR] [--work DIR] [--seed 0]
```

This is the interface in `plan/DECISIONS.md` (D-011); it describes intended behaviour and may change.
`--review` stops after writing a MIDI file, the arrangement XML and a piano-roll image so you can fix
the transcription before packing.

## Planned requirements

- Python 3.11 only. basic-pitch cannot be installed on Python 3.12 (spike S1/S3).
- .NET 10 and [Rocksmith2014.NET](https://github.com/iminashi/Rocksmith2014.NET) (MIT) for packaging.
- Audiokinetic **Wwise**, installed by the user with their own account, for audio conversion. It is
  proprietary and is the one exception to the open-source-only rule; accepting it is part of G-000.
  CI cannot run Wwise, so it would use a small pre-converted `.wem` fixture.

## Human gates

| Gate | Decision |
|---|---|
| G-000 | Accept the scope: Wwise, .NET 10 and Python 3.11 only |
| G-001 | Accept the offline accuracy benchmark result (GuitarSet and Slakh2100, note-onset F1) |
| G-002 | In-game acceptance in Rocksmith |

## Related projects

- [Rawksmyth](https://github.com/qualitycoding/Rawksmyth): a Rocksmith-style guitar learning game.
- [audio-to-midi](https://github.com/qualitycoding/audio-to-midi): a browser app that turns stems into MIDI and tab.

## Licence

No licence file has been added yet.
