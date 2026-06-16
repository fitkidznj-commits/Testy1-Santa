#!/usr/bin/env python3
"""Caption / text overlay layers (output-resolution RGBA) with letter-spacing
and soft shadows for mobile legibility."""
from PIL import Image, ImageDraw, ImageFilter
import art

CORAL=(232,92,66); CREAM=(255,250,238); WHITE=(255,255,255); NAVY=(18,46,60)
GOLD=(255,206,120); TEAL=(20,120,134)

def tracked_width(d, text, font, track):
    return sum(d.textlength(c, font=font) for c in text) + track*max(0,len(text)-1)

def draw_tracked(d, x, y, text, font, fill, track=0, anchor_center=None, shadow=None):
    if anchor_center is not None:
        w=tracked_width(d,text,font,track); x=anchor_center-w/2
    if shadow:
        sx,sy,scol=shadow
        cx=x
        for c in text:
            d.text((cx+sx,y+sy), c, font=font, fill=scol)
            cx+=d.textlength(c,font=font)+track
    cx=x
    for c in text:
        d.text((cx,y), c, font=font, fill=fill)
        cx+=d.textlength(c,font=font)+track

def _layer(W,H): return Image.new("RGBA",(W,H),(0,0,0,0))

def caption(W,H, items, cy, gap=18):
    """items: list of dict(text, font(ImageFont), color, track=0, shadow=True, glow=False).
    Stacks centered around vertical center cy."""
    lay=_layer(W,H); d=ImageDraw.Draw(lay)
    # measure heights
    hs=[]
    for it in items:
        asc,desc=it['font'].getmetrics(); hs.append(asc+desc)
    toth=sum(hs)+gap*(len(items)-1)
    y=cy-toth/2
    for it,h in zip(items,hs):
        sh=(2,3,(0,0,0,150)) if it.get('shadow',True) else None
        if it.get('glow'):
            gl=_layer(W,H); dg=ImageDraw.Draw(gl)
            draw_tracked(dg, 0,y, it['text'], it['font'], it['color']+(255,) if len(it['color'])==3 else it['color'],
                         it.get('track',0), anchor_center=W/2)
            gl=gl.filter(ImageFilter.GaussianBlur(10)); lay.alpha_composite(gl)
        col=it['color'] if len(it['color'])==4 else it['color']+(255,)
        draw_tracked(d, 0,y, it['text'], it['font'], col, it.get('track',0),
                     anchor_center=W/2, shadow=sh)
        y+=h+gap
    return lay

def lower_third(W,H, kicker, title, kicker_color=GOLD, title_color=CREAM, y=None):
    """Food-name style lower third: small spaced kicker + big condensed title near bottom."""
    lay=_layer(W,H); d=ImageDraw.Draw(lay)
    fk=art.font("BebasNeue-Regular.ttf", int(H*0.040))
    ft=art.font("Anton-Regular.ttf", int(H*0.085))
    if y is None: y=int(H*0.74)
    draw_tracked(d, 0,y, kicker, fk, kicker_color+(255,), track=int(H*0.012), anchor_center=W/2,
                 shadow=(2,2,(0,0,0,150)))
    draw_tracked(d, 0,y+int(H*0.055), title, ft, title_color+(255,), track=2, anchor_center=W/2,
                 shadow=(3,4,(0,0,0,170)))
    return lay

def script_line(W,H, text, size_frac, cy, color=CREAM, shadow=True):
    lay=_layer(W,H); d=ImageDraw.Draw(lay)
    f=art.font("Pacifico-Regular.ttf", int(H*size_frac))
    sh=(2,4,(0,0,0,150)) if shadow else None
    draw_tracked(d,0,cy,text,f,color+(255,),0,anchor_center=W/2,shadow=sh)
    return lay
