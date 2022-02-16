import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
file = "surface_thermal_relax.txt"
df = pd.read_csv(file, sep=';', comment='#', names=['t','T', 'pe'])
t = df['t']
pe = df['pe']
T = df['T']

f, (ax1, ax3) = plt.subplots(1, 2)
x1 = 200
x2 = -1
ax1.plot(t, pe)
ax1.axvline(x=t[x1], linestyle='--', color='grey')
ax1.set_xlabel('$t, ps$')
ax1.set_ylabel('$E_{pot}, eV$')

ax3.plot(t[x1:x2], pe[x1:x2])
ax3.set_xlabel('$t, ps$')
ax3.set_ylabel('$E_{pot}, eV$')
f.tight_layout()
plt.savefig('plot.surface_thermal_relax.png')
