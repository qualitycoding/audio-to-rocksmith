# HANDOFF — audio-to-rocksmith

**Status: BLOCKED — HUMAN DECISION REQUIRED at G-000.** Do not start S-001 until plan/GATE_LOG.md records G-000.

## Purpose
CLI that turns an isolated guitar or bass stem (WAV/FLAC/OGG) into a Rocksmith 2014 Remastered PC custom song (`*_p.psarc`).

## Active profiles
software, computational (plan/PROFILE.md).

## Reading order
1. plan/REVIEW.md — why v1 was replaced
2. plan/PROFILE.md, plan/ASSUMPTIONS.md
3. plan/DECISIONS.md — interfaces, algorithms, decision rules
4. plan/PLAN.md — steps S-000..S-026
5. plan/GATES.md, plan/ENVIRONMENT.md, plan/TRACEABILITY.md
6. tests/SPEC.md
7. research/claims.json, research/SOURCES.md, research/rounds/, research/spikes/
8. premortem/

## Environment
plan/ENVIRONMENT.md. Python 3.11 + `requirements.lock`; .NET 10; Wwise (user-installed).

## Running the frozen suite
Not yet frozen. After S-003: `pytest -q` and `sha256sum -c tests/FROZEN_MANIFEST.sha256`.

## Step list
See header of plan/PLAN.md.

## Human gates
G-000 scope acceptance · G-001 accuracy result · G-002 in-game acceptance (plan/GATES.md).

## Halt / deviation protocol
Follow decision rules R1–R8 and the Default rule in plan/DECISIONS.md. Log every deviation in DEVIATIONS.md.
Halt and write BLOCKED.md for anything touching frozen tests, security, data integrity, a public interface, or integrity.

## Integrity rule (verbatim)
No fabrication, cherry-picking, or manual alteration of data, test results, or figures. Every reported number is generated from committed results.
