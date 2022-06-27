from matplotlib import cm, colors
from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import argparse, os
import glob, re
import scipy.stats
def pretty_round(num):
    working = str(num-int(num))
    for i, e in enumerate(working[2:]):
        if e != '0':
            return int(num) + float(working[:i+3])

def main(args):
    name = args.name
    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]=='scripts':
        os.chdir('..')
    print(os.getcwd())
    path = f'GB_projects/{name}/'
    impath = f"GB_projects/{name}/images/"
    Path(impath).mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 1, dpi=500)
    
    files = []
    mus = []
    for e in args.file:
        files.append(glob.glob(f'GB_projects/{name}/output/{e}'))
    
    conc = []
    element = []

    for j, file in enumerate(files):
        mu_avg = []
        fname = file[0].split('/')[-1]
        conc.append(float(re.findall(r'\d+\.*\d*', fname)[1]))
        element.append(fname.split('_')[-5])
        for fpath in file:
            df = pd.read_csv(fpath, sep=' ', comment='#', names=['id', 'mu', 'x', 'y'])
            mu = np.array(df['mu'])
            if args.lims:
                mu = mu[mu>=np.min(args.lims)]
                mu = mu[mu<=np.max(args.lims)]

            mu_avg += list(mu)
            if args.avg:
                pass
                #ax.axvline(mu.max(), linestyle='--')
            else:
                n, bins, h = ax.hist(mu, 25, alpha = 0.7, density=True, label=fpath.split('_')[-1])   
                ax.axvline(mu.max(), linestyle='--', color=h[0]._original_facecolor)
            #ax.text(mu.max(), 10+j, round(mu.max(), 2), fontsize=7)
    
        if args.avg:
            if not args.cumulative:
                ax.hist(mu_avg, args.nbins, density=True, label=('$ c_{' + element[-1] +'}'+f' = {conc[-1]}\%$'), alpha=0.5)
                label = 'density'
                title = 'histogramm'
            else:
                x = np.sort(mu_avg)
                y = 1. * np.arange(len(mu_avg)) / (len(mu_avg) - 1)
                mu_max = (np.max(x[y<=args.y])+np.min(x[y>=args.y]))/2
                if args.mean:
                    postfix = f'<\mu> \ {round(mu_avg.mean(), 2)} eV'
                else:
                    postfix = ' \mu_{int} = ' + f'{round(mu_max, 2)} eV'
                p = ax.plot(x, y, '.', label=('$ c_{' + element[-1] +'}'+f' = {conc[-1]}\%,' + postfix + '$'))
                label = 'probability'
                title = 'distribution'
                plt.plot(mu_max, args.y, '|', markersize=20, color=p[-1].get_color(), zorder=100)
                
    if args.lims:
        plt.xlim(np.min(args.lims), np.max(args.lims))
    if args.ylim:
        plt.ylim(0, args.ylim)
    if args.cumulative:
        ax.hlines(args.y, ax.get_xlim()[0], ax.get_xlim()[1], linestyle='dashed', colors='k')
    
    plt.xlabel('$\mu, eV$')
    plt.ylabel(label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'{impath}mu_distribution.png')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=True, dest='file', metavar='OUTPUT', nargs='+',
                        help='output of mu.py, for example "mu_minimize_0K_STGB_210_Ni_2_k_20.dat"')
    parser.add_argument("--avg", required=False, help='plot average distribution', action='store_true', default=False)
    parser.add_argument("--cumulative", required=False, help='plot cumulative distribution', action='store_true', default=False)   
    parser.add_argument("--mean", required=False, help='calculate mean mu instead of mu_{y}', action='store_true', default=False)       
    parser.add_argument("--lims", required=False, default=False, nargs=2, type=float)
    parser.add_argument("--ylim", required=False, default=False, type=float)
    parser.add_argument("--nbins", required=False, default=250, type=int)
    parser.add_argument("-y", required=False, default=0.9, type=float)
    args = parser.parse_args()
    main(args)