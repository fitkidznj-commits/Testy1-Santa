#!/usr/bin/env python3
"""Synthesized warm 'island' music bed — original, royalty-free by construction.
Light ukulele/marimba arpeggio + soft pad + gentle shaker. Major-key, feel-good."""
import numpy as np

SR = 44100

def _note(freq, dur, sr=SR):
    return np.arange(int(dur*sr))/sr, freq

def pluck(freq, dur, sr=SR, amp=0.5, bright=1.0):
    """Marimba/uke-ish pluck: harmonics with fast exp decay."""
    t = np.arange(int(dur*sr))/sr
    env = np.exp(-t*5.5)
    body = (np.sin(2*np.pi*freq*t)
            + 0.5*bright*np.sin(2*np.pi*2*freq*t)*np.exp(-t*9)
            + 0.25*bright*np.sin(2*np.pi*3*freq*t)*np.exp(-t*13))
    # soft attack
    a = np.minimum(1, t/0.004)
    return amp*env*a*body

def pad(freqs, dur, sr=SR, amp=0.16):
    t = np.arange(int(dur*sr))/sr
    atk = np.minimum(1, t/0.35); rel = np.minimum(1,(dur-t)/0.5)
    env = atk*np.clip(rel,0,1)
    sig = np.zeros_like(t)
    for f in freqs:
        sig += np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*1.005*t)  # slight detune
    vib = 1+0.004*np.sin(2*np.pi*5*t)
    return amp*env*sig/len(freqs)*vib

def shaker(dur, sr=SR, amp=0.06):
    n = int(dur*sr); t=np.arange(n)/sr
    noise = np.random.default_rng(1).normal(0,1,n)
    noise = noise - np.concatenate([[0],noise[:-1]])   # crude highpass
    env = np.exp(-((t%1.0))*30)  # placeholder, replaced by caller env
    return amp*noise

NOTES = {  # freqs
 'C3':130.81,'E3':164.81,'G3':196.0,'A2':110.0,'F3':174.61,'C4':261.63,'D4':293.66,
 'E4':329.63,'G4':392.0,'A3':220.0,'A4':440.0,'F4':349.23,'B3':246.94,'D3':146.83,
 'G2':98.0,'C2':65.41,'F2':87.31,
}

def make_music(duration, sr=SR):
    total = int(duration*sr)
    out = np.zeros(total, np.float32)
    bpm = 96; beat = 60/bpm; bar = beat*4
    # progression C - G - Am - F (warm, hopeful)
    prog = [
        (['C3','E3','G3','C4'], 'C2'),
        (['B3','D4','G3','G4'], 'G2'),
        (['A3','C4','E4','A4'], 'A2'),
        (['F3','A3','C4','F4'], 'F2'),
    ]
    rng = np.random.default_rng(3)
    bar_i = 0; t = 0.0
    while t < duration + bar:
        chord_names, bassname = prog[bar_i % 4]
        freqs = [NOTES[n] for n in chord_names]
        # pad
        seg = pad(freqs, bar*1.02, sr)
        s0 = int(t*sr)
        e0 = min(total, s0+len(seg))
        if s0 < total: out[s0:e0] += seg[:e0-s0]
        # bass on beat 1 and 3
        for bt in (0,2):
            b = pluck(NOTES[bassname], beat*1.4, sr, amp=0.32, bright=0.4)
            ss=int((t+bt*beat)*sr); ee=min(total,ss+len(b))
            if ss<total: out[ss:ee]+=b[:ee-ss]
        # arpeggio: gentle 8th-note pattern across the chord
        pattern=[0,2,1,3,2,1,3,2]
        for k,step in enumerate(pattern):
            f=freqs[step % len(freqs)]*2  # up an octave, sparkle
            if rng.random()<0.12: continue
            p=pluck(f, beat*0.9, sr, amp=0.22*(0.8+0.4*rng.random()), bright=1.0)
            ss=int((t+k*beat*0.5)*sr); ee=min(total,ss+len(p))
            if ss<total: out[ss:ee]+=p[:ee-ss]
        # shaker on offbeats
        for k in range(8):
            if k%2==1:
                n=int(beat*0.5*sr); tt=np.arange(n)/sr
                env=np.exp(-tt*38)
                nz=rng.normal(0,1,n); nz=nz-np.concatenate([[0],nz[:-1]])
                sh=0.05*env*nz
                ss=int((t+k*beat*0.5)*sr); ee=min(total,ss+len(sh))
                if ss<total: out[ss:ee]+=sh[:ee-ss].astype(np.float32)
        t += bar; bar_i += 1
    # gentle master: soft clip + normalize
    out = np.tanh(out*1.1)
    out /= max(1e-6, np.max(np.abs(out)))
    out *= 0.75
    # subtle stereo widening
    left = out.copy(); right = out.copy()
    d=int(0.008*sr)
    right[d:]=out[:-d]
    stereo=np.stack([left,right],axis=1).astype(np.float32)
    # soft fade in/out
    f=int(1.2*sr)
    stereo[:f]*=np.linspace(0,1,f)[:,None]
    stereo[-f:]*=np.linspace(1,0,f)[:,None]
    return stereo, sr

if __name__=="__main__":
    import soundfile as sf, sys
    dur=float(sys.argv[1]) if len(sys.argv)>1 else 80
    s,sr=make_music(dur); sf.write(sys.argv[2] if len(sys.argv)>2 else "build/music_test.wav", s, sr)
    print("music written", s.shape, sr)
