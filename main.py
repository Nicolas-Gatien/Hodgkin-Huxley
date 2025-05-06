import pylab
import math

INITIAL_VOLTAGE = 0.0
TIMESTEP = 0.01
e_SODIUM = 115
SODIUM_CHANNEL_CONDUCTANCE = 120
e_POTASSIUM = -12
POTASSIUM_CHANNEL_CONDUCTANCE = 36
e_LEAK_CURRENT = 10.6
LEAK_CURRENT_CHANNEL_CONDUCTANCE = 0.3

def update(x, dlta_x):
    return x + dlta_x * TIMESTEP

def mnh0(a, b):
    return a / (a + b)

def am (voltage) : return (2.5 - 0.1 * voltage) / (math.exp(2.5 - 0.1 * voltage) - 1)
def bm (voltage) : return 4 * math.exp((-1) * voltage / 18)

def an (voltage) : return (0.1 - 0.01 * voltage) / (math.exp(1 - (0.1 * voltage)) - 1)
def bn (voltage) : return 0.125 / math.exp((-1) * voltage / 80)

def ah (voltage) : return 0.07 * math.exp((-1) * voltage / 20)
def bh (voltage) : return 1 / (math.exp(3 - (0.1) * voltage) + 1)

m0 = mnh0(am(INITIAL_VOLTAGE), bm(INITIAL_VOLTAGE)) 
n0 = mnh0(an(INITIAL_VOLTAGE), bn(INITIAL_VOLTAGE))
h0 = mnh0(ah(INITIAL_VOLTAGE), bh(INITIAL_VOLTAGE))

def calculate_sodium(m, h, voltage):
    return SODIUM_CHANNEL_CONDUCTANCE * (m ** 3) * h * (voltage - e_SODIUM)

def calculate_potassium(n, voltage):
    return POTASSIUM_CHANNEL_CONDUCTANCE * (n ** 4) * (voltage - e_POTASSIUM)

def calculate_leak_currents(voltage):
    return LEAK_CURRENT_CHANNEL_CONDUCTANCE * (voltage - e_LEAK_CURRENT)

def new_step(voltage, m, n, h, current_timestep):
    if current_timestep < 5.0 or current_timestep > 6.0:
        injected_stimulation = 0.0
    else:
        injected_stimulation = 20.0
    
    d_voltage = injected_stimulation - (calculate_sodium(m, h, voltage) + calculate_potassium(n, voltage) + calculate_leak_currents(voltage))
    dm = am(voltage) * (1 - m) - bm(voltage) * m
    dn = an(voltage) * (1 - n) - bn(voltage) * n
    dh = ah(voltage) * (1 - h) - bh(voltage) * h
    voltage_p = update(voltage, d_voltage)
    timestep_p = current_timestep + TIMESTEP
    mp = update(m, dm)
    np = update(n, dn)
    hp = update(h, dh)
    return (voltage_p, mp, np, hp, timestep_p)

voltage_s = []
ms = []
ns = []
hs = []
timestep_s = []
a, b, c, d, e = new_step(INITIAL_VOLTAGE, m0, n0, h0, 0.0)
voltage_s.append(a)
ms.append(b)
ns.append(c)
hs.append(d)
timestep_s.append(e)
for i in (range(2, 3000)):
    a, b, c, d, e = new_step(voltage_s[-1], ms[-1], ns[-1], hs[-1], timestep_s[-1])
    voltage_s.append(a)
    ms.append(b)
    ns.append(c)
    hs.append(d)
    timestep_s.append(round(e, 2)) 

pylab.plot(timestep_s, ms)
pylab.plot(timestep_s, ns)
pylab.plot(timestep_s, hs)

pylab.show()