from matplotlib import cm, colors
from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import argparse, os

def main(args):
    name = args.name
    plot_ni = args.plot_ni
    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]=='scripts':
        os.chdir('..')
    print(os.getcwd())
    path = f'GB_projects/{name}/'
    impath = f"GB_projects/{name}/images/"
    Path(impath).mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, len(args.file), dpi=100) # give plots a rectangular frame
    cmap = cm.viridis

    if args.norm:
        val_min = min(*args.norm)
        val_max = max(*args.norm)


    if not args.norm:
        for j, file in enumerate(args.file):
            fpath = f'GB_projects/{name}/output/{file}'
            df = pd.read_csv(fpath, sep=' ', comment='#', names=['id', 'mu', 'x', 'y'])
            mus = np.array(df['mu'])
            if j>0:
                if mus.min() < val_min:
                    val_min = mus.min()
                if val_max < mus.max():
                    val_max = mus.max()
            elif j==0:
                val_min = mus.min()
                val_max = mus.max()
            print('#Mu (min, max):', mus.min(), mus.max())

    for j, file in enumerate(args.file):
        try:
            ax = axes[j]
        except:
            ax = axes
        fpath = f'GB_projects/{name}/output/{file}'

        with open(fpath, 'r') as f:
            idni, xni, yni, zni = [], [], [], []
            set = [idni, xni, yni, zni]
            for line in f:
                if 'xlen' in line:
                    xlen = float(line.split()[-1])
                if 'ylen' in line:
                    ylen = float(line.split()[-1])
                if 'xmin' in line:
                    xmin = float(line.split()[-1])
                if 'ymin' in line:
                    ymin = float(line.split()[-1])
                if '#Ni' in line:
                    _args = line.split()
                    _id, _xni, _yni, _zni = map(float, _args[1:])
                    _id = int(_id)   
                    _set = [_id, _xni, _yni, _zni]
                    for j, e in enumerate(_set):
                        set[j].append(e)
        df = pd.read_csv(fpath, sep=' ', comment='#', names=['id', 'mu', 'x', 'y'])
        xmax = xmin + xlen
        ymax = ymin + ylen
        x = np.array(df['x'])
        y = np.array(df['y'])
        mus = np.array(df['mu'])

        for i in range(len(x)):
            c = (mus[i]-val_min)/(val_max-val_min)
            color = cmap(c)
            circle = plt.Circle((x[i], y[i]), 0.5, color=color)
            ax.add_artist(circle)
            
        if plot_ni:
            ax.plot(xni, yni, 'x')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_aspect('equal')
        ax.set_title(file, fontsize = 5)


    norm = colors.Normalize(vmin=val_min, vmax=val_max) 
    print('#Norm (min, max):', val_min, val_max)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.24, 0.025, 0.51])
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
    cbar.ax.set_ylabel('$\mu, eV$', rotation=90)
    plt.savefig(f'{impath}{args.file}.png')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=True, dest='file', metavar='OUTPUT', nargs='+',
                        help='output of mu.py, for example "mu_minimize_0K_STGB_210_Ni_2_k_20.dat"')
    parser.add_argument("--plot-ni", required=False, default=False, dest='plot_ni', action='store_true',
                        help='plot Ni on graph')
    parser.add_argument("--norm", required=False, default=False, dest='norm', nargs=2, metavar='MIN MAX',
                        type=float, help='If provided, adjust \\mu color legend for this value')
    args = parser.parse_args()
    main(args)

