# Environment

## Python (verified on Linux x86-64 in spike S3)
- CPython **3.11** (tested 3.11.16). 3.12+ unsupported: C-011.
- Lock: `requirements.lock` (SHA-256 `1b3656149c28d02ce57b41c819632aeda8d53e47748ff20241cf2335e20c328a`). Key pins: basic-pitch 0.4.0, tensorflow 2.15.0.post1, numpy 1.26.4, librosa 0.11.0, scipy 1.17.1, resampy 0.4.2, **setuptools 80.10.2 (must stay <81, C-012)**, mir-eval 0.8.2, pretty-midi 0.2.11.post0, soundfile 0.14.0.

Setup (commands executed in spike S3, using uv):
```bash
pip install uv
uv python install 3.11
uv venv -p 3.11 .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
uv pip install -r requirements.lock
python -c "import basic_pitch, tensorflow; print(tensorflow.__version__)"   # expect 2.15.0
```
Dev-only additions (S-004 adds them to `requirements-dev.lock`): pytest, pytest-timeout, hypothesis, pip-audit, matplotlib.

## .NET (NOT yet verified — S-020)
- .NET SDK 10.0.x. Rocksmith2014.NET as git submodule `vendor/Rocksmith2014.NET` pinned to `b87c9a3afd31c40ade9685a9244e718e7581c0cb`.
```bash
git submodule add https://github.com/iminashi/Rocksmith2014.NET vendor/Rocksmith2014.NET
git -C vendor/Rocksmith2014.NET checkout b87c9a3afd31c40ade9685a9244e718e7581c0cb
dotnet build tools/rs-pack -c Release
```
Note: upstream uses central package management (`Directory.Packages.props`) and a custom `nuget.config`; rs-pack must build inside that context or copy both files (S-020 decides, logs in DEVIATIONS.md).

## Wwise (proprietary — requires G-000 acceptance, A-010)
- Any of 2019.x, 2021.x, 2022.x, 2023.x (C-015). Windows: Program Files\Audiokinetic or `WWISEROOT`. macOS: /Applications/Audiokinetic. Linux: Windows build under Wine at `~/.wine/drive_c/Program Files (x86)/Audiokinetic`.
- Installed by the user through the Audiokinetic Launcher with their own account. Never downloaded or redistributed by this project.

## Threads / determinism
- `OMP_NUM_THREADS=4`, `TF_NUM_INTRAOP_THREADS=4`, `TF_NUM_INTEROP_THREADS=1`, `TF_DETERMINISTIC_OPS=1`, `PYTHONHASHSEED=0`, `--seed 0`.
