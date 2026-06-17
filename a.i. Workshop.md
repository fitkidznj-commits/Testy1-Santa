# a.i. Workshop — HyperFrames CLI Video Prompt

Expert marketing prompt for generating a professional promo video for **The A.I.
Advantage Workshop** using HeyGen HyperFrames in the CLI.

## How to use

In your CLI, install the HyperFrames skill (public package — no account access needed):

```bash
npx skills add heygen-com/hyperframes
```

Then run `/hyperframes` and paste the prompt below.

> Note: HyperFrames produces an animated **motion-graphic** video (kinetic
> typography, branded scenes, logos, QR) — not a talking-avatar video. If you want
> your HeyGen avatar in it, composite that clip over the lower-third afterward
> (the prompt leaves room for it).

---

## Prompt

```
ROLE: You are a senior brand-motion designer and direct-response marketer.
Produce a broadcast-quality vertical promo video for a local AI workshop.

OBJECTIVE: Drive sign-ups before July 11 by making the offer feel valuable,
local, and urgent (only 20 seats). Hook in the first 1.5 seconds, end on a
single clear call-to-action.

DELIVERABLE SPEC:
- Aspect ratio: 9:16 vertical, 1080x1920.
- Duration: 35–40 seconds, 30fps.
- Burned-in captions for every spoken/voiceover line (Reels are watched muted).
- Output: MP4.

BRAND IDENTITY ("a.i. STARR"):
- Tropical Florida Keys vibe matching the source flyer.
- Palette: warm cream/off-white background, coral-salmon red, teal/turquoise,
  soft sand tones. Subtle palm-frond and palm-tree silhouettes as accents.
- Typography: bold condensed display font for headlines (slightly playful,
  rounded), clean sans-serif for body and details. High contrast, large text.
- Mood: friendly, confident, energetic — approachable, not corporate.

MOTION STYLE:
- Smooth, modern kinetic typography. Each key fact animates in on its own beat
  (slide/scale/fade with easing — no harsh cuts).
- Light parallax on background palm silhouettes.
- Tasteful accent transitions (wipes in coral/teal). Keep it premium, not busy.

SCENE STRUCTURE (with on-screen text + optional voiceover):
1. HOOK (0:00–0:05) — Big text: "GET AHEAD WITH AI — WITHOUT THE OVERWHELM."
   Brand mark "a.i. STARR" appears. VO: "Want to get ahead with AI, without
   the overwhelm?"
2. TITLE (0:05–0:11) — "THE A.I. ADVANTAGE WORKSHOP / Tips & Tricks to Get Ahead."
   VO: "It's the A.I. Advantage Workshop — two hours of practical, ready-to-use tools."
3. VALUE (0:11–0:19) — Animate in 3 logos/wordmarks: ChatGPT, Gemini, Claude.
   Supporting text: "Save time. Boost productivity. Grow your business."
   VO: "Learn ChatGPT, Gemini, and Claude — no jargon, no fluff."
4. DETAILS (0:19–0:26) — Bold date card: "SATURDAY, JULY 11 / 9–11 AM /
   ISLAMORADA · MM87." VO: "Join us Saturday, July 11th, 9 to 11 AM, in Islamorada."
5. OFFER + SCARCITY (0:26–0:33) — Huge "$39" with "LIMITED TO 20 SEATS" pulsing
   for urgency. VO: "Just $39 — and only 20 seats, so they'll go fast."
6. CTA / END CARD (0:33–0:40) — QR code placeholder (center), plus
   "CALL 305.697.9207" and "YouraiSTaRR@gmail.com", a.i. STARR logo. Hold 3s.
   VO: "Scan the code or call to grab your spot. See you there!"

HARD REQUIREMENTS (verify exactly):
- Date: Saturday, July 11th. Time: 9–11 AM. Location: Islamorada, MM87.
- Price: $39. Seats: limited to 20. Phone: 305.697.9207.
  Email: YouraiSTaRR@gmail.com. Brand: a.i. STARR.
- Reserve a clearly marked placeholder box for the QR code so I can drop in
  the flyer's QR image.
- Keep all text inside safe margins (avoid the top ~12% and bottom ~12% where
  Reels UI overlaps).

NOTES:
- This is a motion-graphic promo; leave the lower-third clear in the HOOK and
  CTA scenes in case I composite a talking-avatar clip over part of the video later.
- Prioritize legibility and pacing over decoration.
```

---

## Driving it in the CLI

- Iterate in small asks after the first render, e.g. "tighten scene 5, make $39
  bigger with a subtle pulse," or "shift the palm silhouettes to a lighter teal."
- Have the flyer's **QR image** ready to drop into the placeholder, and grab the
  official **ChatGPT / Gemini / Claude** logos for scene 3.
- Use `/hyperframes-cli preview` to check timing before the final `render`.
