w = 3000
st = 100
name = 'STGB_210_Ni_1_k_100'
n = 500
s1 = 10

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys
color_red = 'tab:red'

w, st, n, s1 = sys.argv[1:]
w = int(w)
st = int(st)
n = int(n)
s1 = int(s1)

file = f"segregation_{name}.txt"
df = pd.read_csv(file, sep=';', comment='#', names=['time','temp', 'pe', 'conc'])
t = df['time']
pe = df['pe']
T = df['temp']
c = (1-df['conc'])*100
step = t*1000
s = slice(s1,-1)
def rolling_mean(numbers_series, window_size):
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    final_list = moving_averages_list[window_size - 1:]
    return final_list

pe1 = rolling_mean(pe, n)
c1 = rolling_mean(c, n)
step1 = np.arange(len(pe1))

f, (ax1, ax3) = plt.subplots(1, 2, figsize=(10,5))
ax1.plot(pe1[s])
ax2 = ax1.twinx()
ax2.plot(c1[s], color=color_red)
from scipy import stats
def slope(x1, w):
    s = slice(x1,x1+w)
    y = pe1[s]
    x = step1[s]
    res = stats.linregress(x, y)
    return res.slope*100
res=[]

for i in range(round((len(step1)-w)/st)):
    x1 = i*st
    res.append(slope(x1, w))

ax3.axhline(y=0.001, linestyle='--', color='gray')
ax3.axhline(y=-0.001, linestyle='--', color='gray')
ax1.set_xlabel('$step$')
ax1.set_ylabel('$<E_{pot}>_{roll}, eV$')
ax2.set_ylabel('$concentration$', color=color_red)
ax3.set_xlabel(f'$step\cdot {st}$')
ax3.set_ylabel('$\partial_t<E_{pot}>_{roll}, eV/step$')
ax3.plot(res, 'o')
f.suptitle(name)
f.tight_layout()
ax1.text(0.1, 0.95, f'rolling mean over {n}', transform=ax1.transAxes)
ax3.text(0.5, 0.02, f'dx = {w}', transform=ax3.transAxes)
plt.savefig('plot.segregation.png')
plt.show()