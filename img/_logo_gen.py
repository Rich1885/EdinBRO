# EDINBRO logó: skót Saltire + észak-ír Ulster Banner, keresztbe tett rúdon.
# A zászlók perspektivikus transzformációval feszülnek a rúdra, nem csak forgatva.
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

S = 5                       # supersampling
W, H = 300, 168
CW, CH = W*S, H*S

GOLD   = (198, 156, 44)
GOLD_D = (146, 108, 24)
GOLD_L = (232, 198, 104)
BLUE   = (0, 90, 178)
RED    = (203, 20, 43)
WHITE  = (255, 255, 255)
EDGE   = (28, 34, 46)       # vékony sötét kontúr, hogy a fehér is látszódjon

def sk(*t): return tuple(int(v*S) for v in t)

# ---------------- zászlómintázatok ----------------
def saltire(w, h):
    im = Image.new("RGBA", (w, h), BLUE)
    d = ImageDraw.Draw(im)
    d.line([(0,0),(w,h)], fill=WHITE, width=int(h*0.20))
    d.line([(0,h),(w,0)], fill=WHITE, width=int(h*0.20))
    return im

def ulster(w, h):
    im = Image.new("RGBA", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    bw = int(h*0.16)
    d.rectangle([0, h//2-bw//2, w, h//2+bw//2], fill=RED)
    d.rectangle([w//2-bw//2, 0, w//2+bw//2, h], fill=RED)
    cx, cy, r = w//2, h//2, int(h*0.31)
    # hatágú csillag
    pts=[]
    for i in range(12):
        a = np.pi/2 + i*np.pi/6
        rr = r if i%2==0 else r*0.5
        pts.append((cx+rr*np.cos(a), cy-rr*np.sin(a)))
    d.polygon(pts, fill=WHITE, outline=RED, width=max(2,int(h*0.022)))
    hr=int(r*0.42)
    d.ellipse([cx-hr,cy-hr,cx+hr,cy+hr], fill=RED)          # vörös kéz helyén
    d.polygon([(cx-r*0.9, cy-r*1.02),(cx+r*0.9, cy-r*1.02),
               (cx+r*0.45, cy-r*0.55),(cx-r*0.45, cy-r*0.55)], fill=GOLD)  # korona
    return im

# --------- kép ráfeszítése egy célnégyszögre (perspektíva) ---------
def coeffs(dst, src):
    m=[]
    for (dx,dy),(sx,sy) in zip(dst,src):
        m.append([dx,dy,1,0,0,0,-sx*dx,-sx*dy])
        m.append([0,0,0,dx,dy,1,-sy*dx,-sy*dy])
    A=np.array(m,dtype=float); B=np.array(src,dtype=float).reshape(8)
    return np.linalg.lstsq(A,B,rcond=None)[0]

def feszit(base, flag, quad):
    """quad: [BF, JF, JA, BA] a célvásznon (bal-fent, jobb-fent, jobb-lent, bal-lent)"""
    w,h = flag.size
    src = [(0,0),(w,0),(w,h),(0,h)]
    c = coeffs(quad, src)
    warped = flag.transform((CW,CH), Image.PERSPECTIVE, c, resample=Image.BICUBIC)
    # vékony sötét kontúr a zászló köré
    ol = Image.new("RGBA",(CW,CH),(0,0,0,0))
    ImageDraw.Draw(ol).polygon(quad, outline=EDGE, width=max(2,int(1.6*S)))
    base.alpha_composite(warped); base.alpha_composite(ol)

base = Image.new("RGBA", (CW, CH), (0,0,0,0))
d = ImageDraw.Draw(base)

# ---------------- rudak ----------------
pw = int(8.5*S)
for a,b in ((sk(163,158), sk(95,16)), (sk(137,158), sk(205,16))):
    d.line([a,b], fill=GOLD, width=pw)
    d.line([a,b], fill=GOLD_D, width=max(1,pw//7))

# ---------------- zászlók ----------------
FW, FH = int(150*S), int(96*S)
# bal (skót) — a bal rúdra feszül, balra leng
feszit(base, saltire(FW,FH),
       [sk(12,42), sk(100,29), sk(133,95), sk(20,110)])
# jobb (észak-ír) — a jobb rúdra feszül, jobbra leng
feszit(base, ulster(FW,FH),
       [sk(200,29), sk(288,42), sk(280,110), sk(167,95)])

# ---------------- rúdgombok ----------------
d = ImageDraw.Draw(base)
for cx, cy in (sk(95,15), sk(205,15)):
    r = int(8.5*S)
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=GOLD, outline=GOLD_D, width=max(1,int(0.8*S)))
    d.ellipse([cx-r+int(2.4*S), cy-r+int(2*S), cx-int(0.5*S), cy-int(1*S)], fill=GOLD_L)

out = base.resize((W,H), Image.LANCZOS)
out = out.crop(out.getbbox())
out.save("logo.png")
print("logo.png", out.size)
