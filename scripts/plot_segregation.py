import argparse
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True)
parser.add_argument("-s", "--structure", required=True, dest='src')
parser.add_argument("--w", type=int, default=3000, required=False, help='width of linear regression region for calculating slope')
parser.add_argument("--st", type=int, default=100, required=False, help='step for points in which slope will be calculated')
parser.add_argument("--num", type=int, default=500, required=False, help="width of rolling mean window")
parser.add_argument("--s1", type=int, default=10, required=False, help='starting point for avg dat')
args = parser.parse_args()
w = args.w
st = args.st
n = args.num
s1 = args.s1

color_red = 'tab:red'

file = f"../GB_projects/{args.name}/thermo_output/{args.src}"
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
f.suptitle(args.name)
f.tight_layout()
ax1.text(0.1, 0.95, f'rolling mean over {n}', transform=ax1.transAxes)
ax3.text(0.5, 0.02, f'dx = {w}', transform=ax3.transAxes)
plt.savefig(f"../GB_projects/{args.name}/images/{(args.src).replace('.txt', '.png')}")
plt.show()