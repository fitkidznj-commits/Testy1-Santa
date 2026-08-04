#!/usr/bin/env python3
"""Frame engine: Ken Burns over scene plates + timed caption/overlay animation,
piped straight into ffmpeg with a pre-mixed audio track."""
import os, sys, subprocess, math
import numpy as np
from PIL import Image
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()

def smooth(x):
    x = max(0.0, min(1.0, x)); return x*x*(3-2*x)

class Shot:
    def __init__(self, dur, plate, kb=(0.88,1.0,(0.5,0.5),(0.5,0.5)), overlays=None):
        self.dur=dur; self.plate=plate; self.kb=kb; self.overlays=overlays or []

def _kb_frame(plate, W, H, f0, f1, c0, c1, p):
    """Crop a window (fraction f of plate) at moving center, resize to WxH."""
    PW,PH=plate.size
    f=f0+(f1-f0)*smooth(p)
    cx=c0[0]+(c1[0]-c0[0])*smooth(p); cy=c0[1]+(c1[1]-c0[1])*smooth(p)
    cw=PW*f; ch=PH*f
    # keep output aspect
    ar=W/H
    if cw/ch>ar: cw=ch*ar
    else: ch=cw/ar
    x0=cx*PW-cw/2; y0=cy*PH-ch/2
    x0=max(0,min(PW-cw,x0)); y0=max(0,min(PH-ch,y0))
    crop=plate.crop((int(x0),int(y0),int(x0+cw),int(y0+ch)))
    return crop.resize((W,H), Image.LANCZOS)

def _apply_overlay(base, ov, t):
    t_in=ov['t_in']; dur=ov['dur']; fade=ov.get('fade',0.4)
    if t<t_in or t>t_in+dur: return base
    local=t-t_in
    a_in=smooth(local/fade) if fade>0 else 1.0
    a_out=smooth((dur-local)/fade) if fade>0 else 1.0
    alpha=min(a_in,a_out)
    layer=ov['layer']; anim=ov.get('anim','fade')
    yoff=0
    if anim in ('rise','rise_hold'):
        yoff=int((1-smooth(min(1,local/max(0.001,fade))))*ov.get('rise',36))
    if anim=='pop':
        s=0.94+0.06*smooth(min(1,local/max(0.001,fade)))
        nl=layer.resize((int(layer.width*s),int(layer.height*s)), Image.LANCZOS)
        lay=Image.new("RGBA",base.size,(0,0,0,0))
        lay.alpha_composite(nl,((base.width-nl.width)//2,(base.height-nl.height)//2))
        layer=lay
    if alpha<=0: return base
    if alpha<1.0 or yoff:
        arr=np.asarray(layer).astype(np.float32).copy()
        arr[...,3]*=alpha
        layer=Image.fromarray(arr.astype(np.uint8))
    if yoff:
        shifted=Image.new("RGBA",base.size,(0,0,0,0))
        shifted.alpha_composite(layer,(0,yoff))
        layer=shifted
    base.alpha_composite(layer)
    return base

def render(shots, out_path, audio_wav=None, W=1920, H=1080, fps=30, vignette_pulse=False):
    total_frames=sum(int(round(s.dur*fps)) for s in shots)
    cmd=[FF,"-y","-hide_banner","-loglevel","error",
         "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(fps),"-i","-"]
    if audio_wav: cmd+=["-i",audio_wav]
    cmd+=["-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r",str(fps)]
    if audio_wav: cmd+=["-c:a","aac","-b:a","192k","-shortest"]
    cmd+=["-movflags","+faststart",out_path]
    proc=subprocess.Popen(cmd, stdin=subprocess.PIPE)
    done=0
    for s in shots:
        nf=int(round(s.dur*fps))
        f0,f1,c0,c1=s.kb
        for i in range(nf):
            p=i/max(1,nf-1)
            frame=_kb_frame(s.plate,W,H,f0,f1,c0,c1,p).convert("RGBA")
            t=p*s.dur
            for ov in s.overlays:
                _apply_overlay(frame, ov, t)
            proc.stdin.write(frame.convert("RGB").tobytes())
            done+=1
        sys.stderr.write(f"\r  frames {done}/{total_frames}"); sys.stderr.flush()
    proc.stdin.close(); proc.wait()
    sys.stderr.write("\n")
    if proc.returncode!=0: raise RuntimeError("ffmpeg failed")
    return out_path
