# Risk register (after author round 1 — independent rounds pending, S-002)

| ID | Description | Lens | Sev | Lik | Root cause / trace | Mitigation | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Packages pass automated verify but fail in-game | technical | High | Med | C-002, C-008 unverified; S-021 | G-002 (3 songs), R3 reference diff, T-020..T-022 | mitigated |
| R-002 | basic-pitch TF pin strands users on Python 3.11 | supply chain | Medium | High | C-011 | A-013 documented; CI matrix S-004; ONNX evaluation deferred | residual |
| R-003 | Wwise unavailable/changes; Linux via Wine flaky | supply chain | High | Med | A-010, C-015 | `--audio-wem` bypass, D-015 fallback, T-050 | mitigated |
| R-004 | Benchmark not reproducible | reproducibility | Medium | Med | TF nondeterminism, dataset versions | D-014, env vars, T-071, dataset DOIs (S-001) | mitigated |
| R-005 | Held-out contamination | integrity | High | Low | S-010 | T-040 tuning-log check, G-001 burn rule | mitigated |
| R-006 | Slakh bass is synthetic → overstates real bass accuracy | invalid assumption | Medium | High | C-021 | Report as synthetic in G-001; real bass stem in G-002 | residual |
| R-007 | Real stems with effects/distortion transcribe poorly (F1 below target) | numerical validity | Medium | High | GuitarSet is clean acoustic | Documented limitation; `--review` mode; G-001 decision | residual |
| R-008 | Beat tracking wrong on rubato/odd meter → chart drifts | technical | Medium | Med | C-017 | `--bpm/--first-beat/--time-signature` overrides; unsteady-tempo warning | residual |
| R-009 | Frozen tests depend on still-unverified schema | integrity | High | Med | C-008 | Freeze only after S-001 extracts schema (S-003 depends on S-001 via S-002) | mitigated |
| R-010 | Plaintext GitHub token pasted in chat is reused | security | Low | High | planning session | Revoke token; use a fine-grained, repo-scoped, short-expiry token | open (human) |

## v3.9 addendum risk round (2026-11-02)

| Risk | Severity | Mitigation | Status |
|---|---|---|---|
| No independent fresh-context review (D-906) | High | Recorded substitution; independent review scheduled before product execution resumes | Open |
| CI-dependent checks (mutation pricing/floor, matrix jobs) not locally executable (D-905) | Medium | CI is the authoritative venue; estimates labelled; post-conditions gate in CI | Open |
| Lesson/knowledge store push pending G-003 sign-off | Low | Bundle fallback documented; does not block amendment completion | Open |

Pre-mortem rounds repeated to zero Critical risks; High risk retained honestly
with owner and mitigation.
