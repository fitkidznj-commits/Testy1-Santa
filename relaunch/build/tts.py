#!/usr/bin/env python3
"""Offline neural TTS for the Shrimp Shack relaunch VO (sherpa-onnx + piper voice)."""
import sys, os, json
import numpy as np
import soundfile as sf
import sherpa_onnx

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES = os.path.join(ROOT, "voices")

VOICE_DIRS = {
    "female": ("vits-piper-en_US-hfc_female-medium", "en_US-hfc_female-medium.onnx"),
    "male":   ("vits-piper-en_US-ryan-medium", "en_US-ryan-medium.onnx"),
}

def make_tts(voice="female"):
    d, mod = VOICE_DIRS[voice]
    base = os.path.join(VOICES, d)
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=os.path.join(base, mod),
                tokens=os.path.join(base, "tokens.txt"),
                data_dir=os.path.join(base, "espeak-ng-data"),
            ),
            num_threads=4,
            provider="cpu",
        ),
        max_num_sentences=1,
    )
    return sherpa_onnx.OfflineTts(cfg)

def synth(tts, text, path, speed=1.0):
    a = tts.generate(text, sid=0, speed=speed)
    sr = a.sample_rate
    samples = np.asarray(a.samples, dtype=np.float32)
    sf.write(path, samples, sr)
    return len(samples) / sr

if __name__ == "__main__":
    voice = sys.argv[1] if len(sys.argv) > 1 else "female"
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "build", "vo")
    os.makedirs(outdir, exist_ok=True)
    tts = make_tts(voice)
    # Main video VO, warm and gently paced (speed<1 = slower/warmer)
    LINES = {
        "s1": ("Islamorada... your favorite Shrimp Shack is entering a new chapter.", 0.96),
        "s2": ("For years, the Islamorada Shrimp Shack has been known for great seafood, "
               "friendly faces, and that laid-back Keys feeling locals and visitors love.", 1.0),
        "s3": ("Now, local Keys kid David Epstein is taking the helm, "
               "with one simple promise. Keep the heart, keep the flavor, and keep it local.", 0.98),
        "s4": ("The favorites are staying. The famous shrimp fritters, shrimp and grits, "
               "smoked fish dip, fresh catch, conch classics, "
               "and all the Keys comfort food that made the Shack special.", 1.0),
        "s5": ("To our locals... thank you for making the Shack part of Islamorada. "
               "To our visitors... welcome to one of the Keys' favorite seafood stops.", 0.98),
        "s6": ("Come celebrate the next chapter of Islamorada Shrimp Shack, with David Epstein. "
               "Same Shack. Same soul. New chapter.", 0.97),
    }
    meta = {}
    for k, (txt, spd) in LINES.items():
        p = os.path.join(outdir, f"{k}.wav")
        dur = synth(tts, txt, p, speed=spd)
        meta[k] = round(dur, 3)
        print(f"{k}: {dur:.2f}s  {p}")
    json.dump(meta, open(os.path.join(outdir, "durations.json"), "w"), indent=2)
    print("TOTAL VO:", round(sum(meta.values()), 2), "s")
