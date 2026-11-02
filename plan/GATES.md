# Human gates (development)

| Gate | When | Implementer provides | Human options |
|---|---|---|---|
| **G-000** Scope acceptance | Before S-001 | plan/REVIEW.md, A-003, A-010, A-013 | `proceed` (accept Wwise exception, .NET 10, Py 3.11) · `proceed-with-changes: <text>` · `stop` |
| **G-001** Accuracy result | After S-010 | `results/benchmark.json` (held-out F1 per instrument, P/R, string agreement, provenance), 5 random held-out piano-rolls per instrument (seeded) | `proceed` · `iterate: <direction>` (returns to S-010 with a new research spike; held-out split is then burned → new held-out from GuitarSet player 04 recorded in DEVIATIONS.md) · `stop` |
| **G-002** In-game acceptance | After S-024 | 3 PSARCs (guitar fixture, bass fixture, one user-chosen real stem), `verify` reports, loading instructions (copy to `Rocksmith2014/dlc/`, CDLC enabler installed) | Per song: loads Y/N, chart synced to audio within ~1 beat Y/N, playable Y/N → `proceed` (tag release candidate) · `fix: <notes>` · `stop` |

Runtime review for end users is a CLI feature (`--review`, D-013), not a gate.

## G-003 — split learning stores (v3.9)

Lessons and knowledge are pushed to **separate** stores: the `Lessons`
repository and the `knowledge` repository. G-003 requests the destinations at
plan close; **do-not-push** either store until human sign-off; the documented
bundle fallback applies when sign-off is withheld. Store publication never holds
up the repository amendment's completion record.
