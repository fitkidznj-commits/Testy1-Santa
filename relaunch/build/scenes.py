#!/usr/bin/env python3
"""Scene plate builders (oversized for Ken Burns). Reused by all deliverables."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
import art

def _radial_warm(PW,PH, center=(0.5,0.42), inner=(78,58,52), outer=(22,18,24)):
    yy,xx=np.mgrid[0:PH,0:PW]
    cx,cy=center[0]*PW,center[1]*PH
    d=np.sqrt(((xx-cx)/(PW*0.72))**2+((yy-cy)/(PH*0.72))**2)
    d=np.clip(d,0,1)[...,None]
    arr=np.array(inner)*(1-d)+np.array(outer)*d
    return Image.fromarray(arr.astype(np.uint8))

def plate_hook(PW,PH):
    img=art.sky_water(PW,PH,"dawn",0.64)
    img=art.add_sun(img,int(PW*0.74),int(PH*0.30),int(PH*0.085))
    img=art.sun_glints(img,int(PH*0.64),int(PW*0.74))
    img=art.boat(img,int(PW*0.30),int(PH*0.64),PH/1080*1.0)
    img=art.palm(img,int(PW*0.93),int(PH*0.99),PH/1080*1.5)
    img=art.palm(img,int(PW*0.05),int(PH*1.03),PH/1080*1.25,flip=True)
    img=art.gull(img,int(PW*0.52),int(PH*0.17),1.1); img=art.gull(img,int(PW*0.57),int(PH*0.21),0.8)
    img=art.light_leak(img,"tr",strength=0.45)
    img=art.scrim(img,top=0.30,bottom=0.46)
    return art.finish(img,grain=6,seed=3,vignette=0.34)

def plate_legacy(PW,PH):
    img=art.sky_water(PW,PH,"sunset",0.60)
    img=art.add_sun(img,int(PW*0.22),int(PH*0.34),int(PH*0.075))
    img=art.sun_glints(img,int(PH*0.60),int(PW*0.22))
    img=art.hut(img,int(PW*0.66),int(PH*0.66),PH/1080*1.05)
    img=art.piling(img,int(PW*0.12),int(PH*0.52),int(PH*0.70),PH/1080*1.1,bird=True)
    img=art.piling(img,int(PW*0.20),int(PH*0.56),int(PH*0.70),PH/1080*0.9)
    img=art.palm(img,int(PW*0.90),int(PH*1.0),PH/1080*1.35)
    img=art.gull(img,int(PW*0.42),int(PH*0.16),1.0)
    img=art.light_leak(img,"tl",strength=0.4)
    img=art.scrim(img,top=0.16,bottom=0.5)
    return art.finish(img,grain=7,seed=5,vignette=0.36,warm=1.2)

def plate_owner(PW,PH):
    img=art.sky_water(PW,PH,"day",0.62)
    img=art.add_sun(img,int(PW*0.80),int(PH*0.22),int(PH*0.07),glow=0.8)
    img=art.hut(img,int(PW*0.40),int(PH*0.68),PH/1080*1.12)
    img=art.person(img,int(PW*0.40),int(PH*0.68),PH/1080*1.15,color=(18,30,34))
    img=art.palm(img,int(PW*0.08),int(PH*1.0),PH/1080*1.3,flip=True)
    img=art.palm(img,int(PW*0.95),int(PH*1.02),PH/1080*1.2)
    img=art.boat(img,int(PW*0.74),int(PH*0.60),PH/1080*0.8)
    img=art.gull(img,int(PW*0.6),int(PH*0.15),1.0)
    img=art.light_leak(img,"tr",strength=0.35)
    img=art.scrim(img,top=0.18,bottom=0.5)
    return art.finish(img,grain=6,seed=8,vignette=0.32)

def plate_food(PW,PH,kind):
    bg=_radial_warm(PW,PH)
    d=ImageDraw.Draw(bg,"RGBA")
    for x in range(0,PW,int(PW*0.08)):
        d.line([x,0,x,PH], fill=(0,0,0,32), width=3)            # planks
    card=art.food_card("",kind, w=900,h=1100)
    ch=int(PH*0.82); cw=int(ch*900/1100)
    card=card.resize((cw,ch), Image.LANCZOS)
    cx=(PW-cw)//2; cy=int(PH*0.07)
    sh=Image.new("RGBA",(PW,PH),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.ellipse([cx+20,cy+ch-70,cx+cw-20,cy+ch+40], fill=(0,0,0,120))
    sh=sh.filter(ImageFilter.GaussianBlur(30))
    bg=Image.alpha_composite(bg.convert("RGBA"),sh)
    bg.alpha_composite(card.convert("RGBA"),(cx,cy))
    bg=bg.convert("RGB")
    # coral keyline
    d2=ImageDraw.Draw(bg); d2.rectangle([cx,cy,cx+cw,cy+ch], outline=(232,92,66), width=5)
    bg=art.light_leak(bg,"tr",color=(255,180,120),strength=0.3)
    bg=art.scrim(bg,top=0.12,bottom=0.30)
    return art.finish(bg,grain=8,seed=hash(kind)%97,vignette=0.40,warm=1.15)

def plate_community(PW,PH):
    img=art.sky_water(PW,PH,"golden",0.60)
    img=art.add_sun(img,int(PW*0.5),int(PH*0.26),int(PH*0.08))
    img=art.sun_glints(img,int(PH*0.60),int(PW*0.5))
    img=art.hut(img,int(PW*0.5),int(PH*0.64),PH/1080*1.0)
    for i,xx in enumerate([0.30,0.36,0.62,0.68,0.72]):
        img=art.person(img,int(PW*xx),int(PH*0.70),PH/1080*(0.95+0.1*(i%2)),color=(16,26,30))
    img=art.palm(img,int(PW*0.07),int(PH*1.0),PH/1080*1.3,flip=True)
    img=art.palm(img,int(PW*0.94),int(PH*1.02),PH/1080*1.3)
    img=art.gull(img,int(PW*0.4),int(PH*0.14),1.0); img=art.gull(img,int(PW*0.44),int(PH*0.18),0.8)
    img=art.light_leak(img,"tr",strength=0.4)
    img=art.scrim(img,top=0.18,bottom=0.5)
    return art.finish(img,grain=7,seed=11,vignette=0.34,warm=1.15)

def plate_cta(PW,PH):
    img=art.sky_water(PW,PH,"hero",0.66)
    img=art.add_sun(img,int(PW*0.5),int(PH*0.32),int(PH*0.09))
    img=art.sun_glints(img,int(PH*0.66),int(PW*0.5))
    img=art.palm(img,int(PW*0.06),int(PH*1.02),PH/1080*1.5,flip=True)
    img=art.palm(img,int(PW*0.95),int(PH*1.04),PH/1080*1.5)
    img=art.boat(img,int(PW*0.72),int(PH*0.66),PH/1080*0.7)
    img=art.gull(img,int(PW*0.3),int(PH*0.15),1.0)
    img=art.light_leak(img,"tr",strength=0.4)
    img=art.scrim(img,top=0.34,bottom=0.5)
    return art.finish(img,grain=6,seed=14,vignette=0.36)
