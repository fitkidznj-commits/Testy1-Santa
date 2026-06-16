#!/usr/bin/env python3
"""
Procedural art for the Islamorada Shrimp Shack relaunch film.
A cohesive 'old-school Florida Keys' look: warm gradient skies + water,
sun, palm / boat / pelican / piling silhouettes, film grain, vignette,
a hand-built brand lockup and illustrated food cards.
All vector/procedural -> honest, brand-safe, no fake photography.
"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "fonts")

# ---------------------------------------------------------------- fonts
_FONT_CACHE = {}
def font(name, size):
    key = (name, size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    path = os.path.join(FONTS, name)
    f = ImageFont.truetype(path, size)
    _FONT_CACHE[key] = f
    return f

def mfont(size, weight="Bold"):
    """Montserrat variable instance."""
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat-VF.ttf"), size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f

# ---------------------------------------------------------------- color
def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

PALETTES = {
    # top sky color, mid color, horizon glow, water top, water bottom, sun
    "dawn":   [(255,228,179),(255,193,143),(255,150,120),(86,176,178),(20,92,120),(255,236,170)],
    "sunset": [(255,205,140),(255,150,110),(232,104,98),(70,150,160),(18,74,104),(255,224,150)],
    "day":    [(176,229,232),(140,212,224),(120,196,214),(64,184,188),(16,104,128),(255,247,214)],
    "golden": [(255,224,168),(255,188,128),(247,150,104),(72,168,170),(20,92,116),(255,232,168)],
    "hero":   [(255,216,150),(255,170,118),(238,120,104),(58,170,178),(14,86,118),(255,236,176)],
    "kitchen":[(58,46,52),(70,52,58),(96,62,60),(40,34,42),(20,18,26),(255,210,150)],
}

# ---------------------------------------------------------------- gradient
def vgrad(w, h, stops):
    """stops: list of (pos0..1, (r,g,b)). Returns RGB array image."""
    ys = np.linspace(0, 1, h)
    arr = np.zeros((h, w, 3), np.float32)
    cols = np.zeros((h, 3), np.float32)
    stops = sorted(stops, key=lambda s: s[0])
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]; p1, c1 = stops[i+1]
        m = (ys >= p0) & (ys <= p1 + 1e-6)
        if not m.any():
            continue
        t = (ys[m] - p0) / max(1e-6, (p1 - p0))
        for ch in range(3):
            cols[m, ch] = c0[ch] + (c1[ch] - c0[ch]) * t
    cols[ys < stops[0][0]] = stops[0][1]
    cols[ys > stops[-1][0]] = stops[-1][1]
    arr[:] = cols[:, None, :]
    return arr

def sky_water(w, h, pal, horizon=0.62):
    """Full tropical sky+water plate as PIL RGB."""
    p = PALETTES[pal]
    stops = [
        (0.0, p[0]), (horizon*0.55, p[1]), (horizon-0.02, p[2]),
        (horizon, lerp(p[2], p[3], 0.5)),
        (horizon+0.005, p[3]), (1.0, p[4]),
    ]
    arr = vgrad(w, h, stops)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# ---------------------------------------------------------------- sun
def add_sun(img, cx, cy, r, color=(255,238,176), glow=1.0):
    w, h = img.size
    layer = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    # soft glow
    for i in range(14, 0, -1):
        rr = r * (1 + i*0.55*glow)
        a = int(10*glow*(1 - i/15))
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=color+(max(0,a),))
    layer = layer.filter(ImageFilter.GaussianBlur(r*0.25))
    d2 = ImageDraw.Draw(layer)
    d2.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color+(235,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0,0))
    return img

def sun_glints(img, horizon_y, cx, color=(255,245,200)):
    """Sun reflection shimmer on the water."""
    w, h = img.size
    layer = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    rng = random.Random(7)
    y = horizon_y + 8
    while y < h:
        spread = int((y - horizon_y) * 0.5) + 10
        n = max(2, spread // 14)
        for _ in range(n):
            x = cx + rng.randint(-spread, spread)
            ln = rng.randint(8, 26)
            a = int(70 * (1 - (y-horizon_y)/(h-horizon_y)))
            d.line([x, y, x+ln, y], fill=color+(max(0,a),), width=2)
        y += rng.randint(7, 12)
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

# ---------------------------------------------------------------- silhouettes
def _silhouette_layer(w, h, color=(20,28,34), alpha=255):
    return Image.new("RGBA", (w, h), (0,0,0,0)), color+(alpha,)

def palm(img, x, base_y, scale=1.0, color=(16,26,30), alpha=255, flip=False):
    w, h = img.size
    layer, col = _silhouette_layer(w, h, color, alpha)
    d = ImageDraw.Draw(layer)
    s = scale
    th = 220*s
    # curved trunk
    pts_l, pts_r = [], []
    segs = 22
    for i in range(segs+1):
        t = i/segs
        cur = 60*s*math.sin(t*1.4) * (-1 if flip else 1)
        yy = base_y - t*th
        xx = x + cur
        wdt = (16 - 9*t)*s
        pts_l.append((xx-wdt, yy)); pts_r.append((xx+wdt, yy))
    d.polygon(pts_l + pts_r[::-1], fill=col)
    topx = pts_l[-1][0] + (pts_l[-1][0]-pts_l[-2][0]); topy = pts_l[-1][1]
    cx = (pts_l[-1][0]+pts_r[-1][0])/2; cy = pts_l[-1][1]
    # fronds
    rng = random.Random(int(x))
    for k in range(9):
        ang = math.radians(-12 + k*(204/8)) + (math.pi if flip else 0)*0
        L = (150 + rng.randint(-20,30))*s
        droop = 0.5
        midx = cx + math.cos(ang)*L*0.55
        midy = cy + math.sin(ang)*L*0.55 - 8*s
        endx = cx + math.cos(ang)*L
        endy = cy + math.sin(ang)*L + droop*70*s
        wdt = 13*s
        nx, ny = -math.sin(ang), math.cos(ang)
        poly = [(cx,cy),
                (midx+nx*wdt, midy+ny*wdt),
                (endx, endy),
                (midx-nx*wdt, midy-ny*wdt)]
        d.polygon(poly, fill=col)
    img2 = Image.alpha_composite(img.convert("RGBA"), layer)
    img.paste(img2.convert("RGB"), (0,0))
    return img

def boat(img, cx, y, scale=1.0, color=(24,34,40), alpha=235):
    w, h = img.size
    layer, col = _silhouette_layer(w, h, color, alpha)
    d = ImageDraw.Draw(layer)
    s = scale
    hull = [(cx-70*s,y),(cx+78*s,y),(cx+58*s,y+22*s),(cx-50*s,y+22*s)]
    d.polygon(hull, fill=col)
    d.rectangle([cx-20*s,y-26*s,cx+34*s,y], fill=col)       # cabin
    d.rectangle([cx+30*s,y-58*s,cx+36*s,y-26*s], fill=col)  # tower
    d.line([cx-40*s,y-2*s,cx-40*s,y-70*s], fill=col, width=max(1,int(3*s)))  # outrigger
    d.line([cx+50*s,y-2*s,cx+50*s,y-70*s], fill=col, width=max(1,int(3*s)))
    img2 = Image.alpha_composite(img.convert("RGBA"), layer)
    img.paste(img2.convert("RGB"), (0,0)); return img

def piling(img, x, top_y, base_y, scale=1.0, color=(30,24,22), alpha=255, bird=False):
    w, h = img.size
    layer, col = _silhouette_layer(w, h, color, alpha)
    d = ImageDraw.Draw(layer)
    s = scale; wdt = 18*s
    d.rectangle([x-wdt, top_y, x+wdt, base_y], fill=col)
    d.ellipse([x-wdt-2, top_y-6*s, x+wdt+2, top_y+8*s], fill=col)
    if bird:  # pelican silhouette perched
        bx, by = x, top_y-6*s
        d.ellipse([bx-26*s, by-34*s, bx+18*s, by-2*s], fill=col)   # body
        d.ellipse([bx+4*s, by-52*s, bx+30*s, by-30*s], fill=col)   # head
        d.polygon([(bx+26*s,by-44*s),(bx+64*s,by-30*s),(bx+26*s,by-32*s)], fill=col)  # beak
    img2 = Image.alpha_composite(img.convert("RGBA"), layer)
    img.paste(img2.convert("RGB"), (0,0)); return img

def gull(img, x, y, scale=1.0, color=(40,50,58), alpha=200):
    w, h = img.size
    layer, col = _silhouette_layer(w, h, color, alpha)
    d = ImageDraw.Draw(layer); s=scale*14
    d.arc([x-s, y-s*0.6, x, y+s*0.4], 300, 360, fill=col, width=max(2,int(scale*3)))
    d.arc([x, y-s*0.6, x+s, y+s*0.4], 180, 240, fill=col, width=max(2,int(scale*3)))
    img2 = Image.alpha_composite(img.convert("RGBA"), layer)
    img.paste(img2.convert("RGB"), (0,0)); return img

def hut(img, cx, base_y, scale=1.0, color=(26,30,34), alpha=255, glow=True):
    """Old-school seafood shack silhouette with warm window glow + awning."""
    w,h=img.size
    layer,col=_silhouette_layer(w,h,color,alpha)
    d=ImageDraw.Draw(layer); s=scale
    bw=300*s; bh=150*s
    left=cx-bw/2; right=cx+bw/2; top=base_y-bh
    d.rectangle([left,top,right,base_y], fill=col)                      # walls
    d.polygon([(left-26*s,top),(right+26*s,top),(cx,top-94*s)], fill=col)  # roof
    d.rectangle([cx-10*s, base_y-bh-150*s, cx+10*s, top-70*s], fill=col)   # sign post
    img2=Image.alpha_composite(img.convert("RGBA"),layer); img.paste(img2.convert("RGB"),(0,0))
    if glow:
        gl=Image.new("RGBA",(w,h),(0,0,0,0)); dg=ImageDraw.Draw(gl)
        for (ox) in (-0.26,0.0,0.26):
            wx=cx+ox*bw
            dg.rectangle([wx-26*s, top+34*s, wx+26*s, top+92*s], fill=(255,196,108,235))
        dg.rectangle([cx-34*s, base_y-78*s, cx+34*s, base_y], fill=(255,176,86,225))  # doorway
        gl2=gl.filter(ImageFilter.GaussianBlur(2))
        img.paste(Image.alpha_composite(img.convert("RGBA"),gl2).convert("RGB"),(0,0))
    return img

def person(img, x, base_y, scale=1.0, color=(20,26,30), alpha=255):
    w,h=img.size
    layer,col=_silhouette_layer(w,h,color,alpha)
    d=ImageDraw.Draw(layer); s=scale
    d.ellipse([x-12*s,base_y-86*s,x+12*s,base_y-62*s], fill=col)          # head
    d.polygon([(x-16*s,base_y-58*s),(x+16*s,base_y-58*s),(x+20*s,base_y),(x-20*s,base_y)], fill=col)  # body
    img2=Image.alpha_composite(img.convert("RGBA"),layer); img.paste(img2.convert("RGB"),(0,0))
    return img

# ---------------------------------------------------------------- texture / grade
_GRAIN = {}
def grain_overlay(w, h, amt=10, seed=1):
    key=(w,h,seed)
    if key not in _GRAIN:
        rng=np.random.default_rng(seed)
        n=rng.normal(0,1,(h,w)).astype(np.float32)
        _GRAIN[key]=n
    n=_GRAIN[key]*amt
    return n  # additive luminance noise array

def finish(img, vignette=0.32, grain=8, seed=1, warm=1.0):
    """Apply film grain, gentle warm grade, vignette. Returns RGB."""
    w, h = img.size
    arr = np.asarray(img, np.float32)
    # warm grade
    arr[..., 0] *= (1.0 + 0.05*warm)
    arr[..., 2] *= (1.0 - 0.04*warm)
    # grain
    g = grain_overlay(w, h, grain, seed)[..., None]
    arr += g
    # vignette
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w/2, h/2
    d = np.sqrt(((xx-cx)/(w*0.62))**2 + ((yy-cy)/(h*0.62))**2)
    v = np.clip(1 - vignette*np.clip(d-0.35,0,1), 0, 1)[..., None]
    arr *= v
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8))

def light_leak(img, side="tr", color=(255,196,120), strength=0.5):
    w,h=img.size
    layer=Image.new("RGBA",(w,h),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    cx = w*0.85 if "r" in side else w*0.15
    cy = h*0.12 if "t" in side else h*0.88
    for i in range(10,0,-1):
        rr=w*0.18*i/3
        a=int(60*strength*(1-i/11))
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], fill=color+(max(0,a),))
    layer=layer.filter(ImageFilter.GaussianBlur(w*0.04))
    return Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB")

def scrim(img, top=0.0, bottom=0.0, col=(8,30,40)):
    """Darken top/bottom bands for caption legibility."""
    w,h=img.size
    arr=np.zeros((h,w,4),np.float32)
    ys=np.linspace(0,1,h)
    alpha=np.zeros(h,np.float32)
    if bottom>0:
        b=np.clip((ys-(1-bottom))/bottom,0,1)**1.4
        alpha=np.maximum(alpha, b*165)
    if top>0:
        tg=np.clip(((top-ys)/top),0,1)**1.4
        alpha=np.maximum(alpha, tg*150)
    for c in range(3): arr[...,c]=col[c]
    arr[...,3]=alpha[:,None]
    layer=Image.fromarray(arr.astype(np.uint8))
    return Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB")

# ---------------------------------------------------------------- shrimp icon + logo
def draw_shrimp(d, cx, cy, s, color=(232,92,66), outline=(150,40,30)):
    """Stylized curled shrimp icon."""
    # body: series of overlapping segments along a curl
    pts=[]
    for i in range(7):
        t=i/6
        ang=math.radians(20+t*210)
        rad=s*(1.0-0.45*t)
        x=cx+math.cos(ang)*s*0.9
        y=cy+math.sin(ang)*s*0.9
        pts.append((x,y,rad*0.5))
    for (x,y,r) in pts:
        d.ellipse([x-r,y-r,x+r,y+r], fill=color, outline=outline, width=max(1,int(s*0.04)))
    # tail fan
    tx,ty,_=pts[0]
    d.polygon([(tx,ty),(tx+s*0.6,ty-s*0.5),(tx+s*0.9,ty-s*0.1),(tx+s*0.6,ty+s*0.35)], fill=color, outline=outline)
    # head + eye
    hx,hy,hr=pts[-1]
    d.ellipse([hx-hr*0.7,hy-hr*0.7,hx+hr*0.7,hy+hr*0.7], fill=color, outline=outline)
    d.ellipse([hx-hr*0.15,hy-hr*0.2,hx+hr*0.15,hy+hr*0.1], fill=(30,24,24))
    # legs / antennae
    for k in range(4):
        a=math.radians(40+k*22)
        d.line([hx,hy,hx+math.cos(a)*s*1.1, hy+math.sin(a)*s*1.1], fill=outline, width=max(1,int(s*0.05)))

def logo_lockup(scale=1.0, dark_text=True, on_light=True):
    """
    Build the Islamorada Shrimp Shack brand lockup as an RGBA image (transparent bg).
    Designed wordmark (no copyrighted asset available).
    """
    W,H=int(1120*scale),int(700*scale)
    img=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(img)
    coral=(232,92,66); cream=(255,250,238); navy=(20,52,66)
    ink = navy if dark_text else cream
    cx=W//2
    # top kicker
    f_k=font("BebasNeue-Regular.ttf", int(50*scale))
    kick="ISLAMORADA  •  FLORIDA KEYS"
    tw=d.textlength(kick,font=f_k)
    d.text((cx-tw/2, int(30*scale)), kick, font=f_k, fill=ink)
    d.line([cx-tw/2, int(94*scale), cx+tw/2, int(94*scale)], fill=coral, width=max(2,int(4*scale)))
    # shrimp icon
    draw_shrimp(d, cx, int(152*scale), 42*scale, color=coral, outline=(150,40,30))
    # main words
    f_big=font("Anton-Regular.ttf", int(146*scale))
    for i,word in enumerate(["SHRIMP","SHACK"]):
        tw=d.textlength(word,font=f_big)
        yy=int((226+i*156)*scale)
        d.text((cx-tw/2+3, yy+4), word, font=f_big, fill=(0,0,0,70))   # shadow
        d.text((cx-tw/2, yy), word, font=f_big, fill=ink)
    # est ribbon
    f_e=font("BebasNeue-Regular.ttf", int(38*scale))
    est="EST. 2011  •  THE KEYS' FAVORITE SEAFOOD SHACK"
    tw=d.textlength(est,font=f_e)
    yb=int(560*scale)
    d.text((cx-tw/2, yb), est, font=f_e, fill=coral)
    return img

# ---------------------------------------------------------------- food card
def food_card(title, kind, w=900, h=1100):
    """Illustrated food card: warm board background + vector food + big name."""
    img=Image.new("RGB",(w,h),(40,32,30))
    # weathered board gradient
    arr=vgrad(w,h,[(0,(58,44,38)),(0.5,(44,34,30)),(1,(30,24,22))])
    img=Image.fromarray(arr.astype(np.uint8))
    d=ImageDraw.Draw(img,"RGBA")
    # plank lines
    for x in range(0,w,150):
        d.line([x,0,x,h], fill=(0,0,0,40), width=3)
    # plate / bowl
    pcx,pcy=w//2,int(h*0.46); pr=int(w*0.36)
    d.ellipse([pcx-pr,pcy-pr*0.82,pcx+pr,pcy+pr*0.82], fill=(248,243,232), outline=(206,196,178), width=8)
    d.ellipse([pcx-pr*0.82,pcy-pr*0.66,pcx+pr*0.82,pcy+pr*0.66], outline=(225,217,202), width=4)
    coral=(232,108,72); gold=(228,176,86); cream=(250,238,206)
    def shrimp(x,y,s,rot=0):
        dd=ImageDraw.Draw(img,"RGBA")
        for i in range(6):
            t=i/5; ang=math.radians(rot+20+t*200); r=s*(1-0.4*t)
            xx=x+math.cos(ang)*s*0.8; yy=y+math.sin(ang)*s*0.8
            dd.ellipse([xx-r*0.5,yy-r*0.5,xx+r*0.5,yy+r*0.5], fill=coral, outline=(176,64,40), width=3)
    if kind=="fritters":
        for (ox,oy) in [(-0.16,-0.08),(0.17,-0.05),(0.0,0.16),(-0.14,0.2),(0.16,0.2)]:
            cxp=pcx+int(ox*pr*2); cyp=pcy+int(oy*pr*2); rr=int(pr*0.3)
            d.ellipse([cxp-rr,cyp-rr*0.9,cxp+rr,cyp+rr*0.9], fill=(214,150,74), outline=(168,110,48), width=4)
            for _ in range(18):
                a=random.Random(cxp+cyp).uniform(0,6.28)
            # speckle
        for s_ in range(40):
            rng=random.Random(s_*7+1)
            ang=rng.uniform(0,6.28); rad=rng.uniform(0,pr*0.7)
            xx=pcx+math.cos(ang)*rad; yy=pcy+math.sin(ang)*rad*0.8
            d.ellipse([xx-3,yy-3,xx+3,yy+3], fill=(150,96,40,160))
    elif kind=="grits":
        d.ellipse([pcx-pr*0.7,pcy-pr*0.5,pcx+pr*0.7,pcy+pr*0.5], fill=(244,236,214))  # grits
        for (ox,oy,rot) in [(-0.2,-0.1,10),(0.18,-0.12,200),(0.0,0.12,90),(-0.12,0.16,150)]:
            shrimp(pcx+int(ox*pr*2),pcy+int(oy*pr*2),int(pr*0.22),rot)
        for _ in range(10):
            rng=random.Random(_*3+5); xx=pcx+rng.randint(-int(pr*0.6),int(pr*0.6)); yy=pcy+rng.randint(-int(pr*0.3),int(pr*0.4))
            d.ellipse([xx-6,yy-6,xx+6,yy+6], fill=(120,150,80,200))  # scallion
    elif kind=="dip":
        d.ellipse([pcx-pr*0.6,pcy-pr*0.5,pcx+pr*0.6,pcy+pr*0.45], fill=(238,224,196))  # dip
        d.ellipse([pcx-pr*0.4,pcy-pr*0.34,pcx+pr*0.4,pcy+pr*0.25], fill=(228,210,176))
        d.ellipse([pcx-12,pcy-pr*0.18,pcx+12,pcy-pr*0.18+24], fill=(214,80,60))  # paprika dot
        for (ox) in [-0.7,-0.5,0.5,0.7]:  # crackers
            xx=pcx+int(ox*pr);
            d.rounded_rectangle([xx-34,pcy+pr*0.4,xx+34,pcy+pr*0.4+90], radius=8, fill=(226,196,140), outline=(190,150,90), width=3)
    elif kind=="fish":
        # whole fresh fish
        d.ellipse([pcx-pr*0.75,pcy-pr*0.32,pcx+pr*0.6,pcy+pr*0.32], fill=(150,176,190), outline=(96,120,140), width=5)
        d.polygon([(pcx+pr*0.55,pcy),(pcx+pr*0.8,pcy-pr*0.3),(pcx+pr*0.8,pcy+pr*0.3)], fill=(150,176,190), outline=(96,120,140))
        d.ellipse([pcx-pr*0.6,pcy-pr*0.12,pcx-pr*0.6+22,pcy-pr*0.12+22], fill=(30,30,36))  # eye
        d.line([pcx-pr*0.5,pcy-2,pcx+pr*0.45,pcy-2], fill=(96,120,140,180), width=4)
        # lime wedges
        for ox in [-0.55,0.5]:
            xx=pcx+int(ox*pr); yy=int(pcy+pr*0.5)
            d.pieslice([xx-34,yy-34,xx+34,yy+34],200,340, fill=(180,206,90), outline=(120,150,60), width=3)
    elif kind=="conch":
        for (ox,oy) in [(-0.18,-0.05),(0.18,-0.05),(0.0,0.18)]:
            cxp=pcx+int(ox*pr*2); cyp=pcy+int(oy*pr*2); rr=int(pr*0.34)
            d.ellipse([cxp-rr,cyp-rr*0.7,cxp+rr,cyp+rr*0.7], fill=(220,164,92), outline=(170,116,52), width=5)
        for ox in [-0.55,0.55]:
            xx=pcx+int(ox*pr); yy=int(pcy+pr*0.45)
            d.pieslice([xx-30,yy-30,xx+30,yy+30],200,340, fill=(180,206,90), outline=(120,150,60), width=3)
    elif kind=="pie":
        d.pieslice([pcx-pr*0.7,pcy-pr*0.5,pcx+pr*0.7,pcy+pr*0.7],180,360, fill=(232,224,150), outline=(150,120,60), width=5)  # slice top
        d.polygon([(pcx-pr*0.66,pcy),(pcx+pr*0.66,pcy),(pcx,pcy+pr*0.6)], fill=(238,232,168), outline=(170,140,80))
        d.line([(pcx-pr*0.66,pcy),(pcx+pr*0.66,pcy)], fill=(180,150,90), width=6)  # crust edge
        d.ellipse([pcx-22,pcy-pr*0.18,pcx+22,pcy-pr*0.18+44], fill=(250,250,250))  # cream dollop
    # steam
    for sx in [-0.12,0.0,0.12]:
        x0=pcx+int(sx*pr*2)
        pts=[(x0+int(18*math.sin(i/2.0)), pcy-pr*0.7-i*16) for i in range(8)]
        d.line(pts, fill=(255,255,255,40), width=6)
    img=img.filter(ImageFilter.GaussianBlur(0.4))
    return img


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT,"build","preview"), exist_ok=True)
    # quick test scene
    W,H=1920,1080
    img=sky_water(W,H,"dawn",0.60)
    img=add_sun(img, int(W*0.7), int(H*0.34), 90)
    img=sun_glints(img, int(H*0.60), int(W*0.7))
    img=boat(img, int(W*0.34), int(H*0.60), 1.1)
    img=piling(img, int(W*0.12), int(H*0.50), int(H*0.66), 1.2, bird=True)
    img=palm(img, int(W*0.90), int(H*0.92), 1.5)
    img=palm(img, int(W*0.07), int(H*0.96), 1.2, flip=True)
    img=gull(img, int(W*0.55), int(H*0.2), 1.2)
    img=gull(img, int(W*0.6), int(H*0.24), 0.9)
    img=light_leak(img,"tr",strength=0.5)
    img=scrim(img, bottom=0.34)
    img=finish(img, grain=7, seed=3)
    img.save(os.path.join(ROOT,"build","preview","scene_test.png"))
    logo_lockup(0.9, dark_text=False).save(os.path.join(ROOT,"build","preview","logo.png"))
    food_card("FAMOUS SHRIMP FRITTERS","fritters").save(os.path.join(ROOT,"build","preview","food_fritters.png"))
    print("preview written")
