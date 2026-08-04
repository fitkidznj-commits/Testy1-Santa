#!/usr/bin/env python3
"""Build the MAIN ~70s horizontal relaunch film (1920x1080)."""
import os, sys, json
from PIL import Image
import art, scenes, layers, engine, audio_master

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO=os.path.join(ROOT,"build","vo")
OUT=os.path.join(ROOT,"out"); os.makedirs(OUT,exist_ok=True)

W,H=1920,1080; FPS=30; OS=1.18
PW,PH=int(W*OS),int(H*OS)
C=layers

def place_logo(scale, cy_frac, dark=False):
    lg=art.logo_lockup(scale, dark_text=dark)
    lay=Image.new("RGBA",(W,H),(0,0,0,0))
    lay.alpha_composite(lg,((W-lg.width)//2, int(H*cy_frac)-lg.height//2))
    return lay

def F(name,size): return art.font(name,int(H*size))

def build():
    print("plates...")
    p_hook=scenes.plate_hook(PW,PH)
    p_leg=scenes.plate_legacy(PW,PH)
    p_own=scenes.plate_owner(PW,PH)
    p_comm=scenes.plate_community(PW,PH)
    p_cta=scenes.plate_cta(PW,PH)
    foods=[("THE FAMOUS","SHRIMP FRITTERS","fritters",3.2),
           ("LOW-COUNTRY","SHRIMP & GRITS","grits",2.6),
           ("HOUSE-SMOKED","SMOKED FISH DIP","dip",2.6),
           ("STRAIGHT OFF THE BOAT","FRESH CATCH","fish",2.8),
           ("KEYS CLASSIC","CONCH FRITTERS","conch",2.4),
           ("ICE-COLD","KEY LIME PIE","pie",2.8)]
    food_plates={k:scenes.plate_food(PW,PH,k) for _,_,k,_ in foods}

    shots=[]
    # ---- 1 HOOK
    ov=[{'layer':place_logo(1.02,0.40),'t_in':0.4,'dur':7.4,'fade':0.7,'anim':'pop'},
        {'layer':C.caption(W,H,[{'text':'THE SHACK LIVES ON','font':F("Anton-Regular.ttf",0.090),
            'color':C.CREAM,'track':3}], int(H*0.80)),'t_in':2.6,'dur':5.2,'fade':0.6,'anim':'rise','rise':40}]
    shots.append(engine.Shot(8.0,p_hook,(0.86,1.0,(0.5,0.46),(0.5,0.5)),ov))
    # ---- 2 LEGACY
    ov=[{'layer':C.script_line(W,H,"Same Keys soul.",0.090,int(H*0.40),C.GOLD),
            't_in':1.0,'dur':4.6,'fade':0.6,'anim':'rise','rise':30},
        {'layer':C.caption(W,H,[{'text':'SAME LOCAL FLAVOR.','font':F("Anton-Regular.ttf",0.085),
            'color':C.CREAM,'track':3}], int(H*0.78)),'t_in':5.2,'dur':5.4,'fade':0.6,'anim':'rise','rise':40}]
    shots.append(engine.Shot(11.0,p_leg,(1.0,0.87,(0.42,0.5),(0.6,0.52)),ov))
    # ---- 3 OWNER
    ov=[{'layer':C.caption(W,H,[{'text':'A LOCAL KEYS KID','font':F("BebasNeue-Regular.ttf",0.045),
            'color':C.GOLD,'track':int(H*0.012)}], int(H*0.30)),'t_in':1.0,'dur':9.0,'fade':0.5,'anim':'rise','rise':24},
        {'layer':C.script_line(W,H,"David Epstein",0.105,int(H*0.42),C.CREAM),
            't_in':1.4,'dur':8.6,'fade':0.6,'anim':'rise','rise':30},
        {'layer':C.caption(W,H,[{'text':'TAKES THE HELM','font':F("Anton-Regular.ttf",0.078),
            'color':C.CREAM,'track':3}], int(H*0.80)),'t_in':4.8,'dur':5.6,'fade':0.6,'anim':'rise','rise':40}]
    shots.append(engine.Shot(11.0,p_own,(0.95,0.82,(0.4,0.5),(0.42,0.56)),ov))
    # ---- FOOD montage
    first=True
    for kick,title,kind,dur in foods:
        ov=[{'layer':C.lower_third(W,H,kick,title),'t_in':0.25,'dur':dur-0.45,'fade':0.30,'anim':'rise','rise':30}]
        if first:
            ov.append({'layer':C.caption(W,H,[{'text':'THE FAVORITES ARE STAYING','font':F("BebasNeue-Regular.ttf",0.046),
                'color':C.GOLD,'track':int(H*0.012)}], int(H*0.13)),'t_in':0.3,'dur':2.7,'fade':0.4,'anim':'rise','rise':20})
            first=False
        shots.append(engine.Shot(dur,food_plates[kind],(1.02,0.93,(0.5,0.5),(0.5,0.5)),ov))
    # ---- 5 COMMUNITY
    ov=[{'layer':C.caption(W,H,[
            {'text':'LOCALS.  VISITORS.','font':F("Anton-Regular.ttf",0.072),'color':C.CREAM,'track':3},
            {'text':'FAMILIES.  FRIENDS.','font':F("Anton-Regular.ttf",0.072),'color':C.GOLD,'track':3}],
            int(H*0.42),gap=int(H*0.02)),'t_in':1.2,'dur':8.6,'fade':0.6,'anim':'rise','rise':40}]
    shots.append(engine.Shot(10.5,p_comm,(0.9,1.0,(0.6,0.5),(0.42,0.5)),ov))
    # ---- 6 CTA
    ov=[{'layer':C.script_line(W,H,"Come celebrate the next chapter",0.058,int(H*0.16),C.CREAM),
            't_in':0.6,'dur':11.8,'fade':0.7,'anim':'rise','rise':24},
        {'layer':place_logo(0.72,0.45),'t_in':1.4,'dur':11.0,'fade':0.7,'anim':'pop'},
        {'layer':C.caption(W,H,[{'text':'81901 OVERSEAS HWY  •  ISLAMORADA, FL  •  MM 81.9',
            'font':F("BebasNeue-Regular.ttf",0.046),'color':C.GOLD,'track':int(H*0.008)}], int(H*0.79)),
            't_in':5.0,'dur':7.5,'fade':0.6,'anim':'rise','rise':24},
        {'layer':C.caption(W,H,[{'text':'SAME SHACK.  SAME SOUL.  NEW CHAPTER.',
            'font':F("Anton-Regular.ttf",0.058),'color':C.CREAM,'track':2}], int(H*0.88)),
            't_in':6.8,'dur':5.8,'fade':0.6,'anim':'rise','rise':30}]
    shots.append(engine.Shot(13.0,p_cta,(1.0,0.88,(0.5,0.5),(0.5,0.46)),ov))

    # ---- audio timeline
    starts=[]; t=0
    for s in shots: starts.append(t); t+=s.dur
    total=t
    # shot indices: 0 hook,1 legacy,2 owner,3..8 food,9 community,10 cta
    vo=[(starts[0]+0.6, f"{VO}/s1.wav"),
        (starts[1]+0.7, f"{VO}/s2.wav"),
        (starts[2]+0.7, f"{VO}/s3.wav"),
        (starts[3]+0.3, f"{VO}/s4.wav"),
        (starts[9]+0.7, f"{VO}/s5.wav"),
        (starts[10]+0.7,f"{VO}/s6.wav")]
    print(f"total {total:.1f}s ; building audio...")
    amaster=os.path.join(ROOT,"build","master_main.wav")
    audio_master.build(total, vo, amaster)
    print("rendering video...")
    out=os.path.join(OUT,"shrimp_shack_relaunch_main_1080p.mp4")
    engine.render(shots,out,amaster,W,H,FPS)
    print("DONE:",out)

if __name__=="__main__":
    build()
