#!/usr/bin/env python3
"""Generate Take Down Charters typographic brand assets.

Outputs (all transparent PNGs):
  assets/brand/watermark.png   - small corner watermark lockup
  assets/brand/lockup.png      - large brand lockup (for end card)
  assets/brand/endcard.png     - full 1920x1080 end-card overlay
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "assets", "brand")
os.makedirs(OUT, exist_ok=True)

ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
ARCHIVO = os.path.join(FONTS, "ArchivoBlack-Regular.ttf")
OSWALD = os.path.join(FONTS, "Oswald%5Bwght%5D.ttf")

WHITE = (255, 255, 255, 255)
AQUA = (41, 197, 230, 255)
DARK = (10, 25, 35, 255)


def text_size(draw, text, font, spacing=0):
    if spacing:
        w = 0
        for ch in text:
            b = draw.textbbox((0, 0), ch, font=font)
            w += (b[2] - b[0]) + spacing
        w -= spacing
        b = draw.textbbox((0, 0), text, font=font)
        return w, b[3] - b[1]
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def draw_spaced(draw, pos, text, font, fill, spacing):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        b = draw.textbbox((0, 0), ch, font=font)
        x += (b[2] - b[0]) + spacing


def with_shadow(img, blur=8, alpha=160, offset=(0, 4)):
    """Return img composited over a soft dark shadow of its own alpha."""
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: int(v * alpha / 255))
    black = Image.new("RGBA", img.size, (0, 0, 0, 255))
    shadow.paste(black, offset, a)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(shadow, img)


def make_lockup(scale=1.0, accent=True):
    """'TAKE DOWN' over letter-spaced 'CHARTERS' with rules."""
    f_main = ImageFont.truetype(ANTON, int(190 * scale))
    f_sub = ImageFont.truetype(OSWALD, int(64 * scale))
    pad = int(60 * scale)
    img = Image.new("RGBA", (int(1600 * scale), int(560 * scale)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    main = "TAKE DOWN"
    mw, _ = text_size(d, main, f_main, spacing=int(6 * scale))
    cx = img.width // 2
    y0 = pad
    draw_spaced(d, (cx - mw // 2, y0), main, f_main, WHITE, int(6 * scale))

    sub = "CHARTERS"
    sp = int(34 * scale)
    sw, sh = text_size(d, sub, f_sub, spacing=sp)
    y1 = y0 + int(250 * scale) + int(28 * scale)
    sub_fill = AQUA if accent else WHITE
    draw_spaced(d, (cx - sw // 2, y1), sub, f_sub, sub_fill, sp)

    # thin rules flanking CHARTERS
    ry = y1 + int(44 * scale)
    gap = int(36 * scale)
    rw = int(170 * scale)
    d.rectangle([cx - sw // 2 - gap - rw, ry, cx - sw // 2 - gap, ry + max(2, int(4 * scale))], fill=sub_fill)
    d.rectangle([cx + sw // 2 + gap, ry, cx + sw // 2 + gap + rw, ry + max(2, int(4 * scale))], fill=sub_fill)

    bbox = img.getbbox()
    img = img.crop(bbox)
    return img


def make_watermark():
    """Single-line small watermark: TAKE DOWN CHARTERS."""
    f = ImageFont.truetype(ARCHIVO, 54)
    tmp = Image.new("RGBA", (1400, 160), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    t1, t2 = "TAKE DOWN ", "CHARTERS"
    w1, _ = text_size(d, t1, f)
    w2, _ = text_size(d, t2, f)
    d.text((20, 40), t1, font=f, fill=WHITE)
    d.text((20 + w1, 40), t2, font=f, fill=AQUA)
    img = tmp.crop(tmp.getbbox())
    pad = 14
    canvas = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(img, (pad, pad), img)
    canvas = with_shadow(canvas, blur=5, alpha=190, offset=(0, 3))
    # global opacity ~78%
    a = canvas.split()[3].point(lambda v: int(v * 0.78))
    canvas.putalpha(a)
    canvas.save(os.path.join(OUT, "watermark.png"))


def make_endcard():
    W, H = 1920, 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    lockup = make_lockup(scale=1.05)
    lockup = with_shadow(lockup, blur=10, alpha=170)
    lx = (W - lockup.width) // 2
    ly = 240
    img.paste(lockup, (lx, ly), lockup)

    d = ImageDraw.Draw(img)
    f_loc = ImageFont.truetype(OSWALD, 52)
    loc = "WHALE HARBOR  •  ISLAMORADA, FLORIDA"
    sp = 6
    lw, _ = text_size(d, loc, f_loc, spacing=sp)
    loc_img = Image.new("RGBA", (lw + 40, 110), (0, 0, 0, 0))
    dl = ImageDraw.Draw(loc_img)
    draw_spaced(dl, (20, 20), loc, f_loc, (235, 240, 242, 235), sp)
    loc_img = with_shadow(loc_img.crop(loc_img.getbbox()), blur=6, alpha=170, offset=(0, 3))
    img.paste(loc_img, ((W - loc_img.width) // 2, ly + lockup.height + 70), loc_img)

    # pill button: BOOK YOUR CHARTER
    f_btn = ImageFont.truetype(ARCHIVO, 56)
    btn_t = "BOOK YOUR CHARTER"
    bw, bh = text_size(d, btn_t, f_btn)
    px, py = 70, 34
    pill_w, pill_h = bw + px * 2, bh + py * 2
    pill = Image.new("RGBA", (pill_w + 40, pill_h + 40), (0, 0, 0, 0))
    dp = ImageDraw.Draw(pill)
    dp.rounded_rectangle([20, 20, 20 + pill_w, 20 + pill_h], radius=(pill_h) // 2, fill=AQUA)
    bb = dp.textbbox((0, 0), btn_t, font=f_btn)
    dp.text((20 + px - bb[0], 20 + py - bb[1]), btn_t, font=f_btn, fill=DARK)
    pill = with_shadow(pill, blur=10, alpha=150, offset=(0, 5))
    img.paste(pill, ((W - pill.width) // 2, H - 280), pill)

    img.save(os.path.join(OUT, "endcard.png"))


def main():
    make_watermark()
    lk = make_lockup(scale=1.0)
    lk = with_shadow(lk, blur=10, alpha=170)
    lk.save(os.path.join(OUT, "lockup.png"))
    make_endcard()
    print("brand assets written to", OUT)


if __name__ == "__main__":
    main()
