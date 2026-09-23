# Pre-mortem round 1 — author round (NOT independent)

This round was run by the same agent that wrote v2, so it does **not** satisfy Phase 4's
"fresh-context agent that did not author the plan" requirement. Independent rounds are step S-002.

## Scenario A [software]: 6 months after release the tool has failed badly
Incident: users on Windows install fine but every package crashes the game on load. Root cause: rs-pack built
packages with an arrangement the upstream checker accepted but the game rejects (e.g. missing anchors in a DD level
created by the DD generator from our single level). Automated verify passed because it only compared counts.
→ R-001. Mitigation: G-002 on three songs incl. a real stem; R3 diff against DLC Builder-built reference; T-021 anchors.

Incident: new Python/TensorFlow machines can't install. basic-pitch pins tensorflow<2.15.1; Python 3.11 reaches EOL
Oct 2027. → R-002. Mitigation: A-013 documented; S-004 CI matrix; ONNX backend evaluated as a later option (Medium, residual).

Incident: Wwise version changes break conversion. → R-003. Mitigation: `--audio-wem` bypass; supported versions from C-015.

## Scenario B [computational]: 12 months later results can't be reproduced
Incident: benchmark F1 differs by 0.03 on another machine. Root cause: TF nondeterminism + unpinned dataset version.
→ R-004. Mitigation: D-014 provenance, TF_DETERMINISTIC_OPS, dataset record version/DOI in SOURCES (S-001), T-071.

Incident: held-out split was peeked at during tuning. → R-005. Mitigation: T-040 checks tuning log; G-001 burn rule.

## Lens notes
- Integrity: v1 fabricated verification; v2 claims all trace to committed spikes or are marked unverified.
- Supply chain: submodule pinned by commit; lock hashed in ENVIRONMENT.md.
- Security: local files only; T-002, T-053; Wwise invoked with arguments, no shell string.
- Scale: basic-pitch CPU time in S3 ~ real time; 30-min budget has large margin (T-070 confirms).
- Implementer misinterpretation: interfaces and exit codes fixed in DECISIONS.md; cold read in S-002.
