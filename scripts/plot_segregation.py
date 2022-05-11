import argparse
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy import stats

def rolling_mean(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def main(args):
    w = args.w
    st = args.st
    n = args.num
    s1 = args.s1

    color_red = 'tab:red'
    file = f"../GB_projects/{args.name}/input.txt"
    flag=False
    with open(file, 'r') as f:
        for line in f:
            if 'variable md_steps equal' in line:
                md_steps = int(line.split()[-1])
                flag=True
    if not flag:
        raise ValueError('in input file there are not variable md_steps')

    file = f"../GB_projects/{args.name}/thermo_output/{args.src}"
    df = pd.read_csv(file, sep=';', comment='#', names=['time','temp', 'pe', 'conc'])
    t_ = df['time']
    pe_ = df['pe']
    c_ = (1-df['conc'])*100
    t, pe, c = [t_[0]], [pe_[0]], [c_[0]]
    if s1>=len(t):
        print(f'Error: offset {s1} is too big for sequence of lenght {len(t)}!')
        s1 = 0
        print('offset was set to 0')
    s = slice(s1,-1)
    for i in range(1,len(t_)):
        if t_[i]==t_[i-1]:
            pass
        else:
            t.append(t_[i])
            pe.append(pe_[i])
            c.append(c_[i])
    t = np.array(t)
    pe = np.array(pe)
    c = np.array(c)

    pe1 = rolling_mean(pe[s], n)
    c1 = rolling_mean(c[s], n)
    step1 = np.arange(len(pe1))

    f, (ax1, ax3) = plt.subplots(1, 2, figsize=(10,5))
    ax1.plot(pe1)
    ax2 = ax1.twinx()
    ax2.plot(c1, color=color_red)
    
    def slope(x1, w):
        s = slice(x1,x1+w)
        y = pe1
        x = step1
        res = stats.linregress(x, y)
        return res.slope*md_steps
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
    if not args.hide:
        plt.show()
    return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-s", "--structure", required=True, dest='src')
    parser.add_argument("--w", type=int, default=3000, required=False, help='width of linear regression region for calculating slope')
    parser.add_argument("--st", type=int, default=100, required=False, help='step for points in which slope will be calculated')
    parser.add_argument("--num", type=int, default=500, required=False, help="width of rolling mean window")
    parser.add_argument("--s1", type=int, default=10, required=False, help='starting point for avg dat')
    parser.add_argument("--hide", default=False, required=False, action='store_true', help='hide the plot, only save to file')
    args = parser.parse_args()
    main(args)