# Question tree (status after round 1)

- Q1 Packaging
  - Q1.1 Which maintained library builds RS2014 PC packages headlessly? → Rocksmith2014.NET (C-003, C-004) ✅
  - Q1.2 Exact PSARC entry list for a PC song (C-002) ⏳ S-021
  - Q1.3 Exact instrumental XML schema (C-008) ⏳ S-001
  - Q1.4 Can buildPackages run without the DLC Builder GUI? ⏳ S-020 (expected yes: library code)
- Q2 Audio
  - Q2.1 Any open-source WEM encoder? → none known; Wwise required (A-010, C-015) ✅ pending human acceptance
  - Q2.2 Does Wwise conversion work under Wine on Linux in CI? ⏳ S-022 (D-015 fallback)
- Q3 Transcription
  - Q3.1 Installable, pinned environment → Py 3.11 lock (C-011, C-012) ✅
  - Q3.2 Accuracy on real guitar/bass (unknown outcome) ⏳ S-010 → G-001
  - Q3.3 Bass octave errors (C-006) ✅ observed; mitigation D-007
- Q4 Arrangement
  - Q4.1 Beat grid from audio (C-017) ⏳ T-017
  - Q4.2 Fret mapping algorithm (C-007) ✅ design, ⏳ tests
  - Q4.3 Phrases/sections/DD generation reuse (C-003) ✅ design
- Q5 Evaluation data licences (C-020, C-021) ⏳ S-001
