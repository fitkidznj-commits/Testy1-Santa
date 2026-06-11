#!/usr/bin/env python3
"""Transcribe the source footage with word-level timestamps.

Pipeline:
  1. ffmpeg -> 16 kHz mono wav
  2. ffmpeg silencedetect -> speech regions
  3. sherpa-onnx (Parakeet TDT, word timestamps; Whisper base.en as fallback)
  4. emit transcript.json: [{start, end, text, words: [{w, t0, t1}]}]

Usage: transcribe.py <video> <out_json>
"""
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAKEET = os.path.join(ROOT, "models", "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8")
WHISPER = os.path.join(ROOT, "models", "sherpa-onnx-whisper-base.en")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def extract_wav(video, wav):
    r = run(["ffmpeg", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000",
             "-c:a", "pcm_s16le", wav])
    if r.returncode != 0:
        sys.exit("ffmpeg audio extract failed:\n" + r.stderr[-2000:])


def speech_regions(wav, noise_db="-32dB", min_sil=0.45):
    """Return [(start, end)] speech regions via silencedetect, split to <=28s."""
    r = run(["ffmpeg", "-i", wav, "-af",
             f"silencedetect=noise={noise_db}:d={min_sil}", "-f", "null", "-"])
    log = r.stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", log)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]

    regions, cur = [], 0.0
    for s, e in zip(starts, ends):
        if s - cur > 0.15:
            regions.append((max(0.0, cur - 0.1), min(dur, s + 0.1)))
        cur = e
    if dur - cur > 0.15:
        regions.append((max(0.0, cur - 0.1), dur))

    # split anything > 28 s at its quietest interior point
    out = []
    for s, e in regions:
        while e - s > 28.0:
            out.append((s, s + 25.0))
            s = s + 25.0
        out.append((s, e))
    return out, dur


def load_pcm(wav):
    with wave.open(wav) as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return data.astype(np.float32) / 32768.0, sr


def make_recognizer():
    import sherpa_onnx
    if os.path.isdir(PARAKEET):
        return sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=os.path.join(PARAKEET, "encoder.int8.onnx"),
            decoder=os.path.join(PARAKEET, "decoder.int8.onnx"),
            joiner=os.path.join(PARAKEET, "joiner.int8.onnx"),
            tokens=os.path.join(PARAKEET, "tokens.txt"),
            num_threads=4, model_type="nemo_transducer"), "parakeet"
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=os.path.join(WHISPER, "base.en-encoder.int8.onnx"),
        decoder=os.path.join(WHISPER, "base.en-decoder.int8.onnx"),
        tokens=os.path.join(WHISPER, "base.en-tokens.txt"),
        num_threads=4), "whisper"


def tokens_to_words(tokens, times, offset):
    """Merge BPE tokens (' ' prefix starts a word) into words with t0/t1."""
    words = []
    for tok, t in zip(tokens, times):
        t = float(t) + offset
        new_word = tok.startswith(" ") or tok.startswith("▁") or not words
        text = tok.replace("▁", " ").strip()
        if not text:
            continue
        if new_word:
            words.append({"w": text, "t0": t, "t1": t + 0.15})
        else:
            words[-1]["w"] += text
            words[-1]["t1"] = t + 0.15
    # extend each word's end to next word's start (cap +0.6s)
    for i in range(len(words) - 1):
        words[i]["t1"] = min(words[i + 1]["t0"], words[i]["t0"] + 1.2)
    return words


def main():
    video, out_json = sys.argv[1], sys.argv[2]
    wav = "/tmp/source_16k.wav"
    extract_wav(video, wav)
    regions, dur = speech_regions(wav)
    print(f"duration {dur:.1f}s, {len(regions)} speech regions")
    pcm, sr = load_pcm(wav)

    rec, kind = make_recognizer()
    print("recognizer:", kind)
    segs = []
    for s, e in regions:
        chunk = pcm[int(s * sr):int(e * sr)]
        if len(chunk) < sr // 4:
            continue
        st = rec.create_stream()
        st.accept_waveform(sr, chunk)
        rec.decode_stream(st)
        res = st.result
        text = res.text.strip()
        if not text:
            continue
        words = []
        toks = list(getattr(res, "tokens", []) or [])
        times = list(getattr(res, "timestamps", []) or [])
        if toks and times and len(toks) == len(times):
            words = tokens_to_words(toks, times, s)
        segs.append({"start": round(s, 2), "end": round(e, 2),
                     "text": text, "words": words})
        print(f"[{s:7.2f} - {e:7.2f}] {text}")

    with open(out_json, "w") as f:
        json.dump({"duration": dur, "segments": segs}, f, indent=1)
    print("wrote", out_json)


if __name__ == "__main__":
    main()
