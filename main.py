import pylab
import math

vinit = 0.0
dt = 0.01
ena = 115
gna = 120
ek = -12
gk = 36
el = 10.6
gl = 0.3

def upd(x, dlta_x):
    return x + dlta_x * dt

def mnh0(a, b):
    return a / (a + b)

def am (v) : return (2.5 - 0.1 * v) / (math.exp(2.5 - 0.1 * v) - 1)
def bm (v) : return 4 * math.exp((-1) * v / 18)
def an (v) : return (0.1 - 0.01 * v) / (math.exp(1 - (0.1 * v)) - 1)
def bn (v) : return 0.125 / math.exp((-1) * v / 80)
def ah (v) : return 0.07 * math.exp((-1) * v / 20)
def bh (v) : return 1 / (math.exp(3 - (0.1) * v) + 1)

m0 = mnh0(am(0), bm(0)) 
n0 = mnh0(an(0), bn(0))
h0 = mnh0(ah(0), bh(0))

def ina(m, h, v):
    return gna * (m ** 3) * h * (v - ena)

def ik(n, v):
    return gk * (n ** 4) * (v - ek)

def il(v):
    return gl * (v - el)

def newS(v, m, n, h, t):
    if t < 5.0 or t > 6.0:
        istim = 0.0
    else:
        istim = 20.0
    dv = istim - (ina(m, h, v) + ik(n,v) + il(v))
    dm = am(v) * (1 - m) - bm(v) * m
    dn = an(v) * (1 - n) - bn(v) * n
    dh = ah(v) * (1 - h) - bh(v) * h
    vp = upd(v, dv)
    tp = t + dt
    mp = upd(m, dm)
    np = upd(n, dn)
    hp = upd(h, dh)
    return (vp, mp, np, hp, tp)

vs = []
ms = []
ns = []
hs = []
ts = []
a, b, c, d, e = newS(vinit, m0, n0, h0, 0.0)
vs.append(a)
ms.append(b)
ns.append(c)
hs.append(d)
ts.append(e)
for i in (range(2, 3000)):
    a, b, c, d, e = newS(vs[-1], ms[-1], ns[-1], hs[-1], ts[-1])
    vs.append(a)
    ms.append(b)
    ns.append(c)
    hs.append(d)
    ts.append(e) 

pylab.plot(ts, ms)
pylab.plot(ts, ns)
pylab.plot(ts, hs)

pylab.show()