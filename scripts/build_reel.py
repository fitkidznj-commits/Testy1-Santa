#!/usr/bin/env python3
"""Assemble the Take Down Charters reel from an edit decision list.

Usage: build_reel.py <source_video> <edit.json> <out.mp4>

edit.json schema:
{
  "fps": 30,
  "width": 1920, "height": 1080,
  "crop": null | {"w":..,"h":..,"x":..,"y":..},   # source-space crop before scale
  "clips": [
    {"start": 12.3, "end": 17.8, "zoom": "in"|"out"|"none"}
  ],
  "captions": [
    {"t0": 0.4, "t1": 1.2, "text": "WE'RE OUT HERE"}    # output-timeline seconds
  ],
  "endcard": {"duration": 4.0, "freeze_from_end": false},
  "loudnorm": "I=-14:TP=-1.5:LRA=11"
}

The end card extends the final clip's last frame (or keeps motion), dims it,
and fades in assets/brand/endcard.png. Watermark overlays the talking section.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "assets", "brand")
FONTS = os.path.join(ROOT, "assets", "fonts")


def ass_time(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_ass(captions, path, W, H):
    margin_v = int(H * 0.14)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Archivo Black,68,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,0,0,0,0,100,100,1,0,1,4,2,2,80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for c in captions:
        text = c["text"].replace("\n", "\\N")
        lines.append(
            f"Dialogue: 0,{ass_time(c['t0'])},{ass_time(c['t1'])},Cap,,0,0,0,,{text}")
    with open(path, "w") as f:
        f.write(header + "\n".join(lines) + "\n")


def main():
    src, edit_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    cfg = json.load(open(edit_path))
    W, H, FPS = cfg.get("width", 1920), cfg.get("height", 1080), cfg.get("fps", 30)
    clips = cfg["clips"]
    ec = cfg.get("endcard", {"duration": 4.0})
    ec_dur = float(ec.get("duration", 4.0))

    talk_dur = sum(c["end"] - c["start"] for c in clips)
    total = talk_dur + ec_dur
    print(f"talking {talk_dur:.2f}s + endcard {ec_dur:.2f}s = {total:.2f}s")

    ass_path = "/tmp/captions.ass"
    write_ass(cfg.get("captions", []), ass_path, W, H)

    crop = cfg.get("crop")
    pre = (f"crop={crop['w']}:{crop['h']}:{crop['x']}:{crop['y']}," if crop else "")
    base_scale = f"{pre}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1"

    fc, vlabels, alabels = [], [], []
    for i, c in enumerate(clips):
        d = c["end"] - c["start"]
        z = c.get("zoom", "none")
        if z == "in":
            zexpr = f"min(1+0.07*on/({FPS}*{d:.3f}),1.07)"
        elif z == "out":
            zexpr = f"max(1.07-0.07*on/({FPS}*{d:.3f}),1.0)"
        else:
            zexpr = "1"
        zoom = (f",scale={W * 2}:{H * 2},zoompan=z='{zexpr}'"
                f":x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2'"
                f":d=1:fps={FPS}:s={W}x{H}" if z != "none" else "")
        fc.append(f"[0:v]trim={c['start']}:{c['end']},setpts=PTS-STARTPTS,"
                  f"{base_scale}{zoom}[v{i}]")
        fc.append(f"[0:a]atrim={c['start']}:{c['end']},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.03,afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03[a{i}]")
        vlabels.append(f"[v{i}]")
        alabels.append(f"[a{i}]")

    n = len(clips)
    fc.append("".join(vlabels) + f"concat=n={n}:v=1:a=0[talkv]")
    fc.append("".join(alabels) + f"concat=n={n}:v=0:a=1[talka]")

    # end card: freeze the last frame of the final clip, dim it, fade in overlay
    last = clips[-1]
    fc.append(f"[0:v]trim={max(last['start'], last['end'] - 0.2)}:{last['end']},"
              f"setpts=PTS-STARTPTS,{base_scale},"
              f"tpad=stop_mode=clone:stop_duration={ec_dur + 1},trim=0:{ec_dur},"
              f"setpts=PTS-STARTPTS,"
              f"colorlevels=rimax=0.45:gimax=0.45:bimax=0.45,"
              f"gblur=sigma=6[ecbg]")
    fc.append(f"[2:v]format=rgba,fade=t=in:d=0.6:alpha=1[ecpng]")
    fc.append(f"[ecbg][ecpng]overlay=0:0:shortest=1,fps={FPS},setsar=1[ecv]")
    fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{ec_dur}[eca]")

    # watermark over talking section only
    fc.append(f"[1:v]format=rgba[wm]")
    fc.append(f"[talkv][wm]overlay=W-w-44:44[talkvw]")
    fc.append(f"[talkvw]subtitles={ass_path}:fontsdir={FONTS}[talkvc]")

    fc.append(f"[talkvc][ecv]concat=n=2:v=1:a=0[outv]")
    ln = cfg.get("loudnorm", "I=-14:TP=-1.5:LRA=11")
    fc.append(f"[talka]loudnorm={ln},aresample=48000[talkan]")
    fc.append(f"[talkan][eca]concat=n=2:v=0:a=1,afade=t=out:st={total - 1.2:.2f}:d=1.2[outa]")

    cmd = ["ffmpeg", "-y",
           "-i", src,
           "-loop", "1", "-t", str(ec_dur + 1), "-i", os.path.join(BRAND, "watermark.png"),
           "-loop", "1", "-t", str(ec_dur + 1), "-i", os.path.join(BRAND, "endcard.png"),
           "-filter_complex", ";".join(fc),
           "-map", "[outv]", "-map", "[outa]",
           "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
           "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", out]
    print(" ".join(cmd[:8]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-4000:])
    subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                    "format=duration,size:stream=codec_name,width,height,avg_frame_rate",
                    "-of", "default=noprint_wrappers=1", out])


if __name__ == "__main__":
    main()
