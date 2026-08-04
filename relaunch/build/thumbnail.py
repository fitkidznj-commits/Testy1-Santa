#!/usr/bin/env python3
"""Thumbnail (1920x1080): logo + 'Same Shack. Same Soul. New Chapter.'"""
import os
from PIL import Image, ImageDraw
import art, layers as C

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"out"); os.makedirs(OUT,exist_ok=True)
W,H=1920,1080

def build():
    img=art.sky_water(W,H,"hero",0.66)
    img=art.add_sun(img,int(W*0.5),int(H*0.30),int(H*0.10))
    img=art.sun_glints(img,int(H*0.66),int(W*0.5))
    img=art.palm(img,int(W*0.06),int(H*1.02),H/1080*1.5,flip=True)
    img=art.palm(img,int(W*0.95),int(H*1.04),H/1080*1.5)
    img=art.boat(img,int(W*0.72),int(H*0.66),0.7)
    img=art.gull(img,int(W*0.3),int(H*0.14),1.1); img=art.gull(img,int(W*0.34),int(H*0.18),0.8)
    img=art.light_leak(img,"tr",strength=0.4)
    img=art.scrim(img,top=0.30,bottom=0.42)
    img=art.finish(img,grain=6,seed=21,vignette=0.36)
    img=img.convert("RGBA")
    lg=art.logo_lockup(1.10,dark_text=False)
    img.alpha_composite(lg,((W-lg.width)//2,int(H*0.47)-lg.height//2))
    d=ImageDraw.Draw(img)
    # DDD text badge (TEXT only — no Guy Fieri image / no clips)
    fb=art.font("BebasNeue-Regular.ttf",int(H*0.030))
    badge="AS SEEN ON  ‘DINERS, DRIVE-INS & DIVES’"
    bw=C.tracked_width(d,badge,fb,int(H*0.006))
    bx=(W-bw)//2; by=int(H*0.045)
    d.rounded_rectangle([bx-26,by-12,bx+bw+26,by+int(H*0.030)+12],radius=18,
                        outline=(255,206,120),width=3,fill=(0,0,0,70))
    C.draw_tracked(d,bx,by,badge,fb,(255,206,120,255),int(H*0.006))
    # tagline
    C.draw_tracked(d,0,int(H*0.86),"SAME SHACK.  SAME SOUL.  NEW CHAPTER.",
                   art.font("Anton-Regular.ttf",int(H*0.066)),(255,250,238,255),2,
                   anchor_center=W/2,shadow=(3,4,(0,0,0,170)))
    out=os.path.join(OUT,"thumbnail_same_shack_same_soul.png")
    img.convert("RGB").save(out); print("DONE:",out)

if __name__=="__main__": build()
