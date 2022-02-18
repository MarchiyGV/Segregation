import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys
name = sys.argv[1]
n = int(sys.argv[2])
file = f"../GB_projects/{name}/thermo_output/thermal_relax.txt"
print(file)
df = pd.read_csv(file, sep=';', comment='#', names=['t','T', 'P', 'pe'])
t = df['t']
pe = df['pe']
T = df['T']
P = df['P']

def rolling_mean(numbers_series, window_size):
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    final_list = moving_averages_list[window_size - 1:]
    return final_list

pe1 = rolling_mean(pe, n)
P1 = rolling_mean(P, n)
t1 = t[len(pe)-len(pe1):]
t = np.array(t)

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.plot(t, pe)
ax2.plot(t, P)
ax1.set_xlabel('$t, ps$')
ax2.set_xlabel('$t, ps$')
ax1.set_ylabel('$E_{pot}, eV$')
ax2.set_ylabel('$P, bar$')

ax3.plot(t1, pe1)
ax4.plot(t1, P1)
ax3.set_xlabel('$t, ps$')
ax4.set_xlabel('$t, ps$')
ax3.set_ylabel('$<E_{pot}>_{roll}, eV$')
ax4.set_ylabel('$<P>_{roll}, bar$')
ax3.set_title(f'rolling mean over {n}')
ax4.set_title(f'rolling mean over {n}')
f.suptitle(f'Thermal relax {name} {round(t[-1])}ps')
f.tight_layout()
plt.savefig(f'../GB_projects/{name}/images/plot.thermal_relax_time{round(t[-1])}.png')

