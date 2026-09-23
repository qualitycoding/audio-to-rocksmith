# Sources

| Key | Source | Tier | Verification note |
|---|---|---|---|
| SRC-RSNET | github.com/iminashi/Rocksmith2014.NET @ b87c9a3afd31c40ade9685a9244e718e7581c0cb (2026-03-13) | 1 (source) | Cloned and inspected, spike S2 |
| SRC-BP | pypi.org/project/basic-pitch 0.4.0 (uploaded 2024-08-16), requires_dist metadata | 1 | Installed and executed on Python 3.11.16, spike S3 |
| SRC-PYPI | PyPI JSON API for librosa, mir_eval, numpy, scipy, pretty_midi, soundfile, madmom | 1 | Queried 2026-09-23 |
| SRC-DLCB | cfmanager.customsforge.com/tools/DLCBuilder (DLC Builder v3.5.0) | 3 | Read 2026-09-23 |
| SRC-RSTK | github.com/rscustom/rocksmith-custom-song-toolkit releases (latest tag seen 2.9.0.0) | 2 | Read 2026-09-23; used only to reject RSTK |
| SRC-CF66838 | customsforge.com topic 66838 (RSTK needs Wwise 2013) | 4 | Single forum source; not load-bearing |
| SRC-MIREVAL | mir_eval 0.8.2 transcription module | 1 | Executed in S3 |
| SRC-GUITARSET | GuitarSet (Xi et al., ISMIR 2018), Zenodo record | 1 | **Not yet opened** – S-001 |
| SRC-SLAKH | Slakh2100 (Manilow et al., WASPAA 2019), Zenodo record | 1 | **Not yet opened** – S-001 |

Note: madmom 0.16.1 was considered for beat tracking and rejected: its model files are CC BY-NC-SA (PyPI licence field) and its last release predates Python 3.11.
