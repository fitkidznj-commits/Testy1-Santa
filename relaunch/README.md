# Islamorada Shrimp Shack — Relaunch Video Package

A warm, local, "new chapter" relaunch campaign for the **Islamorada Shrimp Shack**
(81901 Overseas Hwy, Islamorada, FL) under new local owner **David Epstein**.

> Message: **The Shack lives on. Same Keys soul. Same famous flavor. New local owner at the helm.**
> Tone: old-school Florida Keys seafood shack — casual, friendly, family, community — *not* a corporate takeover.

## Deliverables (`out/`)
| File | Format | Use |
|------|--------|-----|
| `shrimp_shack_relaunch_main_1080p.mp4` | 1920×1080 · ~70s | Website, Facebook, presentations |
| `shrimp_shack_relaunch_reel_vertical_1080x1920.mp4` | 1080×1920 · ~30s | Instagram / Facebook Reels & Stories |
| `shrimp_shack_relaunch_teaser_15s_1080p.mp4` | 1920×1080 · 15s | Teaser — "The Shack lives on." |
| `thumbnail_same_shack_same_soul.png` | 1920×1080 | Poster / thumbnail — *Same Shack. Same Soul. New Chapter.* |

All four follow one editing style: warm tropical color grade, natural-sun gradients, film
grain, large mobile-friendly captions, a simple logo build, gentle Ken Burns motion, and a
light original island music bed.

## A note on assets (please read before publishing)
- **No brand logo or photography was provided**, and the live website/photo sources were not
  reachable from the build environment. So every visual is **original, procedurally-designed
  artwork** (gradient Keys skies/water, sun, palm/boat/pelican/shack silhouettes, illustrated
  food plates) plus a **designed wordmark lockup**. These are tasteful, brand-safe placeholders
  in the right style — **swap in the real logo, real food photos, and real footage of David and
  the team before final publishing** for maximum authenticity. The build is modular so this is easy.
- **Voiceover** is an AI scratch track. See `VOICEOVER_SCRIPT.md` — re-record with a real Keys
  voice for extra local warmth (same line lengths drop straight in).
- **Music** is synthesized from scratch in `build/music.py` → royalty-free by construction.
- **Diners, Drive-Ins & Dives**: used as **text only** ("As seen on…") on the thumbnail. No Guy
  Fieri likeness and no Food Network footage are used. Confirm you're comfortable with the text
  mention before publishing.
- **Verify current hours, menu items, and the address/mile-marker** before publishing.

## Brand / messaging guardrails honored
- Leads on **"new chapter"**, not "new ownership" (mentioned minimally).
- Emphasis on **continuity, trust, local pride, and food** — the favorites are explicitly "staying."
- Family-friendly, community-forward; no luxury/corporate styling or cheesy transitions.

## Regenerating / editing
Requires Python 3.11+. One-time setup (downloads fonts + a neural TTS voice; ~140MB):
```bash
pip install imageio-ffmpeg pillow numpy scipy soundfile sherpa-onnx
# fonts -> relaunch/fonts/ : Anton, BebasNeue, Pacifico, Lobster, Montserrat-VF (Google Fonts, OFL)
# voice  -> relaunch/voices/ : vits-piper-en_US-hfc_female-medium (+ ryan-medium), from
#           github.com/k2-fsa/sherpa-onnx releases (tts-models)
```
Then from `relaunch/`:
```bash
python3 build/tts.py female build/vo      # main voiceover
python3 build/tts_extra.py                # reel + teaser voiceover
python3 build/story_main.py               # -> out/...main_1080p.mp4
python3 build/story_vertical.py           # -> out/...reel_vertical...mp4
python3 build/story_teaser.py             # -> out/...teaser_15s...mp4
python3 build/thumbnail.py                # -> out/thumbnail...png
```

### Code map (`build/`)
- `art.py` — palettes, gradients, sun, silhouettes (palm/boat/pelican/shack/person), grain/grade, **logo lockup**, illustrated **food cards**.
- `scenes.py` — full scene "plates" (hook / legacy / owner / food / community / CTA).
- `layers.py` — caption & lower-third text layers (letter-spacing, shadows).
- `music.py` — original island music bed.
- `audio_master.py` — places VO on the timeline and ducks music beneath it.
- `engine.py` — Ken Burns + timed overlay animation, piped to ffmpeg with audio.
- `story_main.py` / `story_vertical.py` / `story_teaser.py` / `thumbnail.py` — the four deliverables.
