#!/usr/bin/env python3
"""Assemble the master audio track: place VO segments on a timeline and
duck a synthesized music bed beneath the narration."""
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
import music as M

SR=44100

def _to_sr(x, sr):
    if sr==SR: return x
    from math import gcd
    g=gcd(int(sr),SR)
    return resample_poly(x, SR//g, sr//g)

def build(total_dur, vo_items, out_path, music_gain=0.9, duck_gain=0.30):
    """vo_items: list of (start_sec, wav_path). Returns master written to out_path."""
    n=int(total_dur*SR)
    vo=np.zeros(n, np.float32)
    present=np.zeros(n, np.float32)
    for start,path in vo_items:
        x,sr=sf.read(path, dtype='float32')
        if x.ndim>1: x=x.mean(1)
        x=_to_sr(x,sr).astype(np.float32)
        # gentle level + tiny head/tail fade
        x*=1.0
        fz=int(0.02*SR); x[:fz]*=np.linspace(0,1,fz); x[-fz:]*=np.linspace(1,0,fz)
        s=int(start*SR); e=min(n,s+len(x))
        if s<n:
            vo[s:e]+=x[:e-s]
            present[s:e]=1.0
    # smooth the duck envelope (attack/release)
    env=present.copy()
    # release: extend presence a bit so music stays low briefly after words
    win=int(0.18*SR)
    k=np.ones(win)/win
    env=np.convolve(env,k,mode='same')
    env=np.clip(env,0,1)
    duck=music_gain*(1-env)+duck_gain*env  # gain for music
    mus,_=M.make_music(total_dur, SR)   # stereo
    musL=mus[:n,0]*duck; musR=mus[:n,1]*duck
    voS=vo*1.12
    left=np.tanh(musL+voS); right=np.tanh(musR+voS)
    out=np.stack([left,right],1).astype(np.float32)
    # master fade
    f=int(0.6*SR); out[:f]*=np.linspace(0,1,f)[:,None]; out[-f:]*=np.linspace(1,0,f)[:,None]
    sf.write(out_path,out,SR)
    return out_path

if __name__=="__main__":
    import sys,json
    print("audio_master module")
