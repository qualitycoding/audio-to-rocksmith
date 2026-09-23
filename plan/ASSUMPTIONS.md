# Assumptions (A-###)

Intake batch from v1 was never answered by the human; defaults below are adopted and marked.
Items marked **GATE** must be confirmed at G-000 before any implementation step runs.

| ID | Assumption | Status | Consequence |
|---|---|---|---|
| A-001 | Support guitar (6-string) and bass (4-string) via `--instrument {guitar,bass}`. 7-string guitar / 5-string bass out of scope for v1. | default | Two tuning tables, one mapper |
| A-002 | Canonical intermediate is `NoteEvent` JSON (D-002). MIDI written as a side output only. | default (changed from v1) | No string/fret loss |
| A-003 | Packaging uses Rocksmith2014.NET @ `b87c9a3a` via in-repo `tools/rs-pack` (.NET 10). RSTK not used. | **GATE** | Adds .NET 10 SDK dependency |
| A-004 | Offline accuracy target: note-onset+pitch F1 ≥ 0.70 on the held-out benchmark (D-012). This is a target, not a frozen expected value. | default | Recorded at G-001 |
| A-005 | End-user runtime review is optional (`--review`), not a development gate. | default (changed from v1) | Tool stays fully automatic by default |
| A-006 | Input is a pre-isolated stem. Source separation (Demucs) is out of scope and not a dependency. | default | Mixed input → garbage out; warned, not blocked |
| A-007 | Target game: Rocksmith 2014 Remastered, PC package (`*_p.psarc`). Mac package and RS+ out of scope. | default | Single platform build |
| A-008 | Tool host OS: Windows 10+, macOS 13+, Linux x86-64. On Linux the Wwise step runs under Wine (upstream behaviour, C-015). | default | Linux CI cannot run Wwise; see D-015 |
| A-009 | Time signature default 4/4; override with `--time-signature N/D`. Tempo from beat tracking; override `--bpm` and `--first-beat`. | default | Odd meters need override |
| A-010 | Wwise (proprietary, Audiokinetic account required) is accepted as the **sole** non-open-source dependency, installed by the user, versions 2019/2021/2022/2023 (C-015). Not redistributed. | **GATE** | Violates original "open-source only" constraint unless accepted |
| A-011 | Tuning default E standard (A440); `--tuning` accepts names (`E`, `Eb`, `DropD`, `D`) or six/four MIDI numbers. | default | |
| A-012 | Metadata (artist, title, album, year) via CLI flags with defaults derived from filename; album art optional (a generated placeholder is used). | default | |
| A-013 | Python 3.11 (C-011). | default | Python 3.12+ unsupported until basic-pitch relaxes its tensorflow pin |
| A-014 | Benchmark data (GuitarSet, Slakh2100) is downloaded by the implementer for evaluation only; never committed or shipped. | default | Licence compliance (C-020, C-021 to verify) |
