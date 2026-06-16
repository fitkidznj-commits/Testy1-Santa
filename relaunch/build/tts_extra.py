#!/usr/bin/env python3
"""VO for the 30s vertical reel and 15s teaser."""
import os, json
from tts import make_tts, synth
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REEL={
 "r1":("Islamorada... the Shrimp Shack lives on.",0.97),
 "r2":("Same Keys soul. Same famous flavor.",0.98),
 "r3":("Now with local owner David Epstein at the helm.",0.98),
 "r4":("The favorites are staying. Shrimp fritters, shrimp and grits, "
       "fresh catch, and Key lime pie.",1.0),
 "r5":("Same Shack. Same soul. New chapter. Come celebrate with us.",0.97),
}
TEASER={
 "t1":("The Shack lives on.",0.95),
 "t2":("The Islamorada Shrimp Shack. Same soul, new chapter, "
       "with local owner David Epstein.",0.98),
}

if __name__=="__main__":
    tts=make_tts("female")
    for grp,outdir in [(REEL,"vo_reel"),(TEASER,"vo_teaser")]:
        od=os.path.join(ROOT,"build",outdir); os.makedirs(od,exist_ok=True)
        meta={}
        for k,(txt,spd) in grp.items():
            d=synth(tts,txt,os.path.join(od,f"{k}.wav"),speed=spd); meta[k]=round(d,3)
            print(outdir,k,f"{d:.2f}s")
        json.dump(meta,open(os.path.join(od,"durations.json"),"w"),indent=2)
