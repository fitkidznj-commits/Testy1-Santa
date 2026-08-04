#!/usr/bin/env python3
"""Build the 15s teaser (1920x1080) — hero line 'The Shack lives on.'"""
import os
from PIL import Image
import art, scenes, layers as C, engine, audio_master

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO=os.path.join(ROOT,"build","vo_teaser")
OUT=os.path.join(ROOT,"out"); os.makedirs(OUT,exist_ok=True)
W,H=1920,1080; FPS=30; OS=1.18
PW,PH=int(W*OS),int(H*OS)
def F(name,size): return art.font(name,int(H*size))
def place_logo(scale,cy):
    lg=art.logo_lockup(scale,dark_text=False)
    lay=Image.new("RGBA",(W,H),(0,0,0,0))
    lay.alpha_composite(lg,((W-lg.width)//2,int(H*cy)-lg.height//2)); return lay

def build():
    print("teaser plates...")
    p_hook=scenes.plate_hook(PW,PH); p_cta=scenes.plate_cta(PW,PH)
    shots=[]
    # 1: the hero line
    ov=[{'layer':C.caption(W,H,[{'text':'THE SHACK','font':F("Anton-Regular.ttf",0.135),'color':C.CREAM,'track':3},
                                {'text':'LIVES ON','font':F("Anton-Regular.ttf",0.135),'color':C.GOLD,'track':3}],
            int(H*0.46),gap=int(H*0.005)),'t_in':0.5,'dur':5.2,'fade':0.7,'anim':'rise','rise':46},
        {'layer':C.caption(W,H,[{'text':'ISLAMORADA  •  FLORIDA KEYS','font':F("BebasNeue-Regular.ttf",0.040),
            'color':C.GOLD,'track':int(H*0.012)}], int(H*0.70)),'t_in':1.6,'dur':4.0,'fade':0.6,'anim':'rise','rise':24}]
    shots.append(engine.Shot(6.0,p_hook,(0.86,1.0,(0.5,0.5),(0.5,0.46)),ov))
    # 2: brand + chapter + owner + address
    ov=[{'layer':place_logo(0.74,0.42),'t_in':0.4,'dur':8.6,'fade':0.7,'anim':'pop'},
        {'layer':C.script_line(W,H,"Same soul, new chapter.",0.058,int(H*0.16),C.CREAM),
            't_in':1.0,'dur':8.0,'fade':0.6,'anim':'rise','rise':24},
        {'layer':C.caption(W,H,[{'text':'NOW WITH LOCAL OWNER DAVID EPSTEIN','font':F("BebasNeue-Regular.ttf",0.042),
            'color':C.GOLD,'track':int(H*0.008)}], int(H*0.78)),'t_in':3.4,'dur':5.4,'fade':0.6,'anim':'rise','rise':24},
        {'layer':C.caption(W,H,[{'text':'81901 OVERSEAS HWY  •  ISLAMORADA, FL','font':F("BebasNeue-Regular.ttf",0.040),
            'color':C.CREAM,'track':int(H*0.006)}], int(H*0.87)),'t_in':4.6,'dur':4.2,'fade':0.6,'anim':'rise','rise':20}]
    shots.append(engine.Shot(9.0,p_cta,(1.0,0.9,(0.5,0.5),(0.5,0.47)),ov))

    starts=[]; t=0
    for s in shots: starts.append(t); t+=s.dur
    total=t
    vo=[(starts[0]+0.8,f"{VO}/t1.wav"),(starts[1]+0.5,f"{VO}/t2.wav")]
    print(f"teaser total {total:.1f}s; audio...")
    am=os.path.join(ROOT,"build","master_teaser.wav"); audio_master.build(total,vo,am)
    out=os.path.join(OUT,"shrimp_shack_relaunch_teaser_15s_1080p.mp4")
    print("rendering teaser..."); engine.render(shots,out,am,W,H,FPS); print("DONE:",out)

if __name__=="__main__": build()
