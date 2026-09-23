"""Spike S3: does basic-pitch 0.4.0 recover known notes from synthetic plucked strings
in guitar and bass registers? Deterministic (seed 0). NOT a benchmark: synthetic
Karplus-Strong tones only. Real-audio accuracy is measured in S-010 (GuitarSet/Slakh).
Usage: python research/spikes/S3-basic-pitch-synthetic/run.py"""
import json, time, platform, os, numpy as np, soundfile as sf, mir_eval
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

SR = 44100
rng = np.random.default_rng(0)
OUT = os.path.dirname(os.path.abspath(__file__))

def ks(freq, dur, sr=SR, decay=0.996):
    n = int(dur * sr); p = int(round(sr / freq))
    buf = rng.uniform(-1, 1, p); out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out

def render(notes, total):
    y = np.zeros(int(total * SR))
    for on, off, midi in notes:
        s = ks(440 * 2 ** ((midi - 69) / 12), off - on); i = int(on * SR)
        y[i:i + len(s)] += 0.3 * s
    return y / max(1e-9, np.abs(y).max()) * 0.8

cases = {
  # single notes E2..E4 + an E-major chord at t=4.0
  "guitar": ([(0.5*k, 0.5*k+0.45, m) for k, m in enumerate([40, 45, 50, 55, 59, 64, 52, 57])]
             + [(4.0, 5.0, m) for m in (40, 47, 52, 56)], 5.5, 70, 1400),
  # bass E1..G2 single notes
  "bass":   ([(0.5*k, 0.5*k+0.45, m) for k, m in enumerate([28, 33, 38, 43, 31, 36, 40, 45])], 4.5, 35, 450),
}
report = {"python": platform.python_version(), "seed": 0}
for name, (notes, total, fmin, fmax) in cases.items():
    wav = os.path.join(OUT, f"{name}.wav"); sf.write(wav, render(notes, total), SR)
    t0 = time.time()
    _, midi, events = predict(wav, ICASSP_2022_MODEL_PATH, minimum_frequency=fmin, maximum_frequency=fmax)
    dt = time.time() - t0
    ref_i = np.array([[a, b] for a, b, _ in notes]); ref_p = np.array([440*2**((m-69)/12) for *_, m in notes])
    est_i = np.array([[e[0], e[1]] for e in events]) if events else np.zeros((0, 2))
    est_p = np.array([440*2**((e[2]-69)/12) for e in events]) if events else np.zeros(0)
    p, r, f, _ = mir_eval.transcription.precision_recall_f1_overlap(ref_i, ref_p, est_i, est_p,
                    onset_tolerance=0.05, pitch_tolerance=50.0, offset_ratio=None)
    report[name] = {"ref_notes": len(notes), "est_notes": len(events), "precision": round(p, 3),
                    "recall": round(r, 3), "f1_onset_pitch": round(f, 3), "seconds": round(dt, 2),
                    "est_pitches": sorted(int(e[2]) for e in events)}
    os.remove(wav)
json.dump(report, open(os.path.join(OUT, "result.json"), "w"), indent=1)
print(json.dumps(report, indent=1))
