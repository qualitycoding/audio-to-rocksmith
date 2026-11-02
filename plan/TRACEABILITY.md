# Traceability

| Req | Statement | Tests | Steps | Gate |
|---|---|---|---|---|
| SC-1 | One command produces a PSARC from a guitar or bass stem | T-001, T-002, T-023, T-025 | S-011..S-024 | — |
| SC-2 | PSARC loads in RS2014 Remastered PC | T-020, T-060..T-063 (proxy) | S-021, S-023 | G-002 |
| SC-3 | Chart aligned with audio | T-017, T-064 (proxy) | S-013, S-023 | G-002 |
| SC-4 | Transcription accuracy target F1 ≥ 0.70 (offline) | T-023 (synthetic), T-040..T-043 | S-010 | G-001 |
| NFR-1 | < 30 min / 4 GB per 4-min song, 4 threads | T-070 | S-025 | — |
| NFR-2 | Deterministic, provenance recorded | T-071, T-072 | S-011 | — |
| NFR-3 | Safe local file handling | T-002, T-052, T-053, T-054 | S-011, S-025 | — |
| NFR-4 | Playable fingering | T-010..T-016 | S-016 | G-002 |
| NFR-5 | Resumable | T-024, T-051 | S-019 | — |

Every T-### above maps to a requirement; T-003, T-019, T-021, T-022, T-030..T-032, T-050 map to decisions D-002, D-007, D-009, D-010 supporting SC-1/NFR-4.

## v3.9 addendum traceability (2026-11-02)

| Requirement | Artifact | Step | Verification |
|---|---|---|---|
| Gap ledger per planning root | `plan/ADDENDUM-V3.9-GAP.md` | S-ADD-001 | `v39_addendum_verify.py final` |
| Planning-only scope freeze | D-900 in `plan/DECISIONS.md` | S-ADD-001 | verifier + retrospective |
| Mutation three-tier priced CI, aggregator, report score gate | `reviews/MUTATION.md` | S-ADD-080 | verifier + first CI run (pending in CI) |
| Split lesson/knowledge stores | G-003 in `plan/GATES.md`, `.checkpoints/state.json` | S-ADD-010/S-ADD-060 | verifier |
| Full-context checkpoints / zero-context resume | `.checkpoints/state.json` | S-ADD-020 | verifier |
| Assumption audit, reviews | `premortem/ASSUMPTION_AUDIT.md`, `reviews/` | S-ADD-030 | verifier |
| Honest verification, deviations | `DEVIATIONS.md`, `EXECUTION_LOG.md` | S-ADD-040 | verifier |
| Ephemeral protections | `plan/ENVIRONMENT.md` | S-ADD-050 | verifier |
| CI platform matrix | `plan/CI-MATRIX.md` | S-ADD-070 | cold read |
| Cold read / pre-mortem | this file, `premortem/RISK_REGISTER.md` | S-ADD-090 | verifier |
