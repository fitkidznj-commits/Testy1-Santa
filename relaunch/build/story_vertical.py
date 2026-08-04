#!/usr/bin/env python3
"""Build the 30s vertical reel (1080x1920) for Instagram / Facebook."""
import os
from PIL import Image
import art, scenes, layers as C, engine, audio_master

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO=os.path.join(ROOT,"build","vo_reel")
OUT=os.path.join(ROOT,"out"); os.makedirs(OUT,exist_ok=True)
W,H=1080,1920; FPS=30; OS=1.16
PW,PH=int(W*OS),int(H*OS)

def F(name,size): return art.font(name,int(H*size))
def place_logo(scale,cy):
    lg=art.logo_lockup(scale,dark_text=False)
    lay=Image.new("RGBA",(W,H),(0,0,0,0))
    lay.alpha_composite(lg,((W-lg.width)//2,int(H*cy)-lg.height//2)); return lay

def build():
    print("vertical plates...")
    p_hook=scenes.plate_hook(PW,PH); p_leg=scenes.plate_legacy(PW,PH)
    p_own=scenes.plate_owner(PW,PH); p_cta=scenes.plate_cta(PW,PH)
    foods=[("THE FAMOUS","SHRIMP FRITTERS","fritters",2.3),
           ("LOW-COUNTRY","SHRIMP & GRITS","grits",2.2),
           ("OFF THE BOAT","FRESH CATCH","fish",2.2),
           ("ICE-COLD","KEY LIME PIE","pie",2.3)]
    fp={k:scenes.plate_food(PW,PH,k) for _,_,k,_ in foods}
    logo_scale=0.74
    shots=[]
    # hook
    ov=[{'layer':place_logo(logo_scale,0.40),'t_in':0.3,'dur':4.2,'fade':0.6,'anim':'pop'},
        {'layer':C.caption(W,H,[{'text':'THE SHACK','font':F("Anton-Regular.ttf",0.075),'color':C.CREAM,'track':2},
                                {'text':'LIVES ON','font':F("Anton-Regular.ttf",0.075),'color':C.GOLD,'track':2}],
            int(H*0.66),gap=int(H*0.005)),'t_in':1.4,'dur':3.0,'fade':0.5,'anim':'rise','rise':36}]
    shots.append(engine.Shot(4.5,p_hook,(0.9,1.0,(0.5,0.5),(0.5,0.46)),ov))
    # legacy
    ov=[{'layer':C.caption(W,H,[{'text':'SAME KEYS SOUL.','font':F("Anton-Regular.ttf",0.062),'color':C.CREAM,'track':2},
                                {'text':'SAME FAMOUS FLAVOR.','font':F("Anton-Regular.ttf",0.062),'color':C.GOLD,'track':2}],
            int(H*0.5),gap=int(H*0.012)),'t_in':0.6,'dur':4.0,'fade':0.5,'anim':'rise','rise':36}]
    shots.append(engine.Shot(5.0,p_leg,(1.0,0.9,(0.5,0.5),(0.55,0.52)),ov))
    # owner
    ov=[{'layer':C.script_line(W,H,"David Epstein",0.072,int(H*0.42),C.CREAM),'t_in':0.5,'dur':4.2,'fade':0.5,'anim':'rise','rise':28},
        {'layer':C.caption(W,H,[{'text':'LOCAL OWNER.','font':F("Anton-Regular.ttf",0.058),'color':C.GOLD,'track':2},
                                {'text':'AT THE HELM.','font':F("Anton-Regular.ttf",0.058),'color':C.CREAM,'track':2}],
            int(H*0.56),gap=int(H*0.012)),'t_in':1.6,'dur':3.2,'fade':0.5,'anim':'rise','rise':30}]
    shots.append(engine.Shot(5.0,p_own,(0.92,0.84,(0.45,0.5),(0.45,0.55)),ov))
    # food
    for kick,title,kind,dur in foods:
        ov=[{'layer':C.lower_third(W,H,kick,title,y=int(H*0.72)),'t_in':0.2,'dur':dur-0.35,'fade':0.28,'anim':'rise','rise':26}]
        shots.append(engine.Shot(dur,fp[kind],(1.02,0.94,(0.5,0.5),(0.5,0.5)),ov))
    # cta
    ov=[{'layer':place_logo(logo_scale,0.40),'t_in':0.4,'dur':5.4,'fade':0.6,'anim':'pop'},
        {'layer':C.caption(W,H,[{'text':'81901 OVERSEAS HWY','font':F("BebasNeue-Regular.ttf",0.034),'color':C.GOLD,'track':int(H*0.004)},
                                {'text':'ISLAMORADA, FL','font':F("BebasNeue-Regular.ttf",0.034),'color':C.GOLD,'track':int(H*0.004)}],
            int(H*0.62),gap=2),'t_in':2.0,'dur':3.8,'fade':0.5,'anim':'rise','rise':22},
        {'layer':C.caption(W,H,[{'text':'SAME SHACK. SAME SOUL.','font':F("Anton-Regular.ttf",0.05),'color':C.CREAM,'track':1},
                                {'text':'NEW CHAPTER.','font':F("Anton-Regular.ttf",0.05),'color':C.GOLD,'track':1}],
            int(H*0.73),gap=int(H*0.008)),'t_in':3.0,'dur':3.0,'fade':0.5,'anim':'rise','rise':26}]
    shots.append(engine.Shot(6.0,p_cta,(1.0,0.9,(0.5,0.5),(0.5,0.46)),ov))

    starts=[]; t=0
    for s in shots: starts.append(t); t+=s.dur
    total=t
    vo=[(starts[0]+0.4,f"{VO}/r1.wav"),(starts[1]+0.4,f"{VO}/r2.wav"),
        (starts[2]+0.3,f"{VO}/r3.wav"),(starts[3]+0.2,f"{VO}/r4.wav"),
        (starts[7]+0.3,f"{VO}/r5.wav")]
    print(f"reel total {total:.1f}s; audio...")
    am=os.path.join(ROOT,"build","master_reel.wav"); audio_master.build(total,vo,am)
    out=os.path.join(OUT,"shrimp_shack_relaunch_reel_vertical_1080x1920.mp4")
    print("rendering reel..."); engine.render(shots,out,am,W,H,FPS); print("DONE:",out)

if __name__=="__main__": build()
