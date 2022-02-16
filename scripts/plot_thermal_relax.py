import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
file = "thermo.txt"
df = pd.read_csv(file, sep=';', comment='#', names=['t','T', 'P', 'pe'])
t = df['t']
pe = df['pe']
T = df['T']
P = df['P']

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
x1 = 10
x2 = -1
ax1.plot(t, pe)
ax2.plot(t, P)
ax1.axvline(x=t[x1], linestyle='--', color='grey')
ax2.axvline(x=t[x1], linestyle='--', color='grey')
ax1.set_xlabel('$t, ps$')
ax2.set_xlabel('$t, ps$')
ax1.set_ylabel('$E_{pot}, eV$')
ax2.set_ylabel('$P, bar$')

ax3.plot(t[x1:x2], pe[x1:x2])
ax4.plot(t[x1:x2], P[x1:x2])
ax3.set_xlabel('$t, ps$')
ax4.set_xlabel('$t, ps$')
ax3.set_ylabel('$E_{pot}, eV$')
ax4.set_ylabel('$P, bar$')
f.tight_layout()
plt.savefig('plot.thermal_relax.png')
